#Embedded file name: /build/PyCLIP/android/app/main.py
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
from mod_elm import ELM, get_devices
from mod_scan_ecus import ScanEcus
from mod_ecu import ECU
from mod_ecu_mnemonic import *
from mod_optfile import *
from mod_utils import *
from mod_zip import get_zip
from mod_ecu_default import *
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy import base
import traceback
__all__ = 'install_android'
mod_globals.os = platform
if mod_globals.os == 'android':
    try:
        from jnius import autoclass
        import glob
        AndroidPythonActivity = autoclass('org.renpy.android.PythonActivity')
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        AndroidActivityInfo = autoclass('android.content.pm.ActivityInfo')
        Environment = autoclass('android.os.Environment')
        Params = autoclass('android.view.WindowManager$LayoutParams')
        user_datadir = Environment.getExternalStorageDirectory().getAbsolutePath() + '/pyren/'
        mod_globals.user_data_dir = user_datadir
        mod_globals.cache_dir = user_datadir + '/cache/'
        mod_globals.log_dir = user_datadir + '/logs/'
        mod_globals.dumps_dir = user_datadir + '/dumps/'
        mod_globals.csv_dir = user_datadir + '/csv/'
    except:
        mod_globals.ecu_root = '../'
        try:
            import serial
            from serial.tools import list_ports
        except:
            pass

elif mod_globals.os == 'nt':
    import pip
    try:
        import serial
    except ImportError:
        pip.main(['install', 'pyserial'])

    try:
        import colorama
    except ImportError:
        pip.main(['install', 'colorama'])
        try:
            import colorama
        except ImportError:
            print '\n\n\n\t\t\tGive me access to the Internet for download modules\n\n\n'
            sys.exit()

    colorama.init()
else:
    try:
        import serial
        from serial.tools import list_ports
    except:
        pass

os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
argv_glob = sys.argv
sys.argv = sys.argv[0:1]

def my_excepthook(excType, excValue, tb):
    message = traceback.format_exception(excType, excValue, tb)
    string = ''
    for m in message:
        string += m

    error = TextInput(text=string)
    popup = Popup(title='Crash', content=error, size=(800, 800), size_hint=(None, None), auto_dismiss=True, on_dismiss=exit)
    popup.open()
    base.runTouchApp()
    exit(2)


sys.excepthook = my_excepthook
resizeFont = False

def set_orientation_landscape():
    if mod_globals.os == 'android':
        print 'request landscape orientation'
        activity = AndroidPythonActivity.mActivity
        activity.setRequestedOrientation(AndroidActivityInfo.SCREEN_ORIENTATION_LANDSCAPE)
        print 'landscape orientation done'


def set_orientation_portrait():
    if mod_globals.os == 'android':
        print 'request portrait orientation'
        activity = AndroidPythonActivity.mActivity
        activity.setRequestedOrientation(AndroidActivityInfo.SCREEN_ORIENTATION_PORTRAIT)
        print 'portrait orientation done'


class screenConfig(App):

    def __init__(self):
        self.button = {}
        self.textInput = {}
        super(screenConfig, self).__init__()
        Window.bind(on_keyboard=self.key_handler)

    def key_handler(self, window, keycode1, keycode2, text, modifiers):
        global resizeFont
        print 'keycodes', keycode1, keycode2
        if resizeFont:
            return True
        if (keycode1 == 45 or keycode1 == 269) and mod_globals.fontSize > 10:
            mod_globals.fontSize = mod_globals.fontSize - 1
            resizeFont = True
            self.stop()
            return True
        if (keycode1 == 61 or keycode1 == 270) and mod_globals.fontSize < 40:
            mod_globals.fontSize = mod_globals.fontSize + 1
            resizeFont = True
            self.stop()
            return True
        if keycode1 == 27:
            exit()
        return False

    def set_orientation_all(self):
        if mod_globals.os == 'android':
            activity = AndroidPythonActivity.mActivity
            activity.setRequestedOrientation(AndroidActivityInfo.SCREEN_ORIENTATION_SENSOR)

    def make_box_switch(self, str1, active, callback = None):
        fs = mod_globals.fontSize
        label1 = Label(text=str1, halign='left', valign='middle', size_hint=(1, None), height=fs * 2, font_size=fs)
        sw = Switch(active=active, size_hint=(1, None), height=fs * 2)
        if callback:
            sw.bind(active=callback)
        self.button[str1] = sw
        label1.bind(size=label1.setter('text_size'))
        glay = GridLayout(cols=2, height=fs * 3, size_hint=(1, None), padding=10, spacing=10)
        glay.add_widget(label1)
        glay.add_widget(sw)
        return glay

    def make_input(self, str1, iText):
        fs = mod_globals.fontSize
        label1 = Label(text=str1, halign='left', valign='middle', size_hint=(1, None), height=fs * 2, font_size=fs)
        ti = TextInput(text=iText, multiline=False)
        self.textInput[str1] = ti
        label1.bind(size=label1.setter('text_size'))
        glay = GridLayout(cols=2, height=fs * 3, size_hint=(1, None), padding=10, spacing=10)
        glay.add_widget(label1)
        glay.add_widget(ti)
        return glay

    def make_bt_device_entry(self):
        fs = mod_globals.fontSize
        ports = get_devices()
        label1 = Label(text='ELM port', halign='left', valign='middle', size_hint=(1, None), height=fs, font_size=fs)
        self.bt_dropdown = DropDown(size_hint=(1, None), height=fs * 2)
        label1.bind(size=label1.setter('text_size'))
        glay = GridLayout(cols=2, height=fs * 3, size_hint=(1, None), padding=10, spacing=10)
        btn = Button(text='WiFi (192.168.0.10:35000)', size_hint_y=None, height=fs * 2)
        btn.bind(on_release=lambda btn: self.bt_dropdown.select(btn.text))
        self.bt_dropdown.add_widget(btn)
        for name, address in ports.iteritems():
            if mod_globals.opt_port == name:
                mod_globals.opt_dev_address = address
            btn = Button(text=name + '>' + address, size_hint_y=None, height=fs * 2)
            btn.bind(on_release=lambda btn: self.bt_dropdown.select(btn.text))
            self.bt_dropdown.add_widget(btn)

        self.mainbutton = Button(text='Select', size_hint=(1, None), height=fs * 2)
        self.mainbutton.bind(on_release=self.bt_dropdown.open)
        self.bt_dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.bt_dropdown.select(mod_globals.opt_port)
        glay.add_widget(label1)
        glay.add_widget(self.mainbutton)
        return glay
    
    def changeLangButton(self, buttonText):
        setattr(self.langbutton, 'text', buttonText)
        setattr(self.langbutton, 'background_normal', '')
        setattr(self.langbutton, 'background_color', (0.345,0.345,0.345,1))

    def make_language_entry(self):
        fs = mod_globals.fontSize
        langs = mod_zip.get_languages()
        label1 = Label(text='Language', halign='left', valign='middle', size_hint=(1, None), height=fs * 2, font_size=fs)
        self.lang_dropdown = DropDown(size_hint=(1, None), height=fs)
        label1.bind(size=label1.setter('text_size'))
        glay = GridLayout(cols=2, height=fs * 3, size_hint=(1, None), padding=10, spacing=10)
        for lang in sorted(langs):
            btn = Button(text=lang, size_hint_y=None, height=fs * 2)
            btn.bind(on_release=lambda btn: self.lang_dropdown.select(btn.text))
            self.lang_dropdown.add_widget(btn)

        if mod_globals.opt_lang:
            if (len(mod_globals.opt_lang) > 2 and len(langs[0]) == 2) or (len(mod_globals.opt_lang) == 2 and len(langs[0]) > 2) :
                txt = 'SELECT'
            else:
                txt = mod_globals.opt_lang
        else:
            txt = 'SELECT'
        
        if txt == 'SELECT':
            self.langbutton = Button(text=txt, size_hint=(1, None), height=fs * 2, background_normal='', background_color=(1,0,0,1))
        else:
            self.langbutton = Button(text=txt, size_hint=(1, None), height=fs * 2)
        self.langbutton.bind(on_release=self.lang_dropdown.open)
        self.lang_dropdown.bind(on_select=lambda instance, x: self.changeLangButton(x))
        # self.lang_dropdown.select(txt)
        glay.add_widget(label1)
        glay.add_widget(self.langbutton)
        return glay

    def finish(self, instance):
        mod_globals.opt_port = ''
        mod_globals.opt_ecuid = ''
        mod_globals.opt_speed = 38400
        mod_globals.opt_rate = 38400
        mod_globals.opt_lang = self.langbutton.text
        mod_globals.opt_car = 0
        if self.button['Generate logs'].active:
            mod_globals.opt_log = 'log.txt' if self.textInput['Log name'].text == '' else self.textInput['Log name'].text
        else:
            mod_globals.opt_log = 'log.txt'
        try:
            mod_globals.fontSize = int(self.textInput['Font size'].text)
        except:
            mod_globals.fontSize = 20

        mod_globals.opt_demo = self.button['Demo mode'].active
        mod_globals.opt_scan = self.button['Scan vehicle'].active
        mod_globals.opt_csv = self.button['CSV Log'].active
        mod_globals.opt_csv_only = False
        mod_globals.opt_csv_human = False
        if mod_globals.opt_csv : mod_globals.opt_csv_human = True
        mod_globals.opt_usrkey = ''
        mod_globals.opt_verbose = False
        mod_globals.opt_si = self.button['KWP Force SlowInit'].active
        mod_globals.opt_cfc0 = self.button['Use CFC0'].active
        mod_globals.opt_n1c = False
        mod_globals.opt_exp = False
        mod_globals.opt_dump = self.button['DUMP'].active
        mod_globals.opt_can2 = self.button['CAN2 (Multimedia CAN)'].active
        if 'wifi' in self.mainbutton.text.lower():
            mod_globals.opt_port = '192.168.0.10:35000'
        else:
            bt_device = self.mainbutton.text.split('>')
            mod_globals.opt_port = bt_device[0]
            if len(bt_device) > 1:
                mod_globals.opt_dev_address = bt_device[-1]
            mod_globals.bt_dev = self.mainbutton.text
        self.stop()

    def change_orientation(self, inst, val):
        if val:
            set_orientation_landscape()
            mod_globals.screen_orient = True
        else:
            set_orientation_portrait()
            mod_globals.screen_orient = False

    def build(self):
        layout = GridLayout(cols=1, padding=10, spacing=20, size_hint=(1.0, None))
        layout.bind(minimum_height=layout.setter('height'))
        fs = mod_globals.fontSize
        layout.add_widget(Label(text='PyClip (pyren)', font_size=fs * 2, height=fs * 2, size_hint=(1, None)))
        layout.add_widget(Label(text='Data directory : ' + mod_globals.user_data_dir, font_size=mod_globals.fontSize, height=fs * 2, size_hint=(1, None)))
        get_zip()
        layout.add_widget(Label(text='DB archive : ' + mod_globals.db_archive_file, font_size=mod_globals.fontSize, height=fs * 2, size_hint=(1, None)))
        gobtn = Button(text='START', height=fs * 3, size_hint=(1, None), on_press=self.finish)
        layout.add_widget(gobtn)
        layout.add_widget(self.make_bt_device_entry())
        layout.add_widget(self.make_language_entry())
        layout.add_widget(self.make_box_switch('Demo mode', mod_globals.opt_demo))
        layout.add_widget(self.make_box_switch('DUMP', mod_globals.opt_dump))
        layout.add_widget(self.make_box_switch('Orientation landscape', mod_globals.screen_orient, self.change_orientation))
        layout.add_widget(self.make_box_switch('Scan vehicle', mod_globals.opt_scan))
        layout.add_widget(self.make_box_switch('Generate logs', True if len(mod_globals.opt_log) > 0 else False))
        layout.add_widget(self.make_input('Log name', mod_globals.opt_log))
        layout.add_widget(self.make_box_switch('CSV Log',mod_globals.opt_csv))
        layout.add_widget(self.make_box_switch('CAN2 (Multimedia CAN)', mod_globals.opt_can2))
        layout.add_widget(self.make_input('Font size', str(mod_globals.fontSize)))
        layout.add_widget(self.make_box_switch('KWP Force SlowInit', mod_globals.opt_si))
        layout.add_widget(self.make_box_switch('Use CFC0', mod_globals.opt_cfc0))
        layout.add_widget(Label(text='PyClip by Marianpol 14-10-2021', font_size=fs, height=fs, size_hint=(1, None)))
        self.lay = layout
        root = ScrollView(size_hint=(1, 1), do_scroll_x=False, pos_hint={'center_x': 0.5,
         'center_y': 0.5})
        root.add_widget(layout)
        return root


def destroy():
    exit()


def kivyScreenConfig():
    global resizeFont
    if mod_globals.os != 'android':
        Window.size = (800, 800)
    else:
        if not mod_globals.screen_orient:
            set_orientation_portrait()
        else:
            set_orientation_landscape()
    
    Window.bind(on_close=destroy)
    while 1:
        config = screenConfig()
        config.run()
        if not resizeFont:
            return
        resizeFont = False


def main():
    version_file_name = 'version09r_1_0_0.txt'
    if not os.path.exists(mod_globals.cache_dir):
        os.makedirs(mod_globals.cache_dir)
    if not os.path.exists(mod_globals.log_dir):
        os.makedirs(mod_globals.log_dir)
    if not os.path.exists(mod_globals.dumps_dir):
        os.makedirs(mod_globals.dumps_dir)
    if not os.path.exists(mod_globals.csv_dir):
        os.makedirs(mod_globals.csv_dir)
    if not os.path.isfile(mod_globals.cache_dir + version_file_name):
        if os.path.isfile(os.path.join(mod_globals.user_data_dir + 'settings.p')):
            os.remove(os.path.join(mod_globals.user_data_dir + 'settings.p'))
    settings = mod_globals.Settings()
    kivyScreenConfig()
    settings.save()
    print 'Opening ELM'
    try:
        elm = ELM(mod_globals.opt_port, mod_globals.opt_speed, mod_globals.opt_log)
    except:
        labelText = '''
            Could not connect to the ELM.

            Possible causes:
            - Bluetooth is not enabled
            - other applications are connected to your ELM e.g Torque
            - other device is using this ELM
            - ELM got unpaired
            - ELM is read under new name or it changed its name

            Check your ELM connection and try again.
        '''
        lbltxt = Label(text=labelText, font_size=mod_globals.fontSize)
        popup_load = Popup(title='ELM connection error', content=lbltxt, size=(800, 800), auto_dismiss=True, on_dismiss=exit)
        popup_load.open()
        base.runTouchApp()
        exit(2)
    if mod_globals.opt_speed < mod_globals.opt_rate and not mod_globals.opt_demo:
        elm.port.soft_boudrate(mod_globals.opt_rate)
    print 'Loading ECUs list'
    se = ScanEcus(elm)
    SEFname = mod_globals.user_data_dir + '/savedEcus.p'
    if mod_globals.opt_can2:
        SEFname = mod_globals.user_data_dir + '/savedEcus2.p'
    if not os.path.exists(SEFname):
        SEFname = './savedEcus.p'
    if mod_globals.opt_demo and len(mod_globals.opt_ecuid) > 0:
        se.read_Uces_file(all=True)
        se.detectedEcus = []
        for i in mod_globals.opt_ecuid.split(','):
            if i in se.allecus.keys():
                se.allecus[i]['ecuname'] = i
                se.allecus[i]['idf'] = se.allecus[i]['ModelId'][2:4]
                if se.allecus[i]['idf'][0] == '0':
                    se.allecus[i]['idf'] = se.allecus[i]['idf'][1]
                se.allecus[i]['pin'] = 'can'
                se.detectedEcus.append(se.allecus[i])

    else:
        if not os.path.isfile(SEFname) or mod_globals.opt_scan:
            se.chooseModel(mod_globals.opt_car)
        se.scanAllEcus()
    lbltxt = Label(text='Loading language', font_size=20)
    popup_load = Popup(title='Status', content=lbltxt, size=(400, 400), size_hint=(None, None))
    base.runTouchApp(slave=True)
    popup_load.open()
    base.EventLoop.idle()
    sys.stdout.flush()
    lang = mod_zip.get_lang_dict(mod_globals.opt_lang)
    if lang:
        mod_globals.language_dict = lang
    base.EventLoop.window.remove_widget(popup_load)
    popup_load.dismiss()
    base.stopTouchApp()
    base.EventLoop.window.canvas.clear()
    if not os.path.isfile(mod_globals.cache_dir + version_file_name):
        for root, dirs, files in os.walk(mod_globals.cache_dir):
            for sfile in files:
                if sfile.startswith('ver') or sfile.startswith('FG'):
                    full_path = os.path.join(mod_globals.cache_dir, sfile)
                    os.remove(full_path)

        verfile = open(mod_globals.cache_dir + version_file_name, 'wb')
        verfile.write('Do not remove me if you have v.0.9.e or above.\n')
        verfile.close()
    while 1:
        clearScreen()
        choosen_ecu = se.chooseECU(mod_globals.opt_ecuid)
        mod_globals.opt_ecuid = ''
        if choosen_ecu == -1:
            continue
        ecucashfile = mod_globals.cache_dir + choosen_ecu['ModelId'] + '_' + mod_globals.opt_lang + '.p'
        if os.path.isfile(ecucashfile):
            ecu = pickle.load(open(ecucashfile, 'rb'))
        else:
            ecu = ECU(choosen_ecu, mod_globals.language_dict)
            pickle.dump(ecu, open(ecucashfile, 'wb'))
        ecu.initELM(elm)
        if mod_globals.opt_demo:
            print 'Loading dump'
            ecu.loadDump()
        elif mod_globals.opt_dump:
            print 'Saving dump'
            ecu.saveDump()
        ecu.show_screens()


if __name__ == '__main__':
    main()
