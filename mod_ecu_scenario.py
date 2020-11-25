#Embedded file name: /build/PyCLIP/android/app/mod_ecu_scenario.py
import os
import re
import mod_globals
from mod_utils import pyren_encode

def playScenario(command, ecu, elm):
    services = ecu.Services
    scenarioName, scenarioData = command.scenario.split('#')
    if scenarioName.lower().startswith('scm'):
        scenarioName = scenarioName.split(':')[1]
        ecuNumberPattern = re.compile(r'\d{5}')
        ecuNumberIndex = ecuNumberPattern.search(scenarioData)
        scenarioName = scenarioData[:scenarioData.find(ecuNumberIndex.group(0)) - 1].lower()
    try:
        scen = __import__(scenarioName)
        scen.run(elm, ecu, command, scenarioData)
        return True
    except:
        return False

    print '\nThere is scenarium. I do not support them!!!\n'
    ch = raw_input('Press ENTER to exit ')
    if 'show' not in ch:
        return
    if not os.path.isfile(path + scenarioData):
        return
    lines = [ line.rstrip('\n') for line in open(path + scenarioData) ]
    for l in lines:
        pa = re.compile('name=\\"(\\w+)\\"\\s+value=\\"(\\w+)\\"')
        ma = pa.search(l)
        if ma:
            p_name = ma.group(1)
            p_value = ma.group(2)
            if p_value.isdigit() and p_value in mod_globals.language_dict.keys():
                p_value = mod_globals.language_dict[p_value]
            print pyren_encode('  %-20s : %s' % (p_name, p_value))
        else:
            print pyren_encode(l.decode('utf-8', 'replace'))

    ch = raw_input('Press ENTER to exit')
