#Embedded file name: /build/PyCLIP/android/app/mod_ecu_command.py
import string
import xml.dom.minidom
from xml.dom.minidom import parse
from kivy.app import App
from kivy.base import EventLoop
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from mod_ecu_identification import get_identification
from mod_ecu_parameter import get_parameter
from mod_ecu_scenario import playScenario
from mod_ecu_screen import *
from mod_ecu_service import *
from mod_ecu_state import get_state
from mod_utils import hex_VIN_plus_CRC
from mod_utils import StringToIntToHex
from mod_utils import ASCIITOHEX
fmn = 1.7
bmn = 2.5

Window.softinput_mode = 'below_target'

def runCommand(command, ecu, elm, param = '', cmdt = 'HEX'):
    isService = 0
    isParam = 0
    isInputList = 0
    if len(command.scenario):
        print 'It is scenarium. I do not support them!!!\n'
        return
    if len(command.inputlist.keys()):
        isInputList = 1
    for si in command.serviceID:
        isService = 1
        service = ecu.Services[si]
        if len(service.params):
            isParam += len(service.params)

    if len(command.datarefs):
        print
        print '#' * 26, ' Current values ', '#' * 26
        print ''
        strlst = []
        elm.clear_cache()
        for dr in command.datarefs:
            datastr = dr.name
            help = dr.type
            if dr.type == 'State':
                datastr, help, csvd = get_state(ecu.States[dr.name], ecu.Mnemonics, ecu.Services, ecu.elm, ecu.calc)
            if dr.type == 'Parameter':
                datastr, help, csvd = get_parameter(ecu.Parameters[dr.name], ecu.Mnemonics, ecu.Services, ecu.elm, ecu.calc)
            if dr.type == 'Identification':
                datastr, help = get_identification(ecu.Identifications[dr.name], ecu.Mnemonics, ecu.Services, ecu.elm, ecu.calc)
            print pyren_encode(datastr)

        print ''
        print '#' * 70
        print ''
    chosenParameter = ''
    if isInputList and param not in command.inputlist.keys():
        print "Not valid parameter. It isn't in inputList"
        return
    summary = ''
    for si in command.serviceID:
        service = ecu.Services[si]
        if len(service.params) == 1 and chosenParameter == '':
            if len(service.params[0]['size']):
                parsize = int(service.params[0]['size'])
            else:
                parsize = 0
            ch = param
            ch = ch.strip().upper()
            if cmdt == 'HEX' and all((c in string.hexdigits for c in ch)) and len(ch) % 2 == 0:
                if parsize > 0 and len(ch) != parsize * 2:
                    continue
                chosenParameter = ch
            if cmdt == 'VIN' and len(ch) == 17 and 'I' not in ch and 'O' not in ch:
                chosenParameter = hex_VIN_plus_CRC(ch)
        if len(service.params) == 1:
            ostr = 'cmd:' + service.startReq + chosenParameter
            print pyren_encode('%-35s ' % ostr),
            resp = executeService(service, elm, command.caracter, chosenParameter, False)
        elif len(service.params) == 0:
            ostr = ('cmd:' + service.startReq,)
            print pyren_encode('%-35s ' % ostr),
            resp = executeService(service, elm, command.caracter, '', False)
        print 'rsp:', resp
        summary = summary + resp + '\n'

    return summary


def getDataId(req, ecu, elm):
    if not req.upper().startswith('2E'):
        return ('', '')
    dataid = req[2:]
    if dataid not in ecu.DataIds.keys():
        return ('', '')
    getdatareq = '22' + dataid
    rsp = elm.request(getdatareq, '', False, 0)
    rsp = rsp.replace(' ', '')
    if not rsp.upper().startswith('62' + dataid):
        return ('', '')
    data = rsp.replace('62' + dataid, '')
    datalen = int(ecu.DataIds[dataid].dataBitLength) / 4
    if len(data) < datalen:
        return ('', '')
    return (dataid, data[:datalen])


def packData(ecu, mnemo, dataid, data, value):
    di = ecu.DataIds[dataid]
    if mnemo not in di.mnemolocations.keys():
        return value
    pr = di.mnemolocations[mnemo]
    mn = ecu.Mnemonics[mnemo]
    littleEndian = True if int(mn.littleEndian) else False
    sb = int(pr.startByte) - 1
    bits = int(mn.bitsLength)
    sbit = int(pr.startBit)
    bytes = (bits + sbit - 1) / 8 + 1
    if littleEndian:
        lshift = sbit
    else:
        lshift = ((bytes + 1) * 8 - (bits + sbit)) % 8
    val = int(value, 16)
    val = (val & 2 ** bits - 1) << lshift
    value = hex(val)[2:]
    if value[-1:].upper() == 'L':
        value = value[:-1]
    if len(value) % 2:
        value = '0' + value
    if value.upper().startswith('0X'):
        value = value[2:]
    value = value.zfill(bytes * 2).upper()
    if not all((c in string.hexdigits for c in value)) and len(value) == bytes * 2:
        return 'ERROR: Wrong value'
    base = data[sb * 2:(sb + bytes) * 2]
    binbase = int(base, 16)
    binvalue = int(value, 16)
    mask = 2 ** bits - 1 << lshift
    binvalue = binbase ^ mask & binbase | binvalue
    value = hex(binvalue)[2:].upper()
    if value[-1:].upper() == 'L':
        value = value[:-1]
    value = value[-bytes * 2:].zfill(bytes * 2)
    data = data[0:sb * 2] + value + data[(sb + bytes) * 2:]
    return data


class MyLabelBlue(Label):

    def __init__(self, **kwargs):
        super(MyLabelBlue, self).__init__(**kwargs)
        self.bind(size=self.setter('text_size'))

    def on_size(self, *args):
        if not self.canvas:
            return
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 1, 0.25)
            Rectangle(pos=self.pos, size=self.size)


class MyLabelGreen(Label):

    def __init__(self, **kwargs):
        super(MyLabelGreen, self).__init__(**kwargs)
        self.bind(size=self.setter('text_size'))

    def on_size(self, *args):
        if not self.canvas:
            return
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=self.pos, size=self.size)


class kivyExecCommand(App):

    def __init__(self, command, ecu, elm, path):
        self.command = command
        self.ecu = ecu
        self.elm = elm
        self.path = path
        self.ok = False
        self.popup = None
        super(kivyExecCommand, self).__init__()

    # def on_pause(self):
    #     exit()

    # def on_resume(self):
    #     self.ecu.elm.send_cmd(self.ecu.ecudata['startDiagReq'])

    def make_box(self, str1, str2):
        label1 = MyLabelBlue(text=str1, halign='left', size_hint=(0.35, 1))
        label2 = MyLabelGreen(text=str2, halign='center', size_hint=(0.65, 1))
        glay = GridLayout(cols=2, height=mod_globals.fontSize * fmn, size_hint=(1, None), spacing=(5, 5))
        glay.add_widget(label1)
        glay.add_widget(label2)
        return glay

    def back(self, instance):
        self.stop()

    def popup_validate(self, instance):
        error = ''
        chosenParameter = self.chosenParameter
        self.popup.dismiss()
        lbltxt = Label(text='Changing configuration...')
        popup2 = Popup(title='Working', content=lbltxt, size=(400, 400), size_hint=(None, None))
        popup2.open()
        EventLoop.idle()
        responses = 'Response :\n'
        i = 0
        for si in self.command.serviceID:
            service = self.ecu.Services[si]
            if len(service.params) == 1 and chosenParameter == '':
                cmdt = self.selectedButton
                if len(service.params[0]['size']):
                    parsize = int(service.params[0]['size'])
                else:
                    parsize = 0
                while True:
                    ch = self.userInput.text
                    ch = ch.strip().upper()
                    if cmdt == 'HEX' and all((c in string.hexdigits for c in ch)) and len(ch) % 2 == 0:
                        if parsize > 0 and len(ch) != parsize * 2:
                            error = 'Too long value'
                        chosenParameter = ch
                    elif cmdt == 'VIN' and len(ch) == 17 and 'I' not in ch and 'O' not in ch:
                        chosenParameter = hex_VIN_plus_CRC(ch)
                    elif cmdt=='DEC' and all (c in string.digits for c in ch) and len(ch):
                        chosenParameter = StringToIntToHex(ch)
                        if parsize > 0 and len(chosenParameter) > parsize * 2:
                            error = 'Too long value'
                        if parsize>0 and len(chosenParameter)<parsize*2:
                            chosenParameter = '0'*(parsize*2 - len(chosenParameter)) + chosenParameter
                    elif cmdt=='ASCII':
                        chosenParameter = ASCIITOHEX(ch)
                        if parsize > 0 and len(chosenParameter) > parsize * 2:
                            error = 'Too long value'
                        if parsize>0 and len(chosenParameter)<parsize*2:
                            chosenParameter = '0'*(parsize*2 - len(chosenParameter)) + chosenParameter
                    else:
                        error = 'Error in input data'
                    break
            
            if not error:
                if len(service.params) == 1 and chosenParameter:
                    resp = executeService(service, self.elm, self.command.caracter, chosenParameter, False)
                elif len(service.params) == 0:
                    resp = executeService(service, self.elm, self.command.caracter, '', False)
                lbltxt.text = 'Sending ' + service.startReq
                EventLoop.idle()
                responses += '%i : %s\n' % (i, resp)
                i += 1

        popup2.dismiss()
        if error:
            popup = Popup(title='ERROR', content=Label(text=error), size=(400, 400), size_hint=(None, None))
        else:
            popup = Popup(title='Done', content=Label(text=responses), size=(400, 400), size_hint=(None, None))
        popup.open()

    def exec_command(self, instance):
        self.chosenParameter = instance.paramid
        box = BoxLayout(orientation='vertical', padding=10)
        self.popup = Popup(title='Proceed ?', title_size=30, title_align='center', content=box, size_hint=(0.5, 0.5), auto_dismiss=True)
        box.add_widget(Button(text='ACCEPT', on_press=self.popup_validate, height=mod_globals.fontSize * bmn * 3, size_hint_y=None))
        box.add_widget(Button(text='CANCEL', on_press=self.popup.dismiss, height=mod_globals.fontSize * bmn * 3, size_hint_y=None))
        self.popup.open()

    def build_datarefs(self, layout):
        if len(self.command.datarefs):
            self.elm.clear_cache()
            for dr in self.command.datarefs:
                datastr = dr.name
                help = dr.type
                if dr.type == 'State':
                    name, code, label, value, csvd = get_state(self.ecu.States[dr.name], self.ecu.Mnemonics, self.ecu.Services, self.ecu.elm, self.ecu.calc, True)
                    codelabel = '%s - %s' % (code, label)
                    layout.add_widget(self.make_box(codelabel, value))
                if dr.type == 'Parameter':
                    name, codeMR, label, value, unit, csvd = get_parameter(self.ecu.Parameters[dr.name], self.ecu.Mnemonics, self.ecu.Services, self.ecu.elm, self.ecu.calc, True)
                    codelabel = '%s - %s' % (codeMR, label)
                    valuestr = '%s %s' % (value, unit)
                    layout.add_widget(self.make_box(codelabel, valuestr))
                if dr.type == 'Identification':
                    name, code, label, value = get_identification(self.ecu.Identifications[dr.name], self.ecu.Mnemonics, self.ecu.Services, self.ecu.elm, self.ecu.calc, True)
                    codelabel = '%s - %s' % (code, label)
                    layout.add_widget(self.make_box(codelabel, value))

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.stop()
            return True
    
    def changeInputStyle(self, show):
        if show:
            self.btn.disabled = False
            # self.userInput.readonly = False
            self.userInput.background_color = [1,1,1,1]
        else:
            self.btn.disabled = True
            # self.userInput.readonly = True
            self.userInput.background_normal = ''
            self.userInput.background_color = [0.55,0.55,0.55,1]

    def changeButtonStyle(self, inst):
        selectedColor = [0, 0.345, 0, 1]
        notSelectedColor = [0.345,0.345,0.345,1]
        selectedButtonText = ''
        selectedButton = ''
        selectedButtonNum = 0
        for num in range(len(self.typeButtons)):
            if self.typeButtons[num].background_color == selectedColor:
                selectedButtonText = self.typeButtons[num].text
                selectedButtonNum = num
                break
        if not selectedButtonText or (inst.text != selectedButtonText and not inst.background_color == selectedColor):
            inst.background_normal = ''
            inst.background_color = selectedColor
            self.changeInputStyle(True)
        if selectedButtonText:
            self.typeButtons[selectedButtonNum].background_normal = ''
            self.typeButtons[selectedButtonNum].background_color = notSelectedColor
        
        selectedButtonText = ''
        for num in range(len(self.typeButtons)):
            if self.typeButtons[num].background_color == selectedColor:
                selectedButtonText = inst.text
        if not selectedButtonText:
            self.changeInputStyle(False)
        self.selectedButton = selectedButtonText

    def build(self):
        layout = GridLayout(cols=1, padding=5, spacing=(5, 5), size_hint=(1, None))
        layout.bind(minimum_height=layout.setter('height'))
        titlelabel = Label(text=pyren_encode(self.path), size_hint=(1, None), halign='center', height=mod_globals.fontSize * fmn * 2)
        layout.add_widget(titlelabel)
        if len(self.command.prerequisite) > 0:
            lines = len(self.command.prerequisite.split('\n'))
            simb = len(self.command.prerequisite)
            if lines < simb / 60:
                lines = simb / 60
            if lines < 7:
                lines = 7
            if lines > 20:
                lines = 20
            prelabel = TextInput(text=pyren_encode(self.command.prerequisite), size_hint=(1, None), multiline=True, height=mod_globals.fontSize * fmn * lines, readonly=True, foreground_color=[1,
             0,
             0,
             1], background_color=[0,
             0,
             0,
             1])
            layout.add_widget(prelabel)
        layout.add_widget(self.make_box('name', self.command.name))
        layout.add_widget(self.make_box('label', pyren_encode(self.command.label)))
        layout.add_widget(self.make_box('scenario', self.command.scenario))
        has_scenario = False
        if self.command.scenario:
            has_scenario = True
        self.build_datarefs(layout)
        has_param = False
        if len(self.command.serviceID):
            layout.add_widget(MyLabelGreen(text='Services ID', size_hint=(1, None), height=mod_globals.fontSize * fmn, halign='center'))
            for si in self.command.serviceID:
                service = self.ecu.Services[si]
                if len(service.params) == 0:
                    txt = '[%s] %s' % (si, service.startReq)
                else:
                    has_param = True
                    txt = '[%s] %s <Params>' % (si, service.startReq)
                svcidlbl = MyLabelBlue(text=txt, size_hint=(1, None), height=mod_globals.fontSize * fmn, font_size=mod_globals.fontSize, halign='center')
                layout.add_widget(svcidlbl)

        for val, key in self.command.inputlist.iteritems():
            btnname = '(%s) - %s' % (val, key)
            configbtn = Button(text=btnname, height=80, size_hint=(1, None))
            configbtn.bind(on_press=self.exec_command)
            configbtn.paramid = val
            layout.add_widget(configbtn)

        if has_scenario:
            btn = Button(text='/!\\ SCENARIO NOT SUPPORTED YET /!\\', height=mod_globals.fontSize * bmn, size_hint=(1, None))
            layout.add_widget(btn)
        if has_param and not self.command.inputlist and not has_scenario:
            self.userInput = TextInput(multiline=False, height=mod_globals.fontSize * 3, size_hint=(1, None), background_color=(0.55,0.55,0.55,1))
            hexBtn = Button(text='HEX', height=mod_globals.fontSize * bmn, size_hint=(1, None), on_press=lambda instance: self.changeButtonStyle(instance))
            decBtn = Button(text='DEC', height=mod_globals.fontSize * bmn, size_hint=(1, None), on_press=lambda instance: self.changeButtonStyle(instance))
            asciiBtn = Button(text='ASCII', height=mod_globals.fontSize * bmn, size_hint=(1, None), on_press=lambda instance: self.changeButtonStyle(instance))
            vinBtn = Button(text='VIN', height=mod_globals.fontSize * bmn, size_hint=(1, None), on_press=lambda instance: self.changeButtonStyle(instance))
            self.typeButtons = [hexBtn,decBtn,asciiBtn,vinBtn] 
            layout.add_widget(hexBtn)
            layout.add_widget(decBtn)
            layout.add_widget(asciiBtn)
            layout.add_widget(vinBtn)
            layout.add_widget(self.userInput)
            self.btn = Button(text='<EXECUTE>', height=mod_globals.fontSize * bmn, size_hint=(1, None), disabled = True)
            self.btn.paramid = ''
            self.btn.bind(on_press=self.exec_command)
            layout.add_widget(self.btn)
        if not has_param and not has_scenario:
            btn = Button(text='<EXECUTE>', height=mod_globals.fontSize * bmn, size_hint=(1, None))
            btn.paramid = None
            btn.bind(on_press=self.exec_command)
            layout.add_widget(btn)
        btn = Button(text='<CANCEL>', height=mod_globals.fontSize * bmn, size_hint=(1.0, None))
        btn.bind(on_press=self.back)
        layout.add_widget(btn)
        root = ScrollView(size_hint=(1, 1), pos_hint={'center_x': 0.5,
         'center_y': 0.5}, do_scroll_x=False)
        root.add_widget(layout)
        return root


def executeCommandGui(command, ecu, elm, path):
    gui = kivyExecCommand(command, ecu, elm, path)
    gui.run()


def executeCommand(command, ecu, elm, path):
    if len(command.scenario):
        if playScenario(command, ecu, elm) == True:
            return
    return executeCommandGui(command, ecu, elm, path)


class ecu_command:
    name = ''
    agcdRef = ''
    codeMR = ''
    mask = ''
    type = ''
    label = ''
    prerequisite = ''
    datarefs = []
    caracter = {}
    inputlist = {}
    serviceID = []
    scenario = ''

    def __init__(self, co, opt, tran):
        self.name = co.getAttribute('name')
        self.agcdRef = co.getAttribute('agcdRef')
        self.codeMR = co.getAttribute('codeMR')
        if not self.codeMR:
            self.codeMR = self.name
        self.type = co.getAttribute('type')
        Mask = co.getElementsByTagName("Mask")
        if Mask:
            self.mask = Mask.item(0).getAttribute("value")
        Label = co.getElementsByTagName('Label')
        codetext = Label.item(0).getAttribute('codetext')
        defaultText = Label.item(0).getAttribute('defaultText')
        self.label = ''
        if codetext:
            if codetext in tran.keys():
                self.label = tran[codetext]
            elif defaultText:
                self.label = defaultText
        Prereq = co.getElementsByTagName('PrerequisiteMessage')
        if Prereq:
            codetext = Prereq.item(0).getAttribute('codetext')
            defaultText = Prereq.item(0).getAttribute('defaultText')
            self.prerequisite = ''
            if codetext:
                if codetext in tran.keys():
                    self.prerequisite = tran[codetext]
                elif defaultText:
                    self.prerequisite = defaultText
        scenario_tmp = co.getElementsByTagName('Scenario')
        if scenario_tmp:
            scenario_fc = scenario_tmp.item(0).firstChild
            if scenario_fc:
                self.scenario = scenario_fc.nodeValue
            else:
                self.scenario = ''
        self.datarefs = []
        CurrentInfo = co.getElementsByTagName('DataList')
        if CurrentInfo:
            for ci in CurrentInfo:
                DataRef = ci.getElementsByTagName('DataRef')
                if DataRef:
                    for dr in DataRef:
                        dataref = ecu_screen_dataref(dr)
                        self.datarefs.append(dataref)

        self.inputlist = {}
        InputList = co.getElementsByTagName('InputList')
        if InputList:
            for corIL in InputList:
                CorrespondanceIL = corIL.getElementsByTagName('Correspondance')
                if CorrespondanceIL:
                    for cil in CorrespondanceIL:
                        ivalue = cil.getAttribute('value')
                        codetext = cil.getAttribute('codetext')
                        defaultText = cil.getAttribute('defaultText')
                        itext = ''
                        if codetext:
                            if codetext in tran.keys():
                                itext = tran[codetext]
                            elif defaultText:
                                itext = defaultText
                            self.inputlist[ivalue] = itext

        self.caracter = {}
        Interpretation = co.getElementsByTagName('StatusInterpretation')
        if Interpretation:
            for corIT in Interpretation:
                CorrespondanceSI = corIT.getElementsByTagName('Correspondance')
                if CorrespondanceSI:
                    for co in CorrespondanceSI:
                        ivalue = co.getAttribute('value')
                        codetext = co.getAttribute('codetext')
                        defaultText = co.getAttribute('defaultText')
                        itext = ''
                        if codetext:
                            if codetext in tran.keys():
                                itext = tran[codetext]
                            elif defaultText:
                                itext = defaultText
                            self.caracter[ivalue] = itext

        if 'Command\\' + self.name not in opt.keys():
            return
        xmlstr = opt['Command\\' + self.name]
        odom = xml.dom.minidom.parseString(xmlstr.encode('utf-8'))
        odoc = odom.documentElement
        self.computation = ''
        self.serviceID = []
        ServiceID = odoc.getElementsByTagName('ServiceID')
        if ServiceID:
            for sid in ServiceID:
                self.serviceID.append(sid.getAttribute('name'))


class ecu_commands:

    def __init__(self, command_list, mdoc, opt, tran):
        commands = mdoc.getElementsByTagName('Command')
        if commands:
            for co in commands:
                command = ecu_command(co, opt, tran)
                command_list[command.name] = command
