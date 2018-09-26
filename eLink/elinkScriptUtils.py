from __future__ import unicode_literals
from time import sleep
from enum import IntFlag, unique, Enum

debug_enable = 0

ABS = 0
REL = 1


@unique
class ElinkEvent(Enum):
    EVT_USB_EXT_RESET = 1
    EVT_USB_EXT_CONFIGURED = 2
    EVT_EXT_BUFFER_FULL = 3
    EVT_KEY_PHANTOM = 4
    EVT_USB_KEY_SET_PROTOCOL = 5
    EVT_USB_KEY_SET_REPORT = 6
    EVT_USB_KEY_SET_IDLE = 7
    EVT_USB_MAIN_RESET = 8
    EVT_USB_MAIN_CONFIGURED = 9
    EVT_USB_MAIN_CONNECTED = 11
    EVT_USB_MAIN_DISCONNECTED = 12
    EVT_STORAGE_FIRST_READ = 13
    EVT_STORAGE_FIRST_READ2 = 14
    EVT_STORAGE_FIRST_WRITE = 15
    EVT_STORAGE_FIRST_WRITE2 = 16
    EVT_RESET_MAX_REACH = 17
    EVT_FILE1_ERROR = 18
    EVT_FILE2_ERROR = 19
    EVT_FILE_VNC_ERROR = 20
    EVT_NAND_ERROR = 21
    EVT_VNC_HIP_CONNECTED = 22
    EVT_STORAGE_IDLE = 23
    EVT_STORAGE_REGION_COUNT = 24
    EVT_KEY_TRIGGER_ON_RESET = 25
    EVT_KEY_ON_POWER_DONE = 26
    EVT_DISK_ON_POWER_DONE = 27


@unique
class UsbMode(IntFlag):
    # Configure eLinkKVM to USB Keyboard
    USB_MODE_KEY = 0x0001
    # Configure eLinkKVM to USB Mouse Keyboard
    USB_MODE_MOUSE = 0x0002
    # Configure eLinkKVM to USB Mass storage
    USB_MODE_MSC = 0x0004
    # Special Mode, set it if want to speed up Booster Mode
    USB_MODE_VNC_HID = 0x0008
    # Configure eLinkKVM to CDC device Keyboard (not support yet)
    USB_MODE_CDC = 0x0010
    # Configure eLinkKVM to USB Video class device (not support yet)
    USB_MODE_UVC = 0x0020
    # Configure eLinkKVM to USB Absolute Mouse
    USB_MODE_MOUSE_ABS = 0x0040
    pass


class VncMode(IntFlag):
    VNC_MODE_DUMMY = 0x00
    # RGB mode , display VGA graphic
    VNC_MODE_RGB = 0x01
    # Booster mode , display server graphic through Booster protocol
    VNC_MODE_BOOSTER = 0x02
    # alias Booster mode , display server graphic through Booster protocol
    VNC_MODE_MSC = 0x02
    # serial mode , display serial data from Serial port
    VNC_MODE_SERIAL = 0x03
    # IPMI mode , display IPMI SOL (Serial overlan)
    VNC_MODE_IPMI = 0x04
    pass


class KeyMode(IntFlag):
    KEY_INTF_NONE = 0  # deactive keyboard
    KEY_INTF_HID = 1  # enable HID keyboard
    KEY_INTF_VNC = 2  # enable VNC keyboard
    pass


class PointerMode(IntFlag):
    # Cấu hình Mouse sử dụng HID USB
    POINT_INTF_HID = 1
    # Cấu Hinh Mouse sử dụng mode VNC (Sử dụng VNC interface)
    POINT_INTF_VNC = 2
    # Cấu Hinh Mouse sử dụng mode USB HID Absolute
    POINT_INTF_HID_ABS = 3
    pass


class PointerAct(IntFlag):
    MOVE = 0
    LEFT_DOWN = 1
    RIGHT_DOWN = 2
    CLICK = 4
    LEFT_DOWN_CLICK = LEFT_DOWN | CLICK
    RIGHT_DOWN_CLICK = RIGHT_DOWN | CLICK


class Coordinate:
    def __init__(self, data: list):
        self.x = int(data[0])
        self.y = int(data[1])
        self.w = int(data[2])
        self.h = int(data[3])


def dbg(msg):
    if debug_enable:
        print(msg)



def getCurrentConnection():
    gConn = elink.getConnection()
    if len(gConn) != 0:
        return gConn[0]
    return None


def sendCommand(elinkObj, command):
    elinkObj.sendString(command)
    sleep(1)
    elinkObj.sendKey("Enter")
    sleep(1)


def waitUntilNoChange(elinkObj, delay=None):
    if delay is None:
        delay = 5000
    e = elinkObj.getEvent()

    elinkObj.setVncIdle(delay)
    while e.getIdCode() != 28:
        e = elinkObj.getEvent()
        # dbg(" |- event id: " + str(e.getIdCode()))

        if e.getIdCode() == 28:
            elinkObj.setVncIdle(0)
            return
        e = elinkObj.getEvent()


def check_maching_image(elinkObj, img, score=0.9):
    loc = elinkObj.matchScreen(img, score, 500)
    return Coordinate(loc[0])


def waitImage(elinkObj: object, img: object, score: object = 0.9, attentionPeriod: object = 3000) -> object:
    """
    :param elinkObj:
    :param img: 
    :param score: 
    :param attentionPeriod: 
    :return: Coordinae
    """
    print("wait for " + repr(img))
    while True:
        loc = elinkObj.matchScreen(img, score, attentionPeriod)
        dbg("max matching %3.2f" % loc[1])
        if None != loc[0]:
            dbg("matching at " + repr(loc[0]))
            break
        sleep(2)
    sleep((attentionPeriod + 500) / 1000)
    return Coordinate(loc[0])


def waitImagesOr(elinkObj, img_list, score=0.94, attentionPeriod=3000):
    print("wait for " + repr(img_list))
    while True:
        for img in img_list:
            found = elinkObj.matchScreen(img, score, attentionPeriod)
            dbg("max matching %3.2f" % found[1])
            if found[0]:
                dbg("matching at " + repr(found[0]))
                sleep((attentionPeriod + 500) / 1000)
                return [img, Coordinate(found[0])]
            sleep(2)


def clickPoint(elinkObj, p, delay=None):
    if delay is None:
        delay = 2

    info = elinkObj.info()
    dbg(info)
    w = info[2]
    h = info[3]
    x = int(p[REL][0] * w)
    y = int(p[REL][1] * h)
    x_abs = int(p[ABS][0])
    y_abs = int(p[ABS][1])
    dbg("x: " + str(x) + " y: " + str(y))
    dbg("x_abs: " + str(x_abs) + " y_abs: " + str(y_abs))
    elinkObj.sendMouse(0, x, y)
    sleep(1)
    elinkObj.sendMouse("LDOWN|CLICK", x, y)  # right mouse click at 100,100	(or 0x40)
    sleep(delay)


def clickbutton(elinkObj, img):
    imglocate = waitImage(elinkObj, img)
    if imglocate is None:
        return
    x = imglocate.x
    y = imglocate.y
    w = imglocate.w
    h = imglocate.h

    dbg("x y w h" + str(x) + str(y) + str(w) + str(h))
    center_x = int(x + w / 2)
    center_y = int(y + h / 2)
    dbg("center_x" + str(center_x) + "center_y " + str(center_y))
    elinkObj.sendMouse(PointerAct.MOVE, center_x, center_y)
    elinkObj.sendMouse("LDOWN|CLICK", center_x, center_y)  # right mouse click at 100,100	(or 0x40)


def waitKeyReady(elinkObj):
    print("waitKeyboard")
    key_state = -1

    while True:
        ev = elinkObj.getEvent()
        if ev.getIdCode() == 2:
            break

    ev = elinkObj.getEvent(2000)

    while True:
        if ev.getIdCode() == ElinkEvent.EVT_USB_KEY_SET_REPORT:
            key_state = ev.getData("Test") & 0x04
            break
        elif ev.getIdCode() == -1:
            break
        else:
            ev = elinkObj.getEvent(2000)

    if key_state == -1:
        key_state = 0
        elinkObj.sendKey("ScrollLock")

    count_send = 0
    while True:
        ev = elinkObj.getEvent(2000)
        if ev.getIdCode() == -1:
            count_send = count_send + 1
            if count_send < 3:
                elinkObj.sendKey("ScrollLock")
                continue
            else:
                print("Keyboard is not ready")
                assert 0
        elif ev.getIdCode() == ElinkEvent.EVT_USB_KEY_SET_REPORT:
            key_state2 = ev.getData("Test") & 0x04
        else:
            continue

        if key_state2 == key_state:
            print("Keyboard is ready")
            break
