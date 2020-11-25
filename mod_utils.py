#Embedded file name: /build/PyCLIP/android/app/mod_utils.py
import os
import sys
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import mod_globals
widgetglobal = None
choice_result = None
resizeFont = False

class widgetChoiceLong(App):

    def __init__(self, list, question, header = ''):
        self.menu_entries = list
        self.header = header
        self.question = question
        self.choice_result = None
        super(widgetChoiceLong, self).__init__()
        Window.bind(on_keyboard=self.key_handler)

    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        global choice_result
        global resizeFont
        if resizeFont:
            return True
        if keycode1 == 45 and mod_globals.fontSize > 10:
            mod_globals.fontSize = mod_globals.fontSize - 1
            resizeFont = True
            self.stop()
            return True
        if keycode1 == 61 and mod_globals.fontSize < 40:
            mod_globals.fontSize = mod_globals.fontSize + 1
            resizeFont = True
            self.stop()
            return True
        if keycode1 == 27:
            choice_result = ['<Up>', -1]
            self.stop()
            return True
        return False

    # def on_pause(self):
    #     exit()

    def choice_done(self, instance):
        global choice_result
        choice_result = [instance.txt, instance.ID]
        self.stop()

    def build(self):
        fs = mod_globals.fontSize
        layout = GridLayout(cols=1, padding=10, spacing=20, size_hint=(1.0, None))
        layout.bind(minimum_height=layout.setter('height'))
        if self.header:
            titlelabel = Label(text=self.header, height=fs * 3, size_hint=(1.0, None))
            titlelabel.bind(size=titlelabel.setter('text_size'))
            titlelabel.texture_update()
            titlelabel.height = titlelabel.texture_size[1]
            layout.add_widget(titlelabel)
        question = Label(text=self.question, height=fs, size_hint=(1.0, None))
        layout.add_widget(question)
        i = 1
        for entry in self.menu_entries:
            btn = Button(text='  ' + pyren_encode(entry), height=fs * 4, size_hint=(1.0, None), halign='left', valign='middle', font_name='RobotoMono-Regular', font_size=fs)
            btn.bind(size=btn.setter('text_size'))
            btn.txt = entry
            btn.ID = i
            btn.bind(on_press=self.choice_done)
            layout.add_widget(btn)
            i += 1

        root = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5,
         'center_y': 0.5}, do_scroll_x=False)
        root.add_widget(layout)
        return root


def kivyChoiceLong(list, question, header = ''):
    global widgetglobal
    global resizeFont
    while 1:
        widgetglobal = widgetChoiceLong(list, question, header)
        widgetglobal.run()
        if not resizeFont:
            return choice_result
        resizeFont = False


def Choice(list, question):
    return kivyChoiceLong(list, question)


def ChoiceLong(list, question, header = ''):
    return kivyChoiceLong(list, question, header)


def ChoiceFromDict(dict, question, showId = True):
    d = {}
    c = 1
    exitNumber = 0
    for k in sorted(dict.keys()):
        s = dict[k]
        if k.lower() == '<up>' or k.lower() == '<exit>':
            exitNumber = c
            print '%s - %s' % ('Q', pyren_encode(s))
            d['Q'] = k
        else:
            if showId:
                print '%s - (%s) %s' % (c, pyren_encode(k), pyren_encode(s))
            else:
                print '%s - %s' % (c, pyren_encode(s))
            d[str(c)] = k
        c = c + 1

    while True:
        try:
            ch = raw_input(question)
        except (KeyboardInterrupt, SystemExit):
            print
            print
            sys.exit()

        if ch == 'q':
            ch = 'Q'
        if ch in d.keys():
            return [d[ch], ch]


def pyren_encode(inp):
    if mod_globals.os == 'android':
        return inp.encode('utf-8', errors='replace')
    else:
        return inp.encode(sys.stdout.encoding, errors='replace')

def pyren_decode(inp):
    if mod_globals.os == 'android':
        return inp.decode('utf-8', errors='replace')
    else:
        return inp.decode(sys.stdout.encoding, errors='replace')

def pyren_decode_i(inp):
    if mod_globals.os == 'android':
        return inp.decode('utf-8', errors='ignore')
    else:
        return inp.decode(sys.stdout.encoding, errors='ignore')

def clearScreen():
    sys.stdout.write(chr(27) + '[2J' + chr(27) + '[;H')


def hex_VIN_plus_CRC(VIN, plusCRC=True):
    VIN = VIN.upper()
    hexVIN = ''
    CRC = 65535
    for c in VIN:
        b = ord(c)
        hexVIN = hexVIN + hex(b)[2:].upper()
        for i in range(8):
            if (CRC ^ b) & 1:
                CRC = CRC >> 1
                CRC = CRC ^ 33800
                b = b >> 1
            else:
                CRC = CRC >> 1
                b = b >> 1

    CRC = CRC ^ 65535
    b1 = CRC >> 8 & 255
    b2 = CRC & 255
    CRC = (b2 << 8 | b1) & 65535
    sCRC = hex(CRC)[2:].upper()
    sCRC = '0' * (4 - len(sCRC)) + sCRC
    if plusCRC:
        return hexVIN + sCRC
    else:
        return hexVIN

def ASCIITOHEX(ATH):
    ATH = ATH.upper()
    hexATH = ''.join(('{:02x}'.format(ord(c)) for c in ATH))
    return hexATH


def StringToIntToHex(DEC):
    DEC = int(DEC)
    hDEC = hex(DEC)
    return hDEC[2:].zfill(2).upper()


def getVIN(de, elm, getFirst = False):
    m_vin = set([])
    for e in de:
        if mod_globals.opt_demo:
            loadDumpToELM(e['ecuname'], elm)
        else:
            if e['pin'].lower() == 'can':
                elm.init_can()
                elm.set_can_addr(e['dst'], e)
            else:
                elm.init_iso()
                elm.set_iso_addr(e['dst'], e)
            elm.start_session(e['startDiagReq'])
        if e['stdType'].lower() == 'uds':
            rsp = elm.request(req='22F190', positive='62', cache=False)[9:59]
        else:
            rsp = elm.request(req='2181', positive='61', cache=False)[6:56]
        try:
            vin = rsp.replace(' ', '').decode('HEX')
        except:
            continue

        if len(vin) == 17:
            m_vin.add(vin)
            if getFirst:
                return vin

    l_vin = m_vin
    if os.path.exists('savedVIN.txt'):
        with open('savedVIN.txt') as vinfile:
            vinlines = vinfile.readlines()
            for l in vinlines:
                l = l.strip()
                if '#' in l:
                    continue
                if len(l) == 17:
                    l_vin.add(l.upper())

    if len(l_vin) == 0 and not getFirst:
        print "ERROR!!! Can't find any VIN. Check connection"
        exit()
    if len(l_vin) < 2:
        try:
            ret = next(iter(l_vin))
        except:
            ret = ''

        return ret
    print '\nFound ', len(l_vin), ' VINs\n'
    choice = Choice(l_vin, 'Choose VIN : ')
    return choice[0]


def DBG(tag, s):
    if mod_globals.opt_debug and mod_globals.debug_file != None:
        mod_globals.debug_file.write('### ' + tag + '\n')
        mod_globals.debug_file.write('"' + s + '"\n')


def kill_server():
    if mod_globals.doc_server_proc is None:
        pass
    else:
        os.kill(mod_globals.doc_server_proc.pid, signal.SIGTERM)


def show_doc(addr, id):
    if mod_globals.vin == '':
        return
    if mod_globals.doc_server_proc == None:
        mod_globals.doc_server_proc = subprocess.Popen(['python',
         '-m',
         'SimpleHTTPServer',
         '59152'])
        atexit.register(kill_server)
    if mod_globals.opt_sd:
        url = 'http://localhost:59152/doc/' + id[1:] + '.htm'
    else:
        url = 'http://localhost:59152/doc/' + mod_globals.vin + '.htm' + id
    webbrowser.open(url, new=0)
