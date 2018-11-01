import csv
import threading
from enum import IntEnum, IntFlag
import sys

# sys.path.extend(['E:\\project\\elink-tutorial\\', 'E:/project/elink-tutorial/venv'])
# sys.path.extend(['E:\\project\\elink-tutorial\\DLLs', 'E:\\project\\elink-tutorial\\Lib'])
import serial
import time


class CmdType(IntEnum):
    RSP_TYPE = 0x00
    CMD_TYPE = 0x01


class FrameFormat(IntEnum):
    TWO_BYTE_LEN = 0x03
    ONE_BYTE_LEN = 0x02
    FRAME_END = 0x04


class SerialCmd(IntEnum):
    COMM_FW_VERSION = 0,
    COMM_TERMINAL_CMD = 1,
    COMM_PRINT = 2,
    COMM_SET_SWITCH = 3,
    COMM_GET_SWITCH = 4,
    COMM_SET_CHANNEL_FREQ = 5,
    COMM_SET_CHANNEL_RANGE = 6,
    COMM_GET_CHANNEL = 7,
    COMM_SET_CHANNEL_ALARM = 8,
    COMM_RESET_ALL = 9,
    COMM_SET_TIME = 10,
    COMM_SET_DATE = 11,
    COMM_GET_REFRESH_RATE = 12,
    COMM_GET_CHANNEL_FREQ = 13,
    COMM_GET_CHANNEL_STATUS = 14,


class ReceiveFrame(IntEnum):
    RECEIVED_START_FR = 0
    RECEIVED_LEN_BYTE_LOW = 1
    RECEIVED_LEN_BYTE_HIGH = 2
    RECEIVED_DATA = 3
    RECEIVED_CRC_H = 4
    RECEIVED_CRC_L = 5
    RECEIVED_END_FR = 6


class RespFrame(IntEnum):
    RESP_CHANNEL_DATA = 0
    RESP_COMM_RESP = 1
    RESP_CHANGE = 2
    RESP_FREQ_CHANGE = 3


class InaChannel(IntFlag):
    INA1_ID = 0x01
    INA2_ID = 0x02
    INA3_ID = 0x03
    INA4_ID = 0x04
    INA5_ID = 0x05
    INA6_ID = 0x06
    INA7_ID = 0x07
    INA8_ID = 0x08


class DataUnit(IntEnum):
    NODATA = 0
    DU_8 = 1
    DU_16 = 2
    DU_32 = 4


class PowerState(IntEnum):
    STATE_OFF = 0x00
    STATE_ON = 0x01


crc16_tab = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084,
             0x50a5, 0x60c6, 0x70e7, 0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad,
             0xe1ce, 0xf1ef, 0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7,
             0x62d6, 0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
             0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485, 0xa56a,
             0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d, 0x3653, 0x2672,
             0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4, 0xb75b, 0xa77a, 0x9719,
             0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc, 0x48c4, 0x58e5, 0x6886, 0x78a7,
             0x0840, 0x1861, 0x2802, 0x3823, 0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948,
             0x9969, 0xa90a, 0xb92b, 0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50,
             0x3a33, 0x2a12, 0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b,
             0xab1a, 0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
             0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49, 0x7e97,
             0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70, 0xff9f, 0xefbe,
             0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78, 0x9188, 0x81a9, 0xb1ca,
             0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f, 0x1080, 0x00a1, 0x30c2, 0x20e3,
             0x5004, 0x4025, 0x7046, 0x6067, 0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d,
             0xd31c, 0xe37f, 0xf35e, 0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214,
             0x6277, 0x7256, 0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c,
             0xc50d, 0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
             0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c, 0x26d3,
             0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634, 0xd94c, 0xc96d,
             0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab, 0x5844, 0x4865, 0x7806,
             0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3, 0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e,
             0x8bf9, 0x9bd8, 0xabbb, 0xbb9a, 0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1,
             0x1ad0, 0x2ab3, 0x3a92, 0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b,
             0x9de8, 0x8dc9, 0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0,
             0x0cc1, 0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
             0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0]


def crc16_calc(buf):
    cksum = 0
    length = len(buf)
    for i in range(length):
        cksum = crc16_tab[(((cksum >> 8) ^ buf[i]) & 0xFF)] ^ (cksum << 8);
        cksum = cksum & 0xFFFF
    return cksum;


class PowerMeterInfo:
    def __init__(self, packet):
        vol = packet[0] << 8 | packet[1]
        self.vol = vol
        del packet[:2]
        amp = packet[0] << 8 | packet[1]
        self.amp = amp
        del packet[:2]
        watt = packet[0] << 8 | packet[1]
        self.watt = watt


class PowerMeterController(threading.Thread):

    def __init__(self, name, port='COM3', logfile='powermeter.csv'):
        threading.Thread.__init__(self)
        self.threadLock = threading.Lock()
        self.name = name
        self.s = serial.Serial(port, 115200, timeout=5, write_timeout=5)
        self.read_state = ReceiveFrame.RECEIVED_START_FR
        self.logfile = logfile
        self.x_time = []
        self.y_volt = []
        self.y_amp = []
        self.y_watt = []
        self.act = "None"
        # self.fig = plt.figure()

    def drawGraph(self, channelId, powerInfo: PowerMeterInfo):

        # Create random data with numpy
        # Create a trace

        def UtcNow():
            epoch_time = int(time.time())
            return epoch_time

        self.x_time.append(UtcNow())
        self.y_watt.append(powerInfo.watt)
        self.y_volt.append(powerInfo.vol)
        self.y_amp.append(powerInfo.amp)
        plt.pause(0.5)
        plt.figure(1)
        plt.subplot(311)
        plt.plot(self.x_time, self.y_watt)
        plt.subplot(312)
        plt.plot(self.x_time, self.y_amp)
        plt.subplot(313)
        plt.plot(self.x_time, self.y_volt)

        # plt.show(block=False)

        # print("{}".format(plot_url))
        # if channelId == InaChannel.INA1_ID:
        #     trace1 = go.Scatter(
        #         x=[].append(UtcNow()),
        #         y=[].append(powerInfo.vol))
        # else:
        #     trace2 = go.Scatter(x=UtcNow(), y=powerInfo.vol)
        #
        # data = [trace1]

        # py.iplot(data, filename='basic-line', fileopt='extend')

    def loggingPowerMeter(self, channelId: InaChannel, power: PowerMeterInfo):
        """

        :type channelId: InaChannel
        """
        with open(self.logfile, mode='a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([int(channelId), power.vol, power.amp, power.watt, self.act])
            # self.drawGraph(channelId, power)

    def run(self):
        print("Starting thread")
        # Get lock to synchronize threads
        while True:
            self.threadLock.acquire()
            self.processData()
            self.threadLock.release()

    def start(self):
        print("start something here")
        super().start()

    def stop(self):
        """

        """
        print('Stop thread')
        threading.join(10)

    def sendCommand(self, cmdType, cmdId, channelId, buf=bytearray()):
        """
        ||cmdType||<ChannelID <<4 ><cmdId>||<Length>||<Buffer Data>||
        Command type
        Channel ID (4bit high)| command Id (4 bitlow)
        Command length
        Buffer data
        :param cmdType:
        :param cmdId:
        :param channelId:
        :param buf:
        """
        packet = bytearray()
        packet.append(cmdType)
        cmdData = int(cmdId << 4) | int(channelId)
        packet.append(cmdData)
        length = len(buf)
        packet.append(length)
        packet += buf
        self.threadLock.acquire()
        self.sendPacket(packet)
        self.threadLock.release()

    def sendPacket(self, packet):
        """
        package format
        <package_len_type>|<package length><package data><crc><frame_end>
        package len type : One_byte_len or tow_byte_len
        length of package
        package_data : Command data
        crc16 : 2 bybe crc 16
        frame end

        :param packet:
        """
        buf = bytearray()
        length = len(packet)
        if length < 256:
            buf.append(FrameFormat.ONE_BYTE_LEN)
            buf.append(length)
        else:
            buf.append(FrameFormat.TWO_BYTE_LEN)
            buf.append(length / 2)
        buf += packet
        crc16 = crc16_calc(packet)
        b = (crc16 >> 8) & 0xFF
        buf.append(b)
        b = crc16 & 0xFF
        buf.append(b)
        buf.append(FrameFormat.FRAME_END)
        self.s.write(buf)
        self.s.flush()

    def sendGetFirmware(self):
        """
        get Firmware version

        """
        self.sendCommand(0x01, SerialCmd.COMM_FW_VERSION, 0)

    def sendGetChannelStatus(self, InaChannelId):
        """

        :param InaChannelId:
        """
        self.sendCommand(0x01, SerialCmd.COMM_GET_CHANNEL_STATUS, InaChannelId)

    def sendGetChannelSampleTime(self, InaChannelId):
        """
        fr.pkgType  = 0;
        fr.pkgId    = 0;
        fr.pkgType_u.cmd = 0x01;
        fr.pkgType_u.dataUnit = 0;
        fr.pkgType_u.dynLen = 0;
        fr.pkgType_u.sttReq = 0;

        fr.pkgId_u.cmdId = (char)COMM_GET_CHANNEL;
        fr.pkgId_u.channelId = (char)chId;
        fr.len = 0;
        :param InaChannelId:
        """
        self.sendCommand(0x01, SerialCmd.COMM_GET_CHANNEL, InaChannelId)

    def sendSetChannelSampleTime(self, InaChannelId, ctIndex, avgIndex):
        """

        :param InaChannelId:
        :param ctIndex:
        :param avgIndex:
        """
        arg = bytearray([ctIndex, avgIndex])
        self.sendCommand(0x01 | (DataUnit.DU_8 << 2), SerialCmd.COMM_SET_CHANNEL_FREQ, InaChannelId, arg)

    def sendGetDataChannel(self, InaChannelId, act="None"):
        """

        :param InaChannelId:
        """
        self.sendCommand(0x00, RespFrame.RESP_CHANNEL_DATA, InaChannelId)
        self.act = act

    def sendSetSwChannel(self, ChannelId, state):
        arg = bytearray([state])
        self.sendCommand(0x01 | (DataUnit.DU_8 << 2), SerialCmd.COMM_SET_SWITCH, ChannelId, arg)

    def sendGetSwChannel(self, ChannelId):
        self.sendCommand(0x01, SerialCmd.COMM_GET_SWITCH, ChannelId)

    def processChannelData(self, chanelId, channel: PowerMeterInfo):
        print("chanelId %d vol=%d amp=%d watt=%d" % (chanelId, channel.vol, channel.amp, channel.watt))
        # self.loggingPowerMeter(chanelId, channel)

    def processFwVersion(self, major, minor):
        print("firmware major=%d minor=%d" % (major, minor))

    def getCmdId(self, pkgId):
        return (pkgId & 0xf0) >> 4

    def getChannelId(self, pkgId):
        return pkgId & 0x0f

    def processPacket(self):
        packet = self.packet
        datUnit = (packet[0] & 0x06) >> 1
        pktLen = packet[2] * datUnit
        pktType = packet[0] & 0x01
        pktCmd = packet[1]
        del packet[:3]
        if pktLen != len(packet):
            print("invalid packet")
            return
        cmdId = self.getCmdId(pktCmd)
        if pktType == CmdType.CMD_TYPE:
            if cmdId == SerialCmd.COMM_FW_VERSION:
                fw_major = packet[0]
                fw_minor = packet[1]
                self.processFwVersion(fw_major, fw_minor)
            elif cmdId == SerialCmd.COMM_GET_CHANNEL:
                print("Get Serial command data COMM_GET_CHANNEL {}".format(packet))
            elif cmdId == SerialCmd.COMM_GET_CHANNEL_FREQ:
                print("get COMM_GET_CHANNEL_FREQ {}".format(packet))
            elif cmdId == SerialCmd.COMM_GET_CHANNEL:
                print("Get COMM_GET_CHANNEL: {} ".format(packet))
            elif cmdId == SerialCmd.COMM_GET_CHANNEL_STATUS:
                print("Get COMM_GET_CHANNEL_STATUS: {}".format(packet))
        else:
            if cmdId == RespFrame.RESP_CHANNEL_DATA:
                chanelId = self.getChannelId(pktCmd)
                dataInfo = PowerMeterInfo(packet)
                self.processChannelData(chanelId, dataInfo)
            else:
                print("unknown packet", packet)

    def processData(self):
        while self.s.in_waiting > 0:
            buf = self.s.read(1)
            if len(buf) > 0:
                if self.read_state == ReceiveFrame.RECEIVED_START_FR:
                    if buf[0] == FrameFormat.ONE_BYTE_LEN:
                        self.read_state = ReceiveFrame.RECEIVED_LEN_BYTE_LOW
                    elif buf[0] == FrameFormat.TWO_BYTE_LEN:
                        self.read_state = ReceiveFrame.RECEIVED_LEN_BYTE_HIGH
                    else:
                        raise Exception("invalid start packet")
                elif self.read_state == ReceiveFrame.RECEIVED_LEN_BYTE_HIGH:
                    raise Exception("not supported high")
                elif self.read_state == ReceiveFrame.RECEIVED_LEN_BYTE_LOW:
                    self.num_data = buf[0]
                    self.read_state = ReceiveFrame.RECEIVED_DATA
                    self.packet = []
                elif self.read_state == ReceiveFrame.RECEIVED_DATA:
                    self.packet.append(buf[0])
                    self.num_data -= 1
                    if self.num_data == 0:
                        self.read_state = ReceiveFrame.RECEIVED_CRC_H
                        self.crc16_read = 0
                elif self.read_state == ReceiveFrame.RECEIVED_CRC_H:
                    self.crc16_read = buf[0] << 8
                    self.read_state = ReceiveFrame.RECEIVED_CRC_L
                elif self.read_state == ReceiveFrame.RECEIVED_CRC_L:
                    self.crc16_read |= buf[0]
                    self.read_state = ReceiveFrame.RECEIVED_END_FR
                elif self.read_state == ReceiveFrame.RECEIVED_END_FR:
                    if (buf[0] == FrameFormat.FRAME_END) and (self.crc16_read == crc16_calc(self.packet)):
                        self.processPacket()
                        self.read_state = ReceiveFrame.RECEIVED_START_FR
                    else:
                        raise Exception("data is invalid")
