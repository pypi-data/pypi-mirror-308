
import asyncio, sys, traceback, pathlib

import curses

import logging
logger = logging.getLogger(__name__)

from ..ipyclient import IPyClient
from ..events import (delProperty, defSwitchVector, defTextVector, defNumberVector, defLightVector, defBLOBVector,
                     setSwitchVector, setTextVector, setNumberVector, setLightVector, setBLOBVector, Message, VectorTimeOut)

from . import windows
from . import widgets

from .devicesscreen import DevicesScreen
from .choosevectorscreen import ChooseVectorScreen
from .vectorscreen import VectorScreen
from .memberscreen import MemberScreen

# set limit to terminal size
MINROWS = 22
MINCOLS = 78


class _Client(IPyClient):

    """Overrides IPyClient
       On receiving an event, appends it into eventque
       Which will pass the received event into ConsoleClient"""

    async def rxevent(self, event):
        """Add event to eventque"""
        eventque = self.clientdata['eventque']
        await self.queueput(eventque, event)



class ConsoleClient:

    def __init__(self, indihost="localhost", indiport=7624, blobfolder=None):
        """If given, blobfolder should be an existing folder where BLOBs will be saved"""

        if blobfolder:
            if isinstance(blobfolder, pathlib.Path):
                self.blobfolder = blobfolder
            else:
                self.blobfolder = pathlib.Path(blobfolder).expanduser().resolve()
            if not self.blobfolder.is_dir():
                raise KeyError("If given, the BLOB's folder should be an existing directory")
            self.blobenabled = True
        else:
            self.blobfolder = None
            self.blobenabled = False

        # this is populated with events as they are received
        self.eventque = asyncio.Queue(maxsize=4)

        self.client = _Client(indihost, indiport, eventque = self.eventque)

        # set up screen
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.mousemask(curses.BUTTON1_RELEASED)

        self.maxrows, self.maxcols = self.stdscr.getmaxyx()

        if self.maxrows < MINROWS or self.maxcols < MINCOLS:
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.curs_set(1)
            curses.echo()
            curses.endwin()
            print("Terminal too small! Try 80 columns x 24 rows")
            sys.exit(1)


        # Idle, OK, Busy or Alert.
        # gray, green, yellow and red

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)

        # this keeps track of which screen is being displayed,
        # initially start with the messages screen
        self.screen = windows.MessagesScreen(self.stdscr, self)
        self.screen.show()

        # shutdown routine sets this to True to stop coroutines
        self._stop = False
        # this is set when asyncrun is finished
        self.stopped = asyncio.Event()

        # these are set to True when asyncrun is finished
        self.updatescreenstopped = False
        self.getinputstopped = False

        # list of known device names, this is needed to send
        # BLOB's enabled
        self.devicenames = []

        # BLOBfiles, is a dictionary of {(devicename,vectorname,membername):filepath}
        self.BLOBfiles = {}

    @property
    def stop(self):
        "returns self._stop, being the instruction to stop the client"
        return self._stop

    def debug_verbosity(self, verbose):
        """Set how verbose the debug xml logs will be when created.

           |  0 no xml logs will be generated
           |  1 for transmitted/received vector tags only,
           |  2 for transmitted/received vectors, members and contents (apart from BLOBs)
           |  3 for all transmitted/received data including BLOBs."""
        self.client.debug_verbosity(verbose)

    def color(self, state):
        "Returns curses.color_pair given a state"
        if not curses.has_colors():
            return curses.color_pair(0)
        state = state.lower()
        if state == "ok":
            return curses.color_pair(1)
        elif state == "busy":
            return curses.color_pair(2)
        elif state == "alert":
            return curses.color_pair(3)
        return curses.color_pair(0)


    @property
    def connected(self):
        return self.client.connected


    def shutdown(self):
        "Shuts down the client"
        if not self.client.stopped.is_set():
            # client is still running, shut it down
            self.client.shutdown()
        # Now stop console co-routines
        self._stop = True


    async def _checkshutdown(self):
        "If the client stops, shutdown"
        await self.client.stopped.wait()
        # so the ipyclient has stopped for some reason
        self.shutdown()


    def console_reset(self):
        "Resets console, called in finally clause at program shutdown"
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.curs_set(1)
        curses.echo()
        curses.endwin()


    async def updatescreen(self):
        "Update while events are being received"
        try:
            while not self._stop:
                await asyncio.sleep(0)
                if isinstance(self.screen, windows.TooSmall):
                    await asyncio.sleep(0.1)
                    continue
                if self.connected and isinstance(self.screen, windows.MessagesScreen):
                    if self.screen.showing_disconnected:
                        # removes showing_disconnected flag and focuses on Devices button
                        self.screen.show()
                if not self.connected:
                    if isinstance(self.screen, windows.MessagesScreen):
                        # set disconnected status and focus on the quit button
                        if not self.screen.showing_disconnected:
                            self.devicenames.clear()
                            self.screen.showunconnected() # sets showing_disconnected
                    else:
                        # when not connected, show messages screen
                        self.screen.close("Messages")
                        continue

                # act when an event is received
                try:
                    event = await asyncio.wait_for(self.eventque.get(), 0.2)
                except asyncio.TimeoutError:
                    # no event received, so do not update screen
                    continue
                self.eventque.task_done()

                if isinstance(event, VectorTimeOut) and (event.devicename == self.screen.devicename):
                    if isinstance(self.screen, ChooseVectorScreen):
                        self.screen.timeout(event)
                        continue
                    if isinstance(self.screen, VectorScreen) and (self.screen.vectorname == event.vectorname):
                        self.screen.timeout(event)
                        continue
                    if isinstance(self.screen, MemberScreen) and (self.screen.vectorname == event.vectorname):
                        self.screen.timeout(event)
                        continue
                if hasattr(event, 'devicename'):
                    # if this is a new device, update it with BLOB status
                    if event.devicename and (event.devicename not in self.devicenames):
                        if event.devicename in self.client:
                            device = self.client[event.devicename]
                            if device.enable:
                                # new devicename
                                self.devicenames.append(event.devicename)
                                if self.blobenabled:
                                    await self.client.send_enableBLOB('Also', event.devicename)
                                else:
                                    await self.client.send_enableBLOB('Never', event.devicename)
                # If the event is a received BLOB, save it to the BLOB Folder
                if isinstance(event, setBLOBVector):
                    loop = asyncio.get_running_loop()
                    # make filename from timestamp
                    timestampstring = event.timestamp.strftime('%Y%m%d_%H_%M_%S')
                    for membername, membervalue in event.items():
                        sizeformat = event.sizeformat[membername]
                        filename =  membername + "_" + timestampstring + sizeformat[1]
                        counter = 0
                        while True:
                            filepath = self.blobfolder / filename
                            if filepath.exists():
                                # append a digit to the filename
                                counter += 1
                                filename = membername + "_" + timestampstring + "_" + str(counter) + sizeformat[1]
                            else:
                                # filepath does not exist, so a new file with this filepath can be created
                                break
                        await loop.run_in_executor(None, filepath.write_bytes, membervalue)
                        # record the filepath
                        self.BLOBfiles[(event.devicename, event.vectorname, membername)] = filepath
                if isinstance(self.screen, windows.MessagesScreen):
                    self.screen.update(event)
                elif isinstance(self.screen, DevicesScreen):
                    self.screen.update(event)
                elif isinstance(self.screen, windows.EnableBLOBsScreen):
                    self.screen.update(event)
                elif event.devicename == self.screen.devicename:
                    # the remaining screens are only affected if the event devicename
                    # is the device they refer to
                    if isinstance(event, delProperty):
                        if event.vectorname is None:
                            # the whole device is disabled,
                            if event.devicename and (event.devicename in self.devicenames):
                                self.devicenames.remove(event.devicename)
                            # show devicesscreen
                            self.screen.close("Devices")
                        elif isinstance(self.screen, ChooseVectorScreen):
                            # one vector has been disabled, update the ChooseVectorScreen
                            self.screen.update(event)
                        elif isinstance(self.screen, VectorScreen) and (self.screen.vectorname == event.vectorname):
                            # This vector has been disabled, show ChooseVectorScreen
                            self.screen.close("Vectors")
                    # so its not a delete property
                    elif isinstance(self.screen, ChooseVectorScreen):
                        self.screen.update(event)
                    elif isinstance(self.screen, VectorScreen) and (self.screen.vectorname == event.vectorname):
                        # The event refers to this vector
                        self.screen.update(event)
                    elif isinstance(self.screen, MemberScreen) and (self.screen.vectorname == event.vectorname) and (self.screen.membername in event):
                        # The event refers to this vector
                        self.screen.update(event)
        except Exception:
            logger.exception("Exception report from ConsoleControl.updatescreen")
            raise
        finally:
            self.updatescreenstopped = True


    async def getinput(self):
        """This is awaited in the gather run by the asyncrun method. It is a continuously
           running loop that awaits self.screen.inputs() which returns an 'action'. This
           action may shut down the screen, or start another screen object"""
        try:
            while not self._stop:
                action = await self.screen.inputs()
                if action == "Quit":
                    self.shutdown()
                    break

                if action == "Resize":
                    self.maxrows, self.maxcols = self.stdscr.getmaxyx()
                    if self.maxrows < 10 or self.maxcols < 40:
                        self.shutdown()
                        break
                    if self.maxrows < MINROWS or self.maxcols < MINCOLS:
                        self.screen = windows.TooSmall(self.stdscr, self)
                        self.screen.show()
                        continue

                # action can be one of Quit, Resize, Devices, Messages, EnableBLOBs, Vectors

                # if the screen is a TooSmall screen then either accept
                # a resize or quit, if resized to a reasonable size, then open
                # a MessagesScreen

                if isinstance(self.screen, windows.TooSmall):
                    if action == "Resize":
                        # To get here the screen must be greater than MINROWS, MINCOLS
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    continue

                # MessagesScreen

                if isinstance(self.screen, windows.MessagesScreen):
                    if action == "Resize":
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Devices":
                        self.screen = DevicesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "EnableBLOBs":
                        self.screen = windows.EnableBLOBsScreen(self.stdscr, self)
                        self.screen.show()
                    continue

                # EnableBLOBsScreen

                if isinstance(self.screen, windows.EnableBLOBsScreen):
                    if action == "Resize":
                        self.screen = windows.EnableBLOBsScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Messages":
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Devices":
                        self.screen = DevicesScreen(self.stdscr, self)
                        self.screen.show()
                    continue

                # DevicesScreen

                if isinstance(self.screen, DevicesScreen):
                    if action == "Resize":
                        self.screen = DevicesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Messages":
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Vectors":
                        self.screen = ChooseVectorScreen(self.stdscr, self, self.screen.devicename)
                        self.screen.show()
                    continue

                # ChooseVectorScreen

                if isinstance(self.screen, ChooseVectorScreen):
                    if action == "Resize":
                        self.screen = ChooseVectorScreen(self.stdscr, self, self.screen.devicename, group=self.screen.groupwin.active)
                        self.screen.show()
                    elif action == "Messages":
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Devices":
                        self.screen = DevicesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Vectors":
                        # get device, vector and show VectorScreen
                        self.screen = VectorScreen(self.stdscr, self, self.screen.devicename, self.screen.vectorname)
                        self.screen.show()
                    continue

                # VectorScreen

                if isinstance(self.screen, VectorScreen):
                    if action == "Resize":
                        self.screen = VectorScreen(self.stdscr, self, self.screen.devicename, self.screen.vectorname)
                        self.screen.show()
                    elif action == "Messages":
                        self.screen = windows.MessagesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Devices":
                        self.screen = DevicesScreen(self.stdscr, self)
                        self.screen.show()
                    elif action == "Vectors":
                        self.screen = ChooseVectorScreen(self.stdscr, self, self.screen.devicename, group=self.screen.vector.group)
                        self.screen.show()
                    elif action == "Member":
                        self.screen = MemberScreen(self.stdscr, self, self.screen.devicename, self.screen.vectorname, self.screen.membername)
                        self.screen.show()
                    continue

                # MemberScreen

                if isinstance(self.screen, MemberScreen):
                    if action == "Resize":
                        self.screen = MemberScreen(self.stdscr, self, self.screen.devicename, self.screen.vectorname, self.screen.membername)
                        self.screen.show()
                    else:
                        # any other key goes back to VectorScreen
                        self.screen = VectorScreen(self.stdscr, self, self.screen.devicename, self.screen.vectorname)
                        self.screen.show()

        except Exception:
            logger.exception("Exception report from ConsoleControl.getinput")
            raise
        finally:
            self.getinputstopped = True


    async def send_enableBLOB(self):
        "Sends Also to enable blobs for all devices"
        if not self.blobenabled:
            return
        for devicename,device in self.client.items():
            if device.enable:
                await self.client.send_enableBLOB('Also', devicename)


    async def send_disableBLOB(self):
        "Sends Never to disable blobs for all devices"
        if self.blobenabled:
            return
        for devicename,device in self.client.items():
            if device.enable:
                await self.client.send_enableBLOB('Never', devicename)


    async def asyncrun(self):
        """Await this method to run the client."""
        self._stop = False
        try:
            await asyncio.gather(self.client.asyncrun(), self.updatescreen(), self.getinput(), self._checkshutdown())
        finally:
            self.stopped.set()
            self._stop = True
