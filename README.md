# eLink Automation Script Tutorial 

### Capture screen 

Các bước thực hiện để record screen bao gồm: 

1. Click Pause button `||` trên thanh tools bar 
2. nhấn và giữ phím "LCtrl" kết hợp với việc nhấp chuột và kéo vùng screen cần nhận diện 
3. eLinkViewer sẽ khởi tạo 1 file ảnh tmp_<xx>.png ở thư mục chạy eLinkViewer 

![capture screen](https://lh3.googleusercontent.com/-s-0ObAxnfuY/W4YQ251OwTI/AAAAAAAAAIU/YhrmlqYxlLEcRC2EDZIdUf0t01VS6xzvgCHMYCw/s0/2018-08-29_10-19-49.gif)



### eLink utility API

```python
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
```

### Tutorial 

#### Hello-World 

Dưới đây là 1 tutorial đơn giản hello-world. Sử dụng eLink Script để thực hiện 1 thao tác đơn giản là detect Notepad icon sau đó click vào icon, chọn menu Maximum và gửi chuổi kí tự "Hello World" 

```python
from elinkScriptUtils import *


def getCurrentConnection():
    gConn = elink.getConnection()
    if len(gConn) != 0:
        return gConn[0]
    return None


def main():
    elinkObj = getCurrentConnection()
    if elinkObj is None:
        elinkObj = elink.newConnection("10.42.0.2")
    elinkObj.setVncMode("MODE_VNC_RGB")
    elinkObj.setUsbMode("USB_MODE_KEY|USB_MODE_VNC_HID|USB_MODE_MOUSE_ABS", 0)
    elinkObj.setKeyMode("KEY_INTF_HID")
    elinkObj.setMouseMode("POINT_INTF_HID_ABS")
    waitImage(elinkObj, "hello-world/notepad_icon.png")
    clickbutton(elinkObj, "hello-world/notepad_icon.png")
    clickbutton(elinkObj, "hello-world/click_maximum.png")
    elinkObj.sendString("Hello World")
    pass


if __name__ == "__main__":
    main()
```

![Hello-world](https://lh3.googleusercontent.com/-cSSV8M3hm5w/W4ZacBCdsvI/AAAAAAAAAJY/ogeJLi1ihigTYPXOA-JTFm2XCp1Cm0IxwCHMYCw/s0/2018-08-29_15-31-05.gif)

#### IPMI reset command

Connect to IPMI server and use IPMI command to remote control server 

```python
from time import sleep
from elinkScriptUtils import *
elinkObj = elink.newConnection("10.42.0.2")
elinkObj.setVncMode("MODE_VNC_RGB")
elinkObj.setUsbMode("USB_MODE_KEY|USB_MODE_VNC_HID|USB_MODE_MOUSE_ABS", 0)
elinkObj.setKeyMode("KEY_INTF_HID")
elinkObj.setMouseMode("POINT_INTF_HID_ABS")
sleep(4)
print("Connect to IPMI 10.42.0.105 usr/pass root/root")
elinkObj.ipmiConnect("10.42.0.105", "root", "root")
status_ret = elinkObj.ipmiStatus()
print("{}".format(status_ret))
print("Reset Server by using IPMI command reset option 0")
elinkObj.ipmiReset(0)
sleep(5)
print("Wait for Bios setup Configurator")
waitImage(elinkObj, "Ipmi/BiosSetupConfiguration.png")
print("Reset Server to Unified Server Configurator by using IPMI command reset")
elinkObj.ipmiReset(1)
print("Wait for Unified Server Configurator")
waitImage(elinkObj, "Ipmi/UnifiedServerConfigurator.png")

```


![IPMI Reset](https://lh3.googleusercontent.com/-ueC6sWDyano/W4Z-CBXw9UI/AAAAAAAAAJw/ozmlyXDH2_Mw9rrN1SkTFHP3J9wSKFrSwCHMYCw/s0/2018-08-29_18-02-06.gif)

