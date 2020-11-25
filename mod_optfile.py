#Embedded file name: /build/PyCLIP/android/app/mod_optfile.py
import glob
import json
import os
import pickle
import struct
import sys
from xml.dom.minidom import parseString
import mod_globals
import mod_zip

class optfile:
    dict = {}
    obf = True

    def __init__(self, filename, progress = False, cache = True, zip = False):
        self.dict = {}
        fn = filename
        pn = './cache/' + os.path.basename(fn) + '.p'
        if os.path.isfile(pn):
            self.dict = pickle.load(open(pn, 'rb'))
        elif os.path.isfile(fn):
            if not zip:
                lf = open(fn, 'rb')
            else:
                lf = mod_zip.get_file_content(fn)
            self.get_dict(lf, progress)
            if cache:
                pickle.dump(self.dict, open(pn, 'wb'))

    def get_string(self, lf, len):
        i = lf.tell()
        bytes = lf.read(2 * len)
        st = ''
        j = 0
        len = len * 2
        while j < len:
            x = struct.unpack('<H', bytes[j:j + 2])[0]
            if self.obf:
                x = x ^ i & 65535 ^ 21845
            j += 2
            i += 2
            st += unichr(x)

        return st

    def get_2_bytes(self, lf):
        i = lf.tell()
        bytes = lf.read(2)
        x = 0
        x = struct.unpack('<H', bytes)[0]
        if self.obf == False:
            return x
        return x ^ i & 65535 ^ 21845

    def get_4_bytes(self, lf):
        return self.get_2_bytes(lf) + (self.get_2_bytes(lf) << 16)

    def get_dict(self, lf, progress):
        self.fb = ord(lf.read(1))
        if self.fb != 85 and self.fb != 189:
            self.obf = False
        lf.seek(20)
        protlen = self.get_4_bytes(lf)
        lf.seek(24 + protlen * 2)
        keyoff = self.get_4_bytes(lf)
        lf.seek(keyoff - 8)
        tb = self.get_4_bytes(lf)
        i = keyoff
        n = 0
        while i < tb:
            if progress and i & 255 == 0:
                pr = (i + 2 - keyoff) * 100 / (tb - keyoff)
                print '\r[' + 'X' * (pr / 2) + ' ' * (50 - pr / 2) + '] ' + str(int(pr)) + '%',
                sys.stdout.flush()
            lf.seek(i)
            addr = self.get_4_bytes(lf)
            strl = self.get_4_bytes(lf)
            keyl = self.get_4_bytes(lf)
            n = n + 1
            key = self.get_string(lf, keyl)
            lf.seek(addr)
            line = self.get_string(lf, strl)
            line = line.strip()
            line = line.strip('\n')
            line = line.replace(u'\xab', '"')
            line = line.replace(u'\xbb', '"')
            self.dict[key] = line
            i = i + 12 + keyl * 2

        if progress:
            print '\r[' + 'X' * 50 + '] 100%',


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    if len(sys.argv) == 1:
        print 'Usage: mod_optfile.py <filename> [key]'
        print '       mod_optfile.py ALLSG'
        print 'Example:'
        print '   mod_optfile.py Location/DiagOnCan_RU.bqm'
        print '   mod_optfile.py EcuRenault/Sessions/SG0110016.XML P001'
        sys.exit(0)
    if sys.argv[1] == 'ALLSG':
        for file in glob.glob('../EcuRenault/Sessions/*.xml'):
            file = os.path.basename(file)
            if file.startswith('SG'):
                sgFileName = '../EcuRenault/Sessions/S' + file[1:]
                ugFileName = '../EcuRenault/Sessions/U' + file[1:-4] + '.json'
                if os.path.exists(ugFileName):
                    print 'Skipping ', ugFileName
                    continue
                try:
                    of = optfile(sgFileName, False, False)
                except:
                    continue

                print ugFileName
                f = open(ugFileName, 'wt')
                f.write(json.dumps(of.dict))
                f.close()

        exit(0)
    if sys.argv[1] == 'ALLBQM':
        for file in glob.glob('../Location/*.bqm'):
            print file
            sgFileName = mod_globals.location_dir + '/' + file
            ugFileName = mod_globals.location_dir + '/Convert/' + os.path.basename(file)[:-4] + '.json'
            of = optfile(sgFileName, False, False)
            rf = json.dumps(of.dict)
            print ugFileName
            f = open(ugFileName, 'wt')
            f.write(rf)
            f.close()

        exit(0)
    of = optfile(sys.argv[1])
    if len(sys.argv) == 2:
        for k in sorted(of.dict.keys()):
            print '#' * 60
            print 'Key:', k
            print '-' * 60
            if of.dict[k][:1] == '<' and of.dict[k][-1:] == '>':
                print parseString(of.dict[k]).toprettyxml(indent='  ')
            else:
                print of.dict[k]

    of = optfile(sys.argv[1])
    if len(sys.argv) == 2:
        for k in sorted(of.dict.keys()):
            print '#' * 60
            print 'Key:', k
            print '-' * 60
            if of.dict[k][:1] == '<' and of.dict[k][-1:] == '>':
                print parseString(of.dict[k]).toprettyxml(indent='  ')
            else:
                print of.dict[k]

    if len(sys.argv) == 3:
        k = sys.argv[2]
        if k in of.dict.keys():
            if of.dict[k][:1] == '<' and of.dict[k][-1:] == '>':
                print parseString(of.dict[k]).toprettyxml(indent='  ')
            else:
                print of.dict[k]
        else:
            for i in sorted(of.dict.keys()):
                if k in i:
                    print '#' * 60
                    print 'Key:', i
                    print '-' * 60
                    if of.dict[i][:1] == '<' and of.dict[i][-1:] == '>':
                        print parseString(of.dict[i]).toprettyxml(indent='  ')
                    else:
                        print of.dict[i]
