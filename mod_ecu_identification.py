#Embedded file name: /build/PyCLIP/android/app/mod_ecu_identification.py
import xml.dom.minidom
from xml.dom.minidom import parse
import mod_globals
from mod_ecu_mnemonic import *

def get_identification(id, mn, se, elm, calc, no_formatting = False):
    comp = id.computation
    comp = comp.replace('&amp;', '&')
    for m in sorted(id.mnemolist, key=len, reverse=True):
        hex_val = get_mnemonic(mn[m], se, elm)
        comp = comp.replace(m, hex_val)

    id.value = calc.calculate(comp)
    if id.type == 'CSTRING' and type(id.value) is str:
        id.value = id.value.decode('ascii', 'ignore')
    if no_formatting:
        return (id.name, id.codeMR, id.label, id.value)
    elif mod_globals.os == 'android':
        return ('%-6s %-40s %-20s' % (id.codeMR, id.label, id.value), id.helps, id.value)
    else:
        return ('%-6s %-50s %-20s' % (id.codeMR, id.label, id.value), id.helps, id.value)


class ecu_identification:
    name = ''
    agcdRef = ''
    codeMR = ''
    mask = ''
    label = ''
    value = ''
    type = ''
    helps = []
    caracter = {}
    computation = ''
    mnemolist = []

    def __init__(self, st, opt, tran):
        self.name = st.getAttribute('name')
        self.agcdRef = st.getAttribute('agcdRef')
        self.codeMR = st.getAttribute('codeMR')
        Mask = st.getElementsByTagName("Mask")
        if Mask:
            self.mask = Mask.item(0).getAttribute("value")
        Label = st.getElementsByTagName('Label')
        codetext = Label.item(0).getAttribute('codetext')
        defaultText = Label.item(0).getAttribute('defaultText')
        self.label = ''
        if codetext:
            if codetext in tran.keys():
                self.label = tran[codetext]
            elif defaultText:
                self.label = defaultText
        self.helps = []
        Helps = st.getElementsByTagName('Helps')
        if Helps:
            for hl in Helps:
                Lines = hl.getElementsByTagName('Line')
                if Lines:
                    for ln in Lines:
                        line = ''
                        Label = ln.getElementsByTagName('Label')
                        if Label:
                            for la in Label:
                                codetext = la.getAttribute('codetext')
                                defaultText = la.getAttribute('defaultText')
                                if codetext:
                                    if codetext in tran.keys():
                                        line = line + tran[codetext]
                                    elif defaultText:
                                        line = line + defaultText

                        self.helps.append(line + '\n')

        xmlstr = opt['Identification\\' + self.name]
        odom = xml.dom.minidom.parseString(xmlstr.encode('utf-8'))
        odoc = odom.documentElement
        self.computation = ''
        Computation = odoc.getElementsByTagName('Computation')
        if Computation:
            for cmpt in Computation:
                self.type = cmpt.getAttribute('type')
                tmp = cmpt.getElementsByTagName('Value').item(0).firstChild.nodeValue
                tmp = tmp.replace(" ","").replace("&amp;","&")
                
                questionMarkCount = tmp.count('?"')
                if questionMarkCount:
                    tmp = self.changeHwNumberComputation(tmp, questionMarkCount)
                
                self.computation = tmp
                self.mnemolist = []
                Mnemo = cmpt.getElementsByTagName('Mnemo')
                if Mnemo:
                    for mn in Mnemo:
                        self.mnemolist.append(mn.getAttribute('name'))

    def changeHwNumberComputation(self, comp, counter):
        firstPos = 0
        lastPos = 0
        for num in range(counter):
            firstPos = comp.find('?"', lastPos + 1)
            if(comp[firstPos-1] != ')'):
                mnemonicBegin = comp.rfind('(', lastPos ,firstPos)
                mnemonicSubstring = comp[mnemonicBegin:firstPos]
                if mnemonicSubstring.count('(') > 1: 
                    return comp
                comp = comp.replace(mnemonicSubstring, '('+ mnemonicSubstring + ')')
                lastPos = firstPos + 2
        return comp 

class ecu_identifications:

    def __init__(self, identification_list, mdoc, opt, tran):
        Identifications = mdoc.getElementsByTagName('Identification')
        if Identifications:
            for id in Identifications:
                identification = ecu_identification(id, opt, tran)
                identification_list[identification.name] = identification
