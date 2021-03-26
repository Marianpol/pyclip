#Embedded file name: /build/PyCLIP/android/app/mod_elm.py
import mod_globals
import sys
import re
import time
import string
import threading
import socket
from datetime import datetime
from collections import OrderedDict
from kivy.utils import platform
if platform != 'android':
    import serial
    from serial.tools import list_ports
else:
    from jnius import autoclass
    mod_globals.os = 'android'
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    UUID = autoclass('java.util.UUID')
DevList = ['27',
 '2E',
 '30',
 '31',
 '32',
 '34',
 '35',
 '36',
 '37',
 '3B',
 '3D']
AllowedList = ['12',
 '17',
 '19',
 '1A',
 '21',
 '22',
 '23']
MaxBurst = 7
snat = {'01': '760',
 '02': '724',
 '04': '762',
 '07': '771',
 '08': '778',
 '0D': '775',
 '0E': '76E',
 '0F': '770',
 '13': '732',
 '1B': '7AC',
 '1C': '76B',
 '1E': '768',
 '23': '773',
 '24': '77D',
 '26': '765',
 '27': '76D',
 '29': '764',
 '2A': '76F',
 '2C': '772',
 '2E': '7BC',
 '32': '776',
 '3A': '7D2',
 '40': '727',
 '4D': '7BD',
 '50': '738',
 '51': '763',
 '57': '767',
 '59': '734',
 '62': '7DD',
 '66': '739',
 '67': '793',
 '68': '77E',
 '6B': '7B5',
 '6E': '7E9',
 '77': '7DA',
 '79': '7EA',
 '7A': '7E8',
 '7C': '77C',
 '86': '7A2',
 '87': '7A0',
 '93': '7BB',
 '95': '7EC',
 'A5': '725',
 'A6': '726',
 'A7': '733',
 'A8': '7B6',
 'C0': '7B9',
 'D1': '7EE',
 'F7': '736',
 'F8': '737',
 'FA': '77B',
 'FD': '76F',
 'FE': '76C',
 'FF': '7D0',
 '11': '7C3',
 'A1': '76C',
 '58': '767',
 '2B': '735',
 '11': '7C9',
 '28': '7D7',
 'E8': '5C4',
 '2F': '76C',
 '64': '7D5',
 'D3': '7EE',
 'DF': '5C1',
 '61': '7BA',
 '46': '7CF',
 'EA': '4B3',
 'ED': '704',
 'EC': '5B7',
 'E9': '762',
 '25': '700',
 'E2': '5BB',
 '97': '7C8',
 'DE': '69C',
 '63': '73E',
 'E6': '484',
 'EB': '5B8',
 '78': '7BD',
 '5B': '7A5',
 '81': '761',
 '06': '791',
 'E1': '5BA',
 '1A': '731',
 'E3': '4A7',
 '91': '7ED',
 '09': '7EB',
 'E7': '7EC',
 'E4': '757',
 'E0': '58B',
 '82': '7AD',
 '47': '7A8',
 'D2': '18DAF1D2',
 '60': '18DAF160',
 'D0': '18DAF1D0',
 'DA': '18DAF1DA',
 '2D': '18DAF12D',
 '41': '18DAF1D2'}
dnat = {'01': '740',
 '02': '704',
 '04': '742',
 '07': '751',
 '08': '758',
 '0D': '755',
 '0E': '74E',
 '0F': '750',
 '13': '712',
 '1B': '7A4',
 '1C': '74B',
 '1E': '748',
 '23': '753',
 '24': '75D',
 '26': '745',
 '27': '74D',
 '29': '744',
 '2A': '74F',
 '2C': '752',
 '2E': '79C',
 '32': '756',
 '3A': '7D6',
 '40': '707',
 '4D': '79D',
 '50': '718',
 '51': '743',
 '57': '747',
 '59': '714',
 '62': '7DC',
 '66': '719',
 '67': '792',
 '68': '75A',
 '6B': '795',
 '6E': '7E1',
 '77': '7CA',
 '79': '7E2',
 '7A': '7E0',
 '7C': '75C',
 '86': '782',
 '87': '780',
 '93': '79B',
 '95': '7E4',
 'A5': '705',
 'A6': '706',
 'A7': '713',
 'A8': '796',
 'C0': '799',
 'D1': '7E6',
 'F7': '716',
 'F8': '717',
 'FA': '75B',
 'FD': '74F',
 'FE': '74C',
 'FF': '7D0',
 '11': '7C9',
 'A1': '74C',
 '58': '747',
 '2B': '723',
 '11': '7C3',
 '28': '78A',
 'E8': '644',
 'EC': '637',
 '2F': '74C',
 '64': '7D4',
 'D3': '7E6',
 'DF': '641',
 '61': '7B7',
 '46': '7CD',
 'EA': '79A',
 'ED': '714',
 'E9': '742',
 '25': '70C',
 'E2': '63B',
 '97': '7D8',
 'DE': '6BC',
 '63': '73D',
 'E3': '73A',
 'E6': '622',
 'EB': '638',
 '78': '79D',
 '5B': '785',
 '81': '73F',
 '06': '790',
 'E1': '63A',
 '1A': '711',
 '91': '7E5',
 '09': '7E3',
 'E7': '7E4',
 'E4': '74F',
 'E0': '60B',
 '82': '7AA',
 '47': '788',
 'D2': '18DAD2F1',
 '60': '18DA60F1',
 'D0': '18DAD0F1',
 '2D': '18DA2DF1',
 'DA': '18DADAF1',
 '41': '18DAD2F1'}
negrsp = {'10': 'NR: General Reject',
 '11': 'NR: Service Not Supported',
 '12': 'NR: SubFunction Not Supported',
 '13': 'NR: Incorrect Message Length Or Invalid Format',
 '21': 'NR: Busy Repeat Request',
 '22': 'NR: Conditions Not Correct Or Request Sequence Error',
 '23': 'NR: Routine Not Complete',
 '24': 'NR: Request Sequence Error',
 '31': 'NR: Request Out Of Range',
 '33': 'NR: Security Access Denied- Security Access Requested  ',
 '35': 'NR: Invalid Key',
 '36': 'NR: Exceed Number Of Attempts',
 '37': 'NR: Required Time Delay Not Expired',
 '40': 'NR: Download not accepted',
 '41': 'NR: Improper download type',
 '42': 'NR: Can not download to specified address',
 '43': 'NR: Can not download number of bytes requested',
 '50': 'NR: Upload not accepted',
 '51': 'NR: Improper upload type',
 '52': 'NR: Can not upload from specified address',
 '53': 'NR: Can not upload number of bytes requested',
 '70': 'NR: Upload Download NotAccepted',
 '71': 'NR: Transfer Data Suspended',
 '72': 'NR: General Programming Failure',
 '73': 'NR: Wrong Block Sequence Counter',
 '74': 'NR: Illegal Address In Block Transfer',
 '75': 'NR: Illegal Byte Count In Block Transfer',
 '76': 'NR: Illegal Block Transfer Type',
 '77': 'NR: Block Transfer Data Checksum Error',
 '78': 'NR: Request Correctly Received-Response Pending',
 '79': 'NR: Incorrect ByteCount During Block Transfer',
 '7E': 'NR: SubFunction Not Supported In Active Session',
 '7F': 'NR: Service Not Supported In Active Session',
 '80': 'NR: Service Not Supported In Active Diagnostic Mode',
 '81': 'NR: Rpm Too High',
 '82': 'NR: Rpm Too Low',
 '83': 'NR: Engine Is Running',
 '84': 'NR: Engine Is Not Running',
 '85': 'NR: Engine RunTime TooLow',
 '86': 'NR: Temperature Too High',
 '87': 'NR: Temperature Too Low',
 '88': 'NR: Vehicle Speed Too High',
 '89': 'NR: Vehicle Speed Too Low',
 '8A': 'NR: Throttle/Pedal Too High',
 '8B': 'NR: Throttle/Pedal Too Low',
 '8C': 'NR: Transmission Range In Neutral',
 '8D': 'NR: Transmission Range In Gear',
 '8F': 'NR: Brake Switch(es)NotClosed (brake pedal not pressed or not applied)',
 '90': 'NR: Shifter Lever Not In Park ',
 '91': 'NR: Torque Converter Clutch Locked',
 '92': 'NR: Voltage Too High',
 '93': 'NR: Voltage Too Low'}

def get_bt_socket_stream():
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    for device in paired_devices:
        if mod_globals.bt_dev and mod_globals.bt_dev != device.getName():
            continue
        socket = device.createRfcommSocketToServiceRecord(UUID.fromString('00001101-0000-1000-8000-00805F9B34FB'))
        #print 'python PYREN : trying to connect %s' % device.getName()
        try:
            socket.connect()
            recv_stream = socket.getInputStream()
            send_stream = socket.getOutputStream()
            return (recv_stream, send_stream)
        except:
            ##print 'python PYREN : cannot connect %s' % device.getName()
            pass


def get_devices():
    devs = []
    if mod_globals.os != 'android':
        iterator = sorted(list(list_ports.comports()))
        for port, desc, hwid in iterator:
            devs.append(port)

        return devs
    paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    for device in paired_devices:
        deviceName = device.getName()
        if deviceName:
            devs.append(deviceName)

    return devs


class Port:
    portType = 0
    ipaddr = '192.168.0.10'
    tcpprt = 35000
    portName = ''
    portTimeout = 5
    droid = None
    btcid = None
    hdr = None

    def __init__(self, portName, speed, portTimeout):
        self.portTimeout = portTimeout
        portName = portName.strip()
        if re.match('^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\:\\d{1,5}$', portName):
            import socket
            self.ipaddr, self.tcpprt = portName.split(':')
            self.tcpprt = int(self.tcpprt)
            self.portType = 1
            self.hdr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.hdr.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.hdr.connect((self.ipaddr, self.tcpprt))
            self.hdr.setblocking(True)
        elif mod_globals.os == 'android':
            self.portType = 2
            self.recv_stream, self.send_stream = get_bt_socket_stream()
        else:
            self.portName = portName
            self.portType = 0
            try:
                self.hdr = serial.Serial(self.portName, baudrate=speed, timeout=portTimeout)
            except:
                #print 'ELM not connected or wrong COM port defined.'
                iterator = sorted(list(list_ports.comports()))
                #print ''
                #print 'Available COM ports:'
                # for port, desc, hwid in iterator:
                    #print '%-30s \n\tdesc: %s \n\thwid: %s' % (port, desc.decode('windows-1251'), hwid)

                #print ''
                mod_globals.opt_demo = True
                exit(2)

            if mod_globals.opt_speed == 38400 and mod_globals.opt_rate != mod_globals.opt_speed:
                self.check_elm()

    def reinit(self):
        if self.portType != 1: return
        self.hdr.close()
        self.hdr = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        self.hdr.setsockopt (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.hdr.connect ((self.ipaddr, self.tcpprt))
        self.hdr.setblocking (True)
        
        self.write("AT\r")
        self.expect(">",1)

    def read(self):
        try:
            byte = ''
            if self.portType == 1:
                try:
                    byte = self.hdr.recv(1)
                except:
                    pass

            elif self.portType == 2:
                if self.recv_stream.available():
                    byte = chr(self.recv_stream.read())
            elif self.hdr.inWaiting():
                byte = self.hdr.read()
        except:
            #print '*' * 40
            #print '*       Connection to ELM was lost'
            mod_globals.opt_demo = True
            exit(2)

        return byte

    def write(self, data):
        try:
            if self.portType == 1:
                try:
                    rcv_bytes = self.hdr.sendall(data)
                except:
                    self.reinit()
                    rcv_bytes = self.hdr.sendall(data)
                return rcv_bytes
            if self.portType == 2:
                self.send_stream.write(data)
                self.send_stream.flush()
                return len(data)
            return self.hdr.write(data)
        except:
            #print '*' * 40
            #print '*       Connection to ELM was lost'
            mod_globals.opt_demo = True
            exit(2)

    def expect(self, pattern, time_out = 1):
        tb = time.time()
        self.buff = ''
        try:
            while True:
                if not mod_globals.opt_demo:
                    byte = self.read()
                else:
                    byte = '>'
                if byte == '\r':
                    byte = '\n'
                self.buff += byte
                tc = time.time()
                if pattern in self.buff:
                    return self.buff
                if tc - tb > time_out:
                    return self.buff + 'TIMEOUT'

        except:
            pass

        return ''

    def check_elm(self):
        self.hdr.timeout = 2
        for s in [38400,
         115200,
         230400,
         57600,
         9600,
         500000]:
            #print '\r\t\t\t\t\rChecking port speed:', s,
            sys.stdout.flush()
            self.hdr.baudrate = s
            self.hdr.flushInput()
            self.write('\r')
            tb = time.time()
            self.buff = ''
            while True:
                if not mod_globals.opt_demo:
                    byte = self.read()
                else:
                    byte = '>'
                self.buff += byte
                tc = time.time()
                if '>' in self.buff:
                    mod_globals.opt_speed = s
                    #print '\nStart COM speed: ', s
                    self.hdr.timeout = self.portTimeout
                    return
                if tc - tb > 1:
                    break

        #print '\nELM not responding'
        sys.exit()

    def soft_boudrate(self, boudrate):
        if mod_globals.opt_demo:
            return
        if self.portType == 1:
            #print 'ERROR - wifi do not support changing boud rate'
            return
        #print 'Changing baud rate to:', boudrate,
        if boudrate == 38400:
            self.write('at brd 68\r')
        elif boudrate == 57600:
            self.write('at brd 45\r')
        elif boudrate == 115200:
            self.write('at brd 23\r')
        elif boudrate == 230400:
            self.write('at brd 11\r')
        elif boudrate == 500000:
            self.write('at brd 8\r')
        tb = time.time()
        self.buff = ''
        while True:
            if not mod_globals.opt_demo:
                byte = self.read()
            else:
                byte = 'OK'
            if byte == '\r' or byte == '\n':
                self.buff = ''
                continue
            self.buff += byte
            tc = time.time()
            if 'OK' in self.buff:
                break
            if tc - tb > 1:
                #print 'ERROR - command not supported'
                sys.exit()

        self.hdr.timeout = 1
        if boudrate == 38400:
            self.hdr.baudrate = 38400
        elif boudrate == 57600:
            self.hdr.baudrate = 57600
        elif boudrate == 115200:
            self.hdr.baudrate = 115200
        elif boudrate == 230400:
            self.hdr.baudrate = 230400
        elif boudrate == 500000:
            self.hdr.baudrate = 500000
        tb = time.time()
        self.buff = ''
        while True:
            if not mod_globals.opt_demo:
                byte = self.read()
            else:
                byte = 'ELM'
            if byte == '\r' or byte == '\n':
                self.buff = ''
                continue
            self.buff += byte
            tc = time.time()
            if 'ELM' in self.buff:
                break
            if tc - tb > 1:
                #print "ERROR - rate not supported. Let's go back."
                self.hdr.timeout = self.portTimeout
                self.hdr.baudrate = mod_globals.opt_speed
                return

        self.write('\r')
        tb = time.time()
        self.buff = ''
        while True:
            if not mod_globals.opt_demo:
                byte = self.read()
            else:
                byte = '>'
            if byte == '\r' or byte == '\n':
                self.buff = ''
                continue
            self.buff += byte
            tc = time.time()
            if '>' in self.buff:
                break
            if tc - tb > 1:
                #print "ERROR - something went wrong. Let's back."
                self.hdr.timeout = self.portTimeout
                self.hdr.baudrate = mod_globals.opt_speed
                return

        #print 'OK'


class ELM:
    port = 0
    lf = 0
    vf = 0
    keepAlive = 4
    busLoad = 0
    srvsDelay = 0
    lastCMDtime = 0
    portTimeout = 5
    elmTimeout = 0
    performanceModeLevel = 1
    error_frame = 0
    error_bufferfull = 0
    error_question = 0
    error_nodata = 0
    error_timeout = 0
    error_rx = 0
    error_can = 0
    response_time = 0
    buff = ''
    currentprotocol = ''
    currentsubprotocol = ''
    currentaddress = ''
    startSession = ''
    lastinitrsp = ''
    currentScreenDataIds = []
    rsp_cache = OrderedDict()
    l1_cache = {}
    notSupportedCommands = {}
    ecudump = {}
    ATR1 = True
    ATCFC0 = False
    supportedCommands = 0
    unsupportedCommands = 0
    portName = ''
    lastMessage = ''

    def __init__(self, portName, speed, log, startSession = '10C0'):
        self.portName = portName
        if not mod_globals.opt_demo:
            self.port = Port(portName, speed, self.portTimeout)
        if len(mod_globals.opt_log) > 0:
            self.lf = open(mod_globals.log_dir + 'elm_' + mod_globals.opt_log, 'at')
            self.vf = open(mod_globals.log_dir + 'ecu_' + mod_globals.opt_log, 'at')
        if mod_globals.opt_debug and mod_globals.debug_file == None:
            mod_globals.debug_file = open(mod_globals.log_dir + 'debug.txt', 'at')
        self.lastCMDtime = 0
        self.ATCFC0 = mod_globals.opt_cfc0

    def __del__(self):
        if not mod_globals.opt_demo:
            #print '*' * 40
            #print '*       RESETTING ELM'
            self.port.write('atz\r')
        #print '*' * 40
        #print '* '
        #print '*       ERRORS STATISTIC'
        #print '* '
        #print '* error_frame      = ', self.error_frame
        #print '* error_bufferfull = ', self.error_bufferfull
        #print '* error_question   = ', self.error_question
        #print '* error_nodata     = ', self.error_nodata
        #print '* error_timeout    = ', self.error_timeout
        #print '* error_rx         = ', self.error_rx
        #print '* error_can        = ', self.error_can
        #print '*'
        #print '*       RESPONSE TIME (Average)'
        #print '* '
        #print '* response_time    = ', '{0:.3f}'.format(self.response_time)
        #print '* '
        #print '*' * 40
        #print self.lastMessage

    def clear_cache(self):
        self.rsp_cache = OrderedDict()

    def setDump(self, ecudump):
        self.ecudump = ecudump

    def request(self, req, positive = '', cache = True, serviceDelay = '0'):
        if mod_globals.opt_demo and req in self.ecudump.keys():
            return self.ecudump[req]
        if cache and req in self.rsp_cache.keys():
            return self.rsp_cache[req]
        rsp = self.cmd(req, int(serviceDelay))
        res = ''
        if self.currentprotocol != 'can':
            rsp_split = rsp.split('\n')[1:]
            for s in rsp_split:
                if '>' not in s and len(s.strip()):
                    res += s.strip() + ' '

        else:
            for s in rsp.split('\n'):
                if ':' in s:
                    res += s[2:].strip() + ' '
                elif s.replace(' ', '').startswith(positive.replace(' ', '')):
                    res += s.strip() + ' '

        rsp = res
        if req[:2] in AllowedList:
            self.rsp_cache[req] = rsp
        if self.vf != 0 and 'NR' not in rsp:
            tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            tmp_addr = self.currentaddress
            if self.currentaddress in dnat.keys():
                tmp_addr = dnat[self.currentaddress]
            self.vf.write(tmstr + ';' + tmp_addr + ';' + req + ';' + rsp + '\n')
            self.vf.flush()
        return rsp

    def cmd(self, command, serviceDelay = 0):
        command = command.upper()
        if command in self.notSupportedCommands.keys():
            return self.notSupportedCommands[command]
        tb = time.time()
        devmode = False
        if tb - self.lastCMDtime < self.busLoad + self.srvsDelay and command.upper()[:2] not in ('AT', 'ST'):
            time.sleep(self.busLoad + self.srvsDelay - tb + self.lastCMDtime)
        tb = time.time()
        saveSession = self.startSession
        if mod_globals.opt_dev and command[0:2] in DevList:
            devmode = True
            self.start_session(mod_globals.opt_devses)
            self.lastCMDtime = time.time()
            if self.lf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.lf.write('#[' + tmstr + ']' + 'Switch to dev mode\n')
                self.lf.flush()
        if tb - self.lastCMDtime > self.keepAlive and len(self.startSession) > 0:
            if self.lf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.lf.write('#[' + tmstr + ']' + 'KeepAlive\n')
                self.lf.flush()
            if not mod_globals.opt_demo:
                self.port.reinit()
            self.send_cmd(self.startSession)
            self.lastCMDtime = time.time()
        cmdrsp = ''
        rep_count = 3
        while rep_count > 0:
            rep_count = rep_count - 1
            no_negative_wait_response = True
            self.lastCMDtime = tc = time.time()
            cmdrsp = self.send_cmd(command)
            for line in cmdrsp.split('\n'):
                line = line.strip().upper()
                nr = ''
                if line.startswith('7F') and len(line) == 8 and line[6:8] in negrsp.keys():
                    nr = line[6:8]
                if line.startswith('NR'):
                    nr = line.split(':')[1]
                if nr in ('12',):
                    self.notSupportedCommands[command] = cmdrsp
                if nr in ('21', '23'):
                    time.sleep(0.5)
                    no_negative_wait_response = False
                elif nr in ('78',):
                    self.send_raw('at at 0')
                    self.send_raw('at st ff')
                    self.lastCMDtime = tc = time.time()
                    cmdrsp = self.send_cmd(command)
                    self.send_raw('at at 1')
                    break

            if no_negative_wait_response:
                break

        if devmode:
            self.startSession = saveSession
            self.start_session(self.startSession)
            self.lastCMDtime = time.time()
            if self.lf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.lf.write('#[' + tmstr + ']' + 'Switch back from dev mode\n')
                self.lf.flush()
        self.srvsDelay = float(serviceDelay) / 1000.0
        for line in cmdrsp.split('\n'):
            line = line.strip().upper()
            if line.startswith('7F') and len(line) == 8 and line[6:8] in negrsp.keys() and self.currentprotocol != 'can':
                if self.lf != 0:
                    self.lf.write('#[' + str(tc - tb) + '] rsp:' + line + ':' + negrsp[line[6:8]] + '\n')
                    self.lf.flush()
                if self.vf != 0:
                    tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                    tmp_addr = self.currentaddress
                    if self.currentaddress in dnat.keys():
                        tmp_addr = dnat[self.currentaddress]
                    self.vf.write(tmstr + ';' + tmp_addr + ';' + command + ';' + line + ';' + negrsp[line[6:8]] + '\n')
                    self.vf.flush()

        return cmdrsp

    def send_cmd(self, command):
        command = command.upper()
        if mod_globals.opt_rate < 50000 and len(command) == 6 and command[:4] == '1902':
            command = '1902AF'
        if command.upper()[:2] in ('AT', 'ST') or self.currentprotocol != 'can':
            return self.send_raw(command)
        elif self.ATCFC0:
            return self.send_can_cfc0(command)
        else:
            rsp = self.send_can(command)
            if self.error_frame > 0 or self.error_bufferfull > 0:
                self.ATCFC0 = True
                self.cmd('at cfc0')
                rsp = self.send_can_cfc0(command)
            return rsp

    def send_can(self, command):
        command = command.strip().replace(' ', '')
        if len(command) == 0:
            return
        elif len(command) % 2 != 0:
            return 'ODD ERROR'
        elif not all((c in string.hexdigits for c in command)):
            return 'HEX ERROR'
        raw_command = []
        cmd_len = len(command) / 2
        if cmd_len < 8:
            if command in self.l1_cache.keys():
                raw_command.append('%0.2X' % cmd_len + command + self.l1_cache[command])
            else:
                raw_command.append('%0.2X' % cmd_len + command)
        else:
            raw_command.append('1' + ('%0.3X' % cmd_len)[-3:] + command[:12])
            command = command[12:]
            frame_number = 1
            while len(command):
                raw_command.append('2' + ('%X' % frame_number)[-1:] + command[:14])
                frame_number = frame_number + 1
                command = command[14:]

        responses = []
        for f in raw_command:
            frsp = self.send_raw(f)
            for s in frsp.split('\n'):
                if s.strip() == f:
                    continue
                s = s.strip().replace(' ', '')
                if len(s) == 0:
                    continue
                if all((c in string.hexdigits for c in s)):
                    if s[:1] == '3':
                        continue
                    responses.append(s)

        result = ''
        noerrors = True
        cframe = 0
        nbytes = 0
        nframes = 0
        if len(responses) == 0:
            return ''
        if len(responses) > 1 and responses[0].startswith('037F') and responses[0][6:8] == '78':
            responses = responses[1:]
            mod_globals.opt_n1c = True
        if len(responses) == 1:
            if responses[0][:1] == '0':
                nbytes = int(responses[0][1:2], 16)
                nframes = 1
                result = responses[0][2:2 + nbytes * 2]
            else:
                self.error_frame += 1
                noerrors = False
        else:
            if responses[0][:1] == '1':
                nbytes = int(responses[0][1:4], 16)
                nframes = nbytes / 7 + 1
                cframe = 1
                result = responses[0][4:16]
            else:
                self.error_frame += 1
                noerrors = False
            for fr in responses[1:]:
                if fr[:1] == '2':
                    tmp_fn = int(fr[1:2], 16)
                    if tmp_fn != cframe % 16:
                        self.error_frame += 1
                        noerrors = False
                        continue
                    cframe += 1
                    result += fr[2:16]
                else:
                    self.error_frame += 1
                    noerrors = False

        if result[:2] == '7F':
            noerrors = False
        if noerrors and nframes < 16 and command[:1] == '2' and not mod_globals.opt_n1c:
            self.l1_cache[command] = str(hex(nframes))[2:].upper()
        if len(result) / 2 >= nbytes and noerrors:
            result = ' '.join((a + b for a, b in zip(result[::2], result[1::2])))
            return result
        elif result[:2] == '7F' and result[4:6] in negrsp.keys():
            if self.vf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.vf.write(tmstr + ';' + dnat[self.currentaddress] + ';' + command + ';' + result + ';' + negrsp[result[4:6]] + '\n')
                self.vf.flush()
            return 'NR:' + result[4:6] + ':' + negrsp[result[4:6]]
        else:
            return 'WRONG RESPONSE'

    def send_can_cfc(self, command):
        command = command.strip().replace(' ', '').upper()
        if len(command) == 0:
            return
        elif len(command) % 2 != 0:
            return 'ODD ERROR'
        elif not all((c in string.hexdigits for c in command)):
            return 'HEX ERROR'
        raw_command = []
        cmd_len = len(command) / 2
        if cmd_len < 8:
            raw_command.append('%0.2X' % cmd_len + command)
        else:
            raw_command.append('1' + ('%0.3X' % cmd_len)[-3:] + command[:12])
            command = command[12:]
            frame_number = 1
            while len(command):
                raw_command.append('2' + ('%X' % frame_number)[-1:] + command[:14])
                frame_number = frame_number + 1
                command = command[14:]

        responses = []
        BS = 1
        ST = 0
        Fc = 0
        Fn = len(raw_command)
        if Fn > 1:
            self.send_raw('at cfc1')
        while Fc < Fn:
            if Fn > 1 and Fn - Fc == 1:
                self.send_raw('at cfc0')
            frsp = ''
            if not self.ATR1:
                frsp = self.send_raw('at r1')
                self.ATR1 = True
            tb = time.time()
            if len(raw_command[Fc]) == 16:
                frsp = self.send_raw(raw_command[Fc])
            else:
                frsp = self.send_raw(raw_command[Fc] + '1')
            frsp = self.send_raw(raw_command[Fc])
            Fc = Fc + 1
            for s in frsp.split('\n'):
                if s.strip()[:len(raw_command[Fc - 1])] == raw_command[Fc - 1]:
                    continue
                s = s.strip().replace(' ', '')
                if len(s) == 0:
                    continue
                if all((c in string.hexdigits for c in s)):
                    if s[:1] == '3':
                        BS = s[2:4]
                        if BS == '':
                            BS = '03'
                        BS = int(BS, 16)
                        ST = s[4:6]
                        if ST == '':
                            ST = 'EF'
                        if ST[:1].upper() == 'F':
                            ST = int(ST[1:2], 16) * 100
                        else:
                            ST = int(ST, 16)
                        break
                    else:
                        responses.append(s)
                        continue

            cf = min({BS - 1, Fn - Fc - 1})
            if cf > 0:
                if self.ATR1:
                    frsp = self.send_raw('at r0')
                    self.ATR1 = False
            while cf > 0:
                cf = cf - 1
                tc = time.time()
                if (tc - tb) * 1000.0 < ST:
                    time.sleep(ST / 1000.0 - (tc - tb))
                tb = tc
                frsp = self.send_raw(raw_command[Fc])
                Fc = Fc + 1

        if len(responses) != 1:
            return 'WRONG RESPONSE'
        result = ''
        noErrors = True
        cFrame = 0
        nBytes = 0
        nFrames = 0
        if responses[0][:1] == '0':
            nBytes = int(responses[0][1:2], 16)
            nFrames = 1
            result = responses[0][2:2 + nBytes * 2]
        elif responses[0][:1] == '1':
            nBytes = int(responses[0][1:4], 16)
            nBytes = nBytes - 6
            nFrames = 1 + nBytes / 7 + bool(nBytes % 7)
            cFrame = 1
            result = responses[0][4:16]
            while cFrame < nFrames:
                sBS = hex(min({nFrames - cFrame, MaxBurst}))[2:]
                frsp = self.send_raw('300' + sBS + '00' + sBS)
                nodataflag = False
                for s in frsp.split('\n'):
                    if s.strip()[:len(raw_command[Fc - 1])] == raw_command[Fc - 1]:
                        continue
                    if 'NO DATA' in s:
                        nodataflag = True
                        break
                    s = s.strip().replace(' ', '')
                    if len(s) == 0:
                        continue
                    if all((c in string.hexdigits for c in s)):
                        responses.append(s)
                        if s[:1] == '2':
                            tmp_fn = int(s[1:2], 16)
                            if tmp_fn != cFrame % 16:
                                self.error_frame += 1
                                noErrors = False
                                continue
                            cFrame += 1
                            result += s[2:16]
                        continue

                if nodataflag:
                    break

        else:
            self.error_frame += 1
            noErrors = False
        if len(result) / 2 >= nBytes and noErrors and result[:2] != '7F':
            result = ' '.join((a + b for a, b in zip(result[::2], result[1::2])))
            return result
        elif result[:2] == '7F' and result[4:6] in negrsp.keys():
            if self.vf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.vf.write(tmstr + ';' + dnat[self.currentaddress] + ';' + command + ';' + result + ';' + negrsp[result[4:6]] + '\n')
                self.vf.flush()
            return 'NR:' + result[4:6] + ':' + negrsp[result[4:6]]
        else:
            return 'WRONG RESPONSE'

    def send_can_cfc0(self, command):
        command = command.strip().replace(' ', '').upper()
        if len(command) == 0:
            return
        elif len(command) % 2 != 0:
            return 'ODD ERROR'
        elif not all((c in string.hexdigits for c in command)):
            return 'HEX ERROR'
        raw_command = []
        cmd_len = len(command) / 2
        if cmd_len < 8:
            raw_command.append('%0.2X' % cmd_len + command)
        else:
            raw_command.append('1' + ('%0.3X' % cmd_len)[-3:] + command[:12])
            command = command[12:]
            frame_number = 1
            while len(command):
                raw_command.append('2' + ('%X' % frame_number)[-1:] + command[:14])
                frame_number = frame_number + 1
                command = command[14:]

        responses = []
        BS = 1
        ST = 0
        Fc = 0
        Fn = len(raw_command)
        if Fn > 1 or len(raw_command[0]) > 15:
            corr_tout = int(75 - self.response_time * 125)
            if corr_tout > 32:
                cmdTxt = 'ATST' + hex(corr_tout)[-2:].zfill(2)
                self.send_raw(cmdTxt)
            else:
                self.send_raw('ATST20')
        while Fc < Fn:
            frsp = ''
            if not self.ATR1:
                frsp = self.send_raw('at r1')
                self.ATR1 = True
            tb = time.time()
            if Fn > 1 and Fc == Fn - 1:
                self.send_raw('ATSTFF')
                self.send_raw('ATAT1')
            if (Fc == 0 or Fc == Fn - 1) and len(raw_command[Fc]) < 16:
                frsp = self.send_raw(raw_command[Fc] + '1')
            else:
                frsp = self.send_raw(raw_command[Fc])
            Fc = Fc + 1
            s0 = []
            for s in frsp.upper().split('\n'):
                if s.strip()[:len(raw_command[Fc - 1])] == raw_command[Fc - 1]:
                    continue
                s = s.strip().replace(' ', '')
                if len(s) == 0:
                    continue
                if all((c in string.hexdigits for c in s)):
                    s0.append(s)

            for s in s0:
                if s[:1] == '3':
                    BS = s[2:4]
                    if BS == '':
                        BS = '03'
                    BS = int(BS, 16)
                    ST = s[4:6]
                    if ST == '':
                        ST = 'EF'
                    if ST[:1].upper() == 'F':
                        ST = int(ST[1:2], 16) * 100
                    else:
                        ST = int(ST, 16)
                    break
                elif s[:4] == '037F' and s[6:8] == '78':
                    if len(s0) > 0 and s == s0[-1]:
                        r = self.waitFrames(6)
                        if len(r.strip()) > 0:
                            responses.append(r)
                    else:
                        continue
                else:
                    responses.append(s)
                    continue

            cf = min({BS - 1, Fn - Fc - 1})
            if cf > 0:
                if self.ATR1:
                    frsp = self.send_raw('at r0')
                    self.ATR1 = False
            while cf > 0:
                cf = cf - 1
                tc = time.time()
                if (tc - tb) * 1000.0 < ST:
                    time.sleep(ST / 1000.0 - (tc - tb))
                tb = tc
                frsp = self.send_raw(raw_command[Fc])
                Fc = Fc + 1

        if len(responses) != 1:
            return 'WRONG RESPONSE'
        result = ''
        noErrors = True
        cFrame = 0
        nBytes = 0
        nFrames = 0
        if responses[0][:1] == '0':
            nBytes = int(responses[0][1:2], 16)
            nFrames = 1
            result = responses[0][2:2 + nBytes * 2]
        elif responses[0][:1] == '1':
            nBytes = int(responses[0][1:4], 16)
            nBytes = nBytes - 6
            nFrames = 1 + nBytes / 7 + bool(nBytes % 7)
            cFrame = 1
            result = responses[0][4:16]
            while cFrame < nFrames:
                sBS = hex(min({nFrames - cFrame, MaxBurst}))[2:]
                frsp = self.send_raw('300' + sBS + '00' + sBS)
                nodataflag = False
                for s in frsp.split('\n'):
                    if s.strip()[:len(raw_command[Fc - 1])] == raw_command[Fc - 1]:
                        continue
                    if 'NO DATA' in s:
                        nodataflag = True
                        break
                    s = s.strip().replace(' ', '')
                    if len(s) == 0:
                        continue
                    if all((c in string.hexdigits for c in s)):
                        responses.append(s)
                        if s[:1] == '2':
                            tmp_fn = int(s[1:2], 16)
                            if tmp_fn != cFrame % 16:
                                self.error_frame += 1
                                noErrors = False
                                continue
                            cFrame += 1
                            result += s[2:16]
                        continue

                if nodataflag:
                    break

        else:
            self.error_frame += 1
            noErrors = False
        if len(result) / 2 >= nBytes and noErrors and result[:2] != '7F':
            result = ' '.join((a + b for a, b in zip(result[::2], result[1::2])))
            return result
        elif result[:2] == '7F' and result[4:6] in negrsp.keys():
            if self.vf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.vf.write(tmstr + ';' + dnat[self.currentaddress] + ';' + command + ';' + result + ';' + negrsp[result[4:6]] + '\n')
                self.vf.flush()
            return 'NR:' + result[4:6] + ':' + negrsp[result[4:6]]
        else:
            return 'WRONG RESPONSE'

    def send_raw(self, command):
        command = command.upper()
        tb = time.time()
        if self.lf != 0:
            tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            self.lf.write('>[' + tmstr + ']' + command + '\n')
            self.lf.flush()
        if not mod_globals.opt_demo:
            self.port.write(str(command + '\r').encode('utf-8'))
        while True:
            tc = time.time()
            if mod_globals.opt_demo:
                break
            self.buff = self.port.expect('>', self.portTimeout)
            tc = time.time()
            if tc - tb > self.portTimeout and 'TIMEOUT' not in self.buff:
                self.buff += 'TIMEOUT'
            if 'TIMEOUT' in self.buff:
                self.error_timeout += 1
                break
            if command in self.buff:
                break
            elif self.lf != 0:
                tmstr = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                self.lf.write('<[' + tmstr + ']' + self.buff + '<shifted>' + command + '\n')
                self.lf.flush()

        if '?' in self.buff:
            self.error_question += 1
        if 'BUFFER FULL' in self.buff:
            self.error_bufferfull += 1
        if 'NO DATA' in self.buff:
            self.error_nodata += 1
        if 'RX ERROR' in self.buff:
            self.error_rx += 1
        if 'CAN ERROR' in self.buff:
            self.error_can += 1
        roundtrip = tc - tb
        self.response_time = (self.response_time * 9 + roundtrip) / 10
        if self.lf != 0:
            self.lf.write('<[' + str(round(roundtrip, 3)) + ']' + self.buff + '\n')
            self.lf.flush()
        return self.buff

    def close_protocol(self):
        self.cmd('atpc')

    def start_session(self, start_session_cmd):
        self.startSession = start_session_cmd
        if len(self.startSession) > 0:
            self.lastinitrsp = self.cmd(self.startSession)

    def check_answer(self, ans):
        if '?' in ans:
            self.unsupportedCommands += 1
        else:
            self.supportedCommands += 1

    def check_adapter(self):
        if mod_globals.opt_demo:
            return
        if self.unsupportedCommands == 0:
            return
        if self.supportedCommands > 0:
            self.lastMessage = '\n\n\tFake adapter !!!\n\n'
        else:
            self.lastMessage = '\n\n\tBroken or unsupported adapter !!!\n\n'

    def init_can(self):
        if not mod_globals.opt_demo:
            self.port.reinit()
        self.currentprotocol = 'can'
        self.currentaddress = '7e0'
        self.startSession = ''
        self.lastCMDtime = 0
        self.l1_cache = {}
        self.notSupportedCommands = {}
        if self.lf != 0:
            tmstr = datetime.now().strftime('%x %H:%M:%S.%f')[:-3]
            self.lf.write('#' * 60 + '\n#[' + tmstr + '] Init CAN\n' + '#' * 60 + '\n')
            self.lf.flush()
        elm_ver = self.cmd('at ws')
        self.check_answer(elm_ver)
        st_rsp = self.cmd('STP 53')
        if '?' not in st_rsp:
            mod_globals.opt_stn = True
        self.check_answer(self.cmd('at e1'))
        self.check_answer(self.cmd('at s0'))
        self.check_answer(self.cmd('at h0'))
        self.check_answer(self.cmd('at l0'))
        self.check_answer(self.cmd('at al'))
        self.check_answer(self.cmd('at caf0'))
        if self.ATCFC0:
            self.check_answer(self.cmd('at cfc0'))
        else:
            self.check_answer(self.cmd('at cfc1'))
        self.lastCMDtime = 0

    def set_can_500(self, addr = 'XXX'):
        if len(addr)==3:
            if mod_globals.opt_can2 and mod_globals.opt_stn:
                self.cmd("STP 53")
                self.cmd("STPBR 500000")
                tmprsp = self.send_raw("0210C0")
                if not 'CAN ERROR' in tmprsp: return
            self.cmd("at sp 6")
        else:
            if mod_globals.opt_can2 and mod_globals.opt_stn:
                self.cmd("STP 54")
                self.cmd("STPBR 500000")
                tmprsp = self.send_raw("0210C0")
                if not 'CAN ERROR' in tmprsp: return
            self.cmd("at sp 7")
    
    def set_can_250(self, addr = 'XXX'):
        if len(addr)==3:
            if mod_globals.opt_can2 and mod_globals.opt_stn:
                self.cmd("STP 53")
                self.cmd("STPBR 250000")
                tmprsp = self.send_raw("0210C0")
                if not 'CAN ERROR' in tmprsp: return
            self.cmd("at sp 8")
        else:
            if mod_globals.opt_can2 and mod_globals.opt_stn:
                self.cmd("STP 54")
                self.cmd("STPBR 250000")
                tmprsp = self.send_raw("0210C0")
                if not 'CAN ERROR' in tmprsp: return
            self.cmd("at sp 9")

    def set_can_addr(self, addr, ecu):
        self.notSupportedCommands = {}
        if self.currentprotocol == 'can' and self.currentaddress == addr:
            return
        if len(ecu['idTx']):
            dnat[addr] = ecu['idTx']
        if len(ecu['idRx']):
            snat[addr] = ecu['idRx']
        if self.lf != 0:
            self.lf.write('#' * 60 + '\n#connect to: ' + ecu['ecuname'] + ' Addr:' + addr + '\n' + '#' * 60 + '\n')
            self.lf.flush()
        self.currentprotocol = 'can'
        self.currentaddress = addr
        self.startSession = ''
        self.lastCMDtime = 0
        self.l1_cache = {}
        self.clear_cache()
        if addr in dnat.keys():
            TXa = dnat[addr]
        else:
            TXa = 'undefined'
        if addr in snat.keys():
            RXa = snat[addr]
        else:
            RXa = 'undefined'
        if len(TXa) == 8:
            self.check_answer(self.cmd('at cp ' + TXa[:2]))
            self.check_answer(self.cmd('at sh ' + TXa[2:]))
        else:
            self.check_answer(self.cmd('at sh ' + TXa))
        self.check_answer(self.cmd('at fc sh ' + TXa))
        self.check_answer(self.cmd('at fc sd 30 00 00'))
        self.check_answer(self.cmd('at fc sm 1'))
        self.check_answer(self.cmd('at st ff'))
        self.check_answer(self.cmd('at at 0'))
        if 'brp' in ecu.keys() and '1' in ecu['brp'] and '0' in ecu['brp']:
            if self.lf != 0:
                self.lf.write('#' * 60 + '\n#    Double BRP, try CAN250 and then CAN500\n' + '#' * 60 + '\n')
                self.lf.flush()
            self.set_can_250(TXa)
            tmprsp = self.send_raw('0210C0')
            if 'CAN ERROR' in tmprsp:
                ecu['brp'] = '0'
                self.set_can_500(TXa)
            else:
                ecu['brp'] = '1'
        elif 'brp' in ecu.keys() and '1' in ecu['brp']:
            self.set_can_250(TXa)
        else:
            self.set_can_500(TXa)
        self.check_answer(self.cmd('at at 1'))
        self.check_answer(self.cmd('at cra ' + RXa))
        self.check_adapter()

    def init_iso(self):
        if not mod_globals.opt_demo:
            self.port.reinit()
        self.currentprotocol = 'iso'
        self.currentsubprotocol = ''
        self.currentaddress = ''
        self.startSession = ''
        self.lastCMDtime = 0
        self.lastinitrsp = ''
        self.notSupportedCommands = {}
        if self.lf != 0:
            tmstr = datetime.now().strftime('%x %H:%M:%S.%f')[:-3]
            self.lf.write('#' * 60 + '\n#[' + tmstr + '] Init ISO\n' + '#' * 60 + '\n')
            self.lf.flush()
        self.check_answer(self.cmd('at ws'))
        self.check_answer(self.cmd('at e1'))
        self.check_answer(self.cmd('at s1'))
        self.check_answer(self.cmd('at l1'))
        self.check_answer(self.cmd('at d1'))

    def set_iso_addr(self, addr, ecu):
        self.notSupportedCommands = {}
        if self.currentprotocol == 'iso' and self.currentaddress == addr and self.currentsubprotocol == ecu['protocol']:
            return
        if self.lf != 0:
            self.lf.write('#' * 60 + '\n#connect to: ' + ecu['ecuname'] + ' Addr:' + addr + ' Protocol:' + ecu['protocol'] + '\n' + '#' * 60 + '\n')
            self.lf.flush()
        if self.currentprotocol == 'iso':
            self.check_answer(self.cmd('82'))
        self.currentprotocol = 'iso'
        self.currentsubprotocol = ecu['protocol']
        self.currentaddress = addr
        self.startSession = ''
        self.lastCMDtime = 0
        self.lastinitrsp = ''
        self.clear_cache()
        self.check_answer(self.cmd('at sh 81 ' + addr + ' f1'))
        self.check_answer(self.cmd('at sw 96'))
        self.check_answer(self.cmd('at wm 81 ' + addr + ' f1 3E'))
        self.check_answer(self.cmd('at ib10'))
        self.check_answer(self.cmd('at st ff'))
        self.check_answer(self.cmd('at at 0'))
        if 'PRNA2000' in ecu['protocol'].upper() or mod_globals.opt_si:
            self.cmd('at sp 4')
            if len(ecu['slowInit']) > 0:
                self.cmd('at iia ' + ecu['slowInit'])
            rsp = self.lastinitrsp = self.cmd('at si')
            if 'ERROR' in rsp and len(ecu['fastInit']) > 0:
                ecu['protocol'] = ''
                if self.lf != 0:
                    self.lf.write('### Try fast init\n')
                    self.lf.flush()
        if 'OK' not in self.lastinitrsp:
            self.cmd('at sp 5')
            self.lastinitrsp = self.cmd('at fi')
        self.check_answer(self.cmd('at at 1'))
        self.check_answer(self.cmd('81'))
        self.check_adapter()

    def checkPerformaceLevel(self, dataids):
        performanceLevels = [3, 2]

        for level in performanceLevels:
            if len(dataids) >= level:
                paramToSend = ''
                frameLength = '{:02X}'.format(1 + level * 2)

                for i in range(level):
                    paramToSend += dataids.keys()[i]
                cmd = frameLength + '22' + paramToSend + '1'

                resp = self.send_raw(cmd)
                if not '?' in resp and resp[2:4] != '7F':
                    self.performanceModeLevel = level
                    return
    
    def reset_elm(self):
        self.cmd('at z')
