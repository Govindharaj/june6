#from cli.app import CommandLineApp
from read.read import read as readerprs
from readuts.readuts import readuts as readeruts
from readutsdumb.readutsdumb import readutsdumb as readerutsdumb
from config.config import config as setting
import serial
import sys


class Readttys:
    checkDataSize = 20

    @staticmethod
    def main():
        c = setting()
        debug = c.get('parser', 'debug')
        testDataFile = c.get('parser', 'test_data_file')
        dataType = c.get('default', 'counter_type')
        dataType = dataType.lower()

        if 'prs' != dataType and 'uts' != dataType and 'uts-dumb' != dataType and 'uts-db' != dataType:
            dataType = Readttys.__detectionData(debug, testDataFile)

        if 'prs' == dataType:
            r = readerprs(c.get('parser', 'db_path'), dataType)
            print "PRS"
        elif 'uts-dumb' == dataType or 'uts-db' == dataType:
            r = readerutsdumb(c.get('parser', 'db_path'), dataType)
            print "UTS-Dumb"
        elif 'uts' == dataType:
            r = readeruts(c.get('parser', 'db_path'), dataType)
            print "UTS"

        if 0 == int(debug):
            r.readSerialport()
        else:
            r.readSampleFile(testDataFile)


    @staticmethod
    def __detectionData(debug, sampleFile):
        dataType = 'prs'
        packet = ''
        try:
            if 0 == int(debug):
                c = setting()
                serialPortName = c.get('parser', 'serial_port_name')
                if serialPortName == '0':
                    serialPortName = 0
                fh = serial.Serial(serialPortName)
            else:
                fh = open(sampleFile)
                # Getting the sub string of serial data
            read = True
            checkPacketCount = 0
            while read:
                start = fh.read(1)
                if start.strip() != "":
                    data = Readttys.__byteToHex(start)

                    #print data
                    # Check the uts unique code in getting data and decide what it is
                    if '^$' in packet:
                        #print packet
                        dataType = 'uts'
                        read = False
                    elif data == "1B":
                        packetData = Readttys.__byteToHex(packet)
                        packet = ""
                        checkPacketCount += 1
                        if '1B5B306D' == packetData:
                            dataType = 'uts-dumb'
                            read = False

                    if Readttys.checkDataSize == checkPacketCount:
                        read = False
                    packet += start
            fh.close()
        except BaseException as e:
            print 'Error in reading the data :'
            print e
            sys.exit(0)

        return dataType

    ##
    # @brief   Convert to byte to hex
    # @param   Byte byteStr
    # @return  String
    @staticmethod
    def __byteToHex(byteStr):
        return ''.join(["%02X" % ord(x) for x in byteStr]).strip()


if __name__ == "__main__":
    Readttys.main()