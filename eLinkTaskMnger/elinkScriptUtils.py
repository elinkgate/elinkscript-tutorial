from __future__ import unicode_literals
from time import sleep

debug_enable = 0

ABS = 0
REL = 1


def dbg(msg):
    if debug_enable:
        print(msg)


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


def waitImage(elinkObj, img, score=0.9, attentionPeriod=3000):
    print("wait for " + repr(img))
    while True:
        loc = elinkObj.matchScreen(img, score, attentionPeriod)
        dbg("max matching %3.2f" % loc[1])
        if loc[0] != None:
            dbg("matching at " + repr(loc[0]))
            break
        sleep(2)
    sleep((attentionPeriod + 500) / 1000)
    return loc[0]


def waitImagesOr(elinkObj, img_list, score=0.94, attentionPeriod=3000):
    print("wait for " + repr(img_list))
    while True:
        for img in img_list:
            found = elinkObj.matchScreen(img, score, attentionPeriod)
            dbg("max matching %3.2f" % found[1])
            if found[0]:
                dbg("matching at " + repr(found[0]))
                sleep((attentionPeriod + 500) / 1000)
                return [img, found[0]]
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
    x = int(imglocate[0])
    y = int(imglocate[1])
    w = int(imglocate[2])
    h = int(imglocate[3])
    dbg("x y w h" + str(x) + str(y) + str(w) + str(h))
    center_x = int(x + w / 2)
    center_y = int(y + h / 2)
    dbg("center_x" + str(center_x) + "center_y " + str(center_y))
    elinkObj.sendMouse(0, center_x, center_y)
    sleep(1)
    elinkObj.sendMouse("LDOWN|CLICK", center_x, center_y)  # right mouse click at 100,100	(or 0x40)
    sleep(2)


def waitKeyReady(elinkObj):
    print("waitKeyboard")
    key_state = -1

    while True:
        ev = elinkObj.getEvent()
        if ev.getIdCode() == 2:
            break

    ev = elinkObj.getEvent(2000)

    while True:
        if ev.getIdCode() == 6:
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
        elif ev.getIdCode() == 6:
            key_state2 = ev.getData("Test") & 0x04
        else:
            continue

        if key_state2 == key_state:
            print("Keyboard is ready")
            break