"""
Demonstrates how to use the blocking scheduler to schedule a job that executes on 3 second
intervals.
"""
import os
import os
import sys
from datetime import datetime
from typing import List, Any

from apscheduler.schedulers.blocking import BlockingScheduler


# from elinkScriptUtils import *


class Location:
    def __init__(self, data: list):
        self.x = data[0]
        self.y = data[1]
        self.w = data[2]
        self.h = data[3]


class ScreenRecognize:
    @classmethod
    def waitimage(cls, vnc, img: str, score=0.9, attention_period=3000) -> Location:
        print("wait for " + repr(img))
        while True:
            loc = vnc.matchScreen(img, score, attention_period)
            if loc[0] is not None:
                break
            sleep(2)
        sleep((attentionPeriod + 500) / 1000)
        return Location(loc[0])


class RecognizeAction:
    def __init__(self, vnc=None, act=None, reg_img=""):
        self.__regImg = reg_img
        self.__action = act
        self.__vnc = vnc
        pass

    def set_recognize_img(self, img: str):
        self.__regImg = img

    def set_action(self, act):
        self.__action = act

    def set_vnc(self, vnc):
        self.__vnc = vnc

    def handle(self):
        """
        recognize image and take an action
        :return:
        """
        print("hello handle action")
        # ScreenRecognize.waitimage(self.__vnc, self.__regImg)
        self.__action()
        pass


class ELinkApp:
    __listact: List[Any]

    def __init__(self, vnc):
        self.__scheduler = BlockingScheduler()
        self.__listact = []

    def add_action(self, func):
        """
        add an action
        :type act: RecognizeAction
        :return:
        """
        return self.__scheduler.add_job(func, 'interval', seconds=1)

    def run(self):
        self.__scheduler.start()


# elinkapp = ELinkApp('hello')
#
#
# @elinkapp.add_action
# def tick():
#     print('Tick! The time is: %s' % datetime.now())
#
#
# if __name__ == '__main__':
#     elinkapp.run()
#