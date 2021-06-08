#Embedded file name: /build/PyCLIP/android/app/mod_globals.py
import os as sysos
import pickle
opt_debug = True
debug_file = None
opt_port = ''
opt_ecuid = ''
opt_ecuAddr = ''
opt_protocol = ''
opt_speed = 38400
opt_rate = 38400
opt_dev_address = ''
opt_lang = ''
opt_car = ''
opt_log = ''
opt_demo = False
opt_scan = False
opt_csv = False
opt_csv_only = False
opt_csv_human = False
opt_usrkey = ''
opt_verbose = False
opt_cmd = True
opt_ddt = False
opt_si = False
opt_cfc0 = False
opt_n1c = False
opt_dev = False
opt_devses = '1086'
opt_exp = False
opt_dump = False
opt_can2 = False
opt_stn = False
opt_perform = False
state_scan = False
currentDDTscreen = None
ext_cur_DTC = '000000'
os = ''
language_dict = {}
bt_dev = ''
ecu_root = ''
user_data_dir = './'
db_archive_file = 'None'
cache_dir = './cache/'
log_dir = './logs/'
dumps_dir = './dumps/'
csv_dir = './csv/'
fontSize = 20
screen_orient = False

class Settings:
    port = ''
    lang = ''
    log = True
    logName = 'log.txt'
    cfc = False
    si = False
    demo = False
    fontSize = 20
    screen_orient = False
    useDump = False
    csv = False
    dev_address = ''

    def __init__(self):
        global opt_lang
        global opt_si
        global opt_log
        global opt_dump
        global fontSize
        global opt_port
        global opt_cfc0
        global screen_orient
        global opt_demo
        global opt_csv
        global opt_dev_address
        self.load()
        opt_port = self.port
        opt_lang = self.lang
        opt_si = self.si
        opt_cfc0 = self.cfc
        opt_log = self.logName
        fontSize = self.fontSize
        opt_demo = self.demo
        screen_orient = self.screen_orient
        opt_dump = self.useDump
        opt_csv = self.csv
        opt_dev_address = self.dev_address

    def __del__(self):
        self.save()

    def load(self):
        if not sysos.path.isfile(user_data_dir + '/settings.p'):
            self.save()
        try:
            f = open(user_data_dir + '/settings.p', 'rb')
            tmp_dict = pickle.load(f)
            f.close()
        except:
            sysos.remove(user_data_dir + '/settings.p')
            self.save()
            f = open(user_data_dir + '/settings.p', 'rb')
            tmp_dict = pickle.load(f)
            f.close()
        self.__dict__.update(tmp_dict)

    def save(self):
        self.port = opt_port
        self.lang = opt_lang
        self.si = opt_si
        self.cfc = opt_cfc0
        self.logName = opt_log
        self.fontSize = fontSize
        self.demo = opt_demo
        self.screen_orient = screen_orient
        self.useDump = opt_dump
        self.csv = opt_csv
        self.dev_address = opt_dev_address
        f = open(user_data_dir + '/settings.p', 'wb')
        pickle.dump(self.__dict__, f)
        f.close()
