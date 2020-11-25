#Embedded file name: /build/PyCLIP/android/app/mod_zip.py
import os
import glob
import pickle
import xml.dom.minidom
import zipfile
import mod_globals
LOCATION_DIR = 'Location/'
SESSIONS_DIR = 'EcuRenault/Sessions/'
UCES_FILE = 'EcuRenault/Uces.xml'
SCENARIO_DIR = 'EcuRenault/Scenarios/'
VEHICLE_DIR = 'Vehicles/'
ARCHIVE_FILE = 'pyrendata.zip'
ZIPARCHIVE = None

def get_zip():
    global ARCHIVE_FILE
    global ZIPARCHIVE
    if ZIPARCHIVE is not None:
        return ZIPARCHIVE
    df_list = sorted(glob.glob(os.path.join(mod_globals.user_data_dir, 'pyrendata*.zip')), reverse=True)
    if len(df_list):
        ARCHIVE_FILE = df_list[0]
    else:
        df_list = sorted(glob.glob(os.path.join('./', 'pyrendata*.zip')), reverse=True)
        if len(df_list):
            ARCHIVE_FILE = df_list[0]
    if not os.path.exists(ARCHIVE_FILE):
        return
    mod_globals.db_archive_file = ARCHIVE_FILE
    print mod_globals.db_archive_file
    zf = zipfile.ZipFile(ARCHIVE_FILE, mode='r')
    ZIPARCHIVE = zf
    return zf


def get_languages_files():
    zf = get_zip()
    ret = []
    for name in zf.namelist():
        if name.startswith(LOCATION_DIR) and '.p' in name:
            ret.append(name)

    return ret


def get_languages():
    ret = []
    lf = get_languages_files()
    for name in lf:
        ret.append(name[19:].replace('.p', ''))

    return ret


def get_uces():
    zf = get_zip()
    file = UCES_FILE
    data = zf.read(file)
    return data


def get_xml_file(name):
    zf = get_zip()
    filename = SESSIONS_DIR + name
    return xml.dom.minidom.parseString(zf.read(filename))


def get_xml_scenario(name):
    zf = get_zip()
    filename = SCENARIO_DIR + name
    return xml.dom.minidom.parseString(zf.read(filename))


def get_xml(filename):
    zf = get_zip()
    return xml.dom.minidom.parseString(zf.read(filename))


def get_file_content(name):
    zf = get_zip()
    filename = SESSIONS_DIR + name
    return zf.read(filename)


def get_ecu_p(name):
    zf = get_zip()
    filename = SESSIONS_DIR + name
    return pickle.loads(zf.read(filename))


def get_tcoms():
    zf = get_zip()
    ret = []
    for name in zf.namelist():
        if name.startswith(VEHICLE_DIR + 'TCOM_'):
            ret.append(name)

    return ret


def get_lang_file_dict(name):
    zf = get_zip()
    filename = LOCATION_DIR + name
    if filename not in zf.namelist():
        return None
    data = pickle.loads(zf.read(filename))
    return data


def get_lang_dict(lang):
    pref = get_languages_files()[0][9:19]
    return get_lang_file_dict(pref + lang + '.p')


if __name__ == '__main__':
    exit()
