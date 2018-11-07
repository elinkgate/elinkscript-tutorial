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

default_elinkvkm = "10.42.0.2"
new_ramdom = random.choice(list(VncMode))
action = "None"

testScheduler = AsyncIOScheduler()
powermeter = PowerMeterController(name="test Power", port="COM13")
# elinkObj = elink.newConnection(default_elinkvkm)
# powermeter.sendSetSwChannel(InaChannel.INA2_ID, int(1))
# powermeter.sendSetSwChannel(InaChannel.INA1_ID, int(0))
testScheduler.start()
powermeter.start()
state_channel1 = 1
state_channel2 = 0


def getPowerMeterChannel1():
    # if state_channel1:
    # print("channel 1 enable: get channel data")
    powermeter.sendGetDataChannel(InaChannel.INA1_ID, action)


def getPowerMeterChenel2():
    # if state_channel2:
    # print("chanel 2 enable: get channel data")
    powermeter.sendGetDataChannel(InaChannel.INA2_ID, action)


def test_switch_power():
    global state_channel1
    global state_channel2

    state_channel = random.choice(list(PowerState))
    # while state_channel == state_channel1:
    #     state_channel = random.choice(list(PowerState))
    powermeter.sendSetSwChannel(InaChannel.INA1_ID, int(state_channel))
    state_channel1 = state_channel
    print("set channel 1 state: {}".format(state_channel1))

    state_channel = random.choice(list(PowerState))
    # while state_channel == state_channel2:
    #     state_channel = random.choice(list(PowerState))
    powermeter.sendSetSwChannel(InaChannel.INA2_ID, int(state_channel))
    print("set channel 2 state: {}".format(state_channel))
    state_channel2 = state_channel


if __name__ == '__main__':

    testScheduler.add_job(getPowerMeterChannel1, 'interval', seconds=0.5, max_instances=1)
    testScheduler.add_job(getPowerMeterChenel2, 'interval', seconds=0.5, max_instances=1)
    testScheduler.add_job(test_switch_power, 'interval', seconds=10, max_instances=1)
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
