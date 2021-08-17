#Embedded file name: /build/PyCLIP/android/app/mod_ecu_mnemonic.py
import string
import xml.dom.minidom
from xml.dom.minidom import parse
from mod_ecu_service import *

def get_mnemonicDTC(m, resp):
    bytes = 1
    bits = int(m.bitsLength)
    if bits > 7:
        bytes = bits / 8
    hexval = '00'
    sb = int(m.startByte) - 1
    if sb * 3 + bytes * 3 - 1 > len(resp):
        return hexval
    hexval = resp[sb * 3:(sb + bytes) * 3 - 1]
    hexval = hexval.replace(' ', '')
    if bits < 8:
        val = int(hexval, 16)
        val = val << int(m.startBit) >> 8 - bits & 2 ** bits - 1
        hexval = str(val)
    return hexval

def get_SnapShotMnemonic(m, se, elm, dataids):
    snapshotService = ""
    byteLength = 3
    dataIdByteLength = 2

    for sid in se:
        if len(se[sid].params) > 1:
            if se[sid].params[1]['type'] == 'Snapshot':
                snapshotService = se[sid]
    
    resp = executeService( snapshotService, elm, [], "", True )
    if ((mod_globals.opt_demo and not resp) or not resp.startswith(snapshotService.simpleRsp) or len(resp)/2 == 6):
        return '00'
    resp = resp.strip().replace(' ', '')
    if not all((c in string.hexdigits for c in resp)):
        resp = ''
    resp = ' '.join((a + b for a, b in zip(resp[::2], resp[1::2])))
    numberOfIdentifiers = int("0x" + resp[7*byteLength:8*byteLength-1],16)
    resp = resp[8*byteLength:]

    didDict = {}
    numberOfPossibleDataId = 0
    posInResp = 0
    dataIdLength = dataIdByteLength * byteLength

    for idNum in range(numberOfIdentifiers):
        if (idNum + numberOfPossibleDataId > numberOfIdentifiers):
            break
        
        dataId = resp[posInResp:posInResp + dataIdLength].replace(" ", "")
        posInResp += dataIdLength

        if dataId not in dataids.keys():
            bytePos = 1
            restOfResp = resp[posInResp:]

            while True:
                posInRestResp = bytePos*byteLength
                if len(restOfResp) > posInRestResp + dataIdLength and restOfResp[posInRestResp] == '2':
                    numberOfPossibleDataId = numberOfPossibleDataId + 1
                    possibleDataId = restOfResp[posInRestResp:posInRestResp + dataIdLength].replace(" ", "")
                    if possibleDataId in dataids.keys():
                        posInResp += posInRestResp
                        break
                    else:
                        bytePos += 1
                else:
                    bytePos += 1
            continue

        didDataLength = int(dataids[dataId].dataBitLength)/8
        didData = resp[posInResp: posInResp + didDataLength*3]
        posInResp += didDataLength*3
        didDict[dataId] = didData
    
    startByte = '1'
    startBit = '0'
    dataId = ''
    for did in dataids.keys():
        for mn in dataids[did].mnemolocations.keys():
            if mn == m.name:
                dataId = did
                startByte = dataids[dataId].mnemolocations[m.name].startByte
                startBit = dataids[dataId].mnemolocations[m.name].startBit
    
    if dataId not in didDict:
        didDict[dataId] = '0' * (int(dataids[dataId].dataBitLength)/8)

    hexval = getHexVal(m, startByte, startBit, didDict[dataId])
    return hexval


def get_mnemonic(m, se, elm):
    if not m.serviceID and mod_globals.ext_cur_DTC != '000000':
        for sid in se.keys():
            startReq = se[sid].startReq
            if startReq.startswith("12") and startReq.endswith(mod_globals.ext_cur_DTC[:4]):
                m.startByte = se[sid].responces[se[sid].responces.keys()[0]].mnemolocations[m.name].startByte
                m.startBit = se[sid].responces[se[sid].responces.keys()[0]].mnemolocations[m.name].startBit
                m.request = se[sid].startReq
                m.positive = se[sid].simpleRsp
                m.delay = '100' 
    if len(m.sids) > 0:
        for sid in m.sids:
            service = se[sid]
            resp = executeService(service, elm, [], '', True)

    else:
        resp = elm.request(m.request, m.positive, True, m.delay)
    resp = resp.strip().replace(' ', '')
    if not all((c in string.hexdigits for c in resp)):
        resp = ''
    resp = ' '.join((a + b for a, b in zip(resp[::2], resp[1::2])))
    if len(m.startByte) == 0:
        m.startByte = u'01'
    
    hexval = getHexVal(m, m.startByte, m.startBit, resp)
    return hexval
    
def getHexVal(m, startByte, startBit, resp):
    sb = int(startByte) - 1
    bits = int(m.bitsLength)
    sbit = int(startBit)
    bytes = (bits + sbit - 1) / 8 + 1
    rshift = ((bytes + 1) * 8 - (bits + sbit)) % 8
    if sb * 3 + bytes * 3 - 1 > len(resp):
        return '00'
    hexval = resp[sb * 3:(sb + bytes) * 3 - 1]
    hexval = hexval.replace(' ', '')
    val = int(hexval, 16) >> rshift & 2 ** bits - 1
    hexval = hex(val)[2:]
    if hexval[-1:].upper() == 'L':
        hexval = hexval[:-1]
    if len(hexval) % 2:
        hexval = '0' + hexval
    if (len(hexval)/2)%bytes:
        hexval = '00' * (bytes - len(hexval)/2) + hexval
    if m.littleEndian == '1':
        a = hexval
        b = ''
        if not len(a) % 2:
            for i in range(0, len(a), 2):
                b = a[i:i + 2] + b

            hexval = b
    return hexval


class ecu_mnemonic:
    name = ''
    littleEndian = ''
    type = ''
    bitsLength = ''
    serviceID = ''
    startByte = ''
    startBit = ''
    request = ''
    delay = ''
    nextDelay = ''
    rOffset = ''
    positive = ''
    sids = []

    def __str__(self):
        out = '\n  name          = %s\n  littleEndian  = %s\n  type          = %s\n  bitsLength    = %s\n  serviceID     = %s\n  startByte     = %s\n  startBit      = %s\n  request       = %s\n  delay         = %s\n  nextDelay     = %s\n  rOffset       = %s\n  positive      = %s\n  sids          = %s\n    ' % (self.name,
         self.littleEndian,
         self.type,
         self.bitsLength,
         self.serviceID,
         self.startByte,
         self.startBit,
         self.request,
         self.delay,
         self.nextDelay,
         self.rOffset,
         self.positive,
         self.sids)
        return pyren_encode(out)

    def __init__(self, sv, opt):
        self.name = sv.getAttribute('name')
        MnemoDatas = sv.getElementsByTagName('MnemoDatas').item(0)
        if MnemoDatas:
            self.littleEndian = MnemoDatas.getAttribute('littleEndian')
            self.type = MnemoDatas.getAttribute('type')
            self.bitsLength = MnemoDatas.getAttribute('bitsLength')
        self.sids = []
        ServiceID = sv.getElementsByTagName('ServiceID').item(0)
        ServiceIDs = sv.getElementsByTagName('ServiceID')
        if ServiceIDs:
            for ServiceID in ServiceIDs:
                self.serviceID = ServiceID.getAttribute('name')
                self.sids.append(self.serviceID)
                srvxmlstr = opt['Service\\' + self.serviceID]
                sdom = xml.dom.minidom.parseString(srvxmlstr.encode('utf-8'))
                sdoc = sdom.documentElement
                self.delay = sdoc.getAttribute('delay')
                if len(self.delay) == 0:
                    self.delay = '0'
                Start = sdoc.getElementsByTagName('Start').item(0)
                if Start:
                    Request = sdoc.getElementsByTagName('Request').item(0)
                    if Request:
                        self.request = Request.getAttribute('val')
                        self.nextDelay = Request.getAttribute('nextDelay')
                MnemoLocation = sdoc.getElementsByTagName('MnemoLocation')
                for m in MnemoLocation:
                    if m.getAttribute('name') == self.name:
                        self.startByte = m.getAttribute('startByte')
                        self.startBit = m.getAttribute('startBit')
                        self.rOffset = m.getAttribute('rOffset')

                self.positive = ''
                Simple = sdoc.getElementsByTagName('Simple').item(0)
                if Simple:
                    self.positive = Simple.getAttribute('val')
                    continue
                RepeatInProgress = sdoc.getElementsByTagName('RepeatInProgress').item(0)
                if RepeatInProgress:
                    self.positive = RepeatInProgress.getAttribute('val')
                    continue


class ecu_mnemonics:

    def __init__(self, mnemonic_list, mdoc, opt, tran):
        for k in opt.keys():
            if 'Mnemonic' in k:
                xmlstr = opt[k]
                odom = xml.dom.minidom.parseString(xmlstr.encode('utf-8'))
                odoc = odom.documentElement
                mnemonic = ecu_mnemonic(odoc, opt)
                mnemonic_list[mnemonic.name] = mnemonic
