from eLink.FileManager import FileManager
from eLink.elinkScriptUtils import *
from apscheduler.schedulers import background
from eLink.PowerMeter import *
import random
from datetime import datetime
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

try:
    import asyncio
except ImportError:
    import trollius as asyncio

default_elinkvkm = "10.42.0.101"
new_ramdom = random.choice(list(VncMode))
action = "None"

testScheduler = AsyncIOScheduler()
powermeter = PowerMeterController(name="test Power", port="COM13")

testScheduler.start()
count = 0


def getPowerMeterChannel():
    powermeter.sendGetDataChannel(InaChannel.INA1_ID, action)
    powermeter.sendGetDataChannel(InaChannel.INA2_ID, action)


def remove_and_upload_file(elinkObj):
    filemnger = FileManager(elinkObj)
    entry = filemnger.find_entry("opencv_world341.dll")
    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.FILE_TRANSFER, ActionState.ACTION_START)
    if entry:
        entry.show()
        filemnger.remove_file(entry)
        filemnger.upload_file("E:\project\elink-tutorial\opencv_world341.dll",
                              "/A:")
        entry = filemnger.find_entry("opencv_world341.dll")
        if entry:
            entry.show()
    else:
        filemnger.upload_file("E:\project\elink-tutorial\opencv_world341.dll",
                              "/A:")
        entry = filemnger.find_entry("opencv_world341.dll")
        if entry:
            entry.show()


async def vnc_switch_mode():
    global count
    global new_ramdom
    global action
    print("Test {}".format(count))
    print("Enable power")

    powermeter.sendSetSwChannel(InaChannel.INA1_ID, 0x01)
    powermeter.sendSetSwChannel(InaChannel.INA2_ID, 0x01)

    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.POWER_ON, ActionState.ACTION_START, testcount=count)

    WaitForELinkKVMReady(default_elinkvkm)
    elinkObj = elink.newConnection(default_elinkvkm)
    sleep(1)
    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.FILE_TRANSFER, ActionState.ACTION_FINISH, testcount=count)
    print("current mode {}".format(new_ramdom))
    if new_ramdom != VncMode.VNC_MODE_RGB:
        ramdom_mode = random.choice(list(VncMode))
        while new_ramdom == ramdom_mode:
            ramdom_mode = random.choice(list(VncMode))
    else:
        ramdom_mode = VncMode.VNC_MODE_RGB
    elinkObj.setVncMode(ramdom_mode)
    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.SWITCH_MODE_VNC, ActionState.ACTION_START,
                            detail="{}".format(ramdom_mode), testcount=count)
    new_ramdom = ramdom_mode
    sleep(5)
    elinkObj.close()
    sleep(1)
    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.SWITCH_MODE_VNC, ActionState.ACTION_FINISH,
                            detail="{}".format(ramdom_mode), testcount=count)
    powermeter.sendSetSwChannel(InaChannel.INA1_ID, 0x00)
    powermeter.sendSetSwChannel(InaChannel.INA2_ID, 0x00)
    powermeter.getPowerInfo(vnc_switch_mode.__name__, Action.POWER_OFF, ActionState.ACTION_FINISH, testcount=count)
    count += 1
    if count >= 20000:
        testScheduler.shutdown()
    # exit


if __name__ == '__main__':
    testScheduler.add_job(vnc_switch_mode, 'interval', seconds=6, id="test")
    # testScheduler.add_job(getPowerMeterChannel, 'interval', seconds=0.3, max_instances=3)
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
