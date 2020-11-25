#Embedded file name: /build/PyCLIP/android/app/scen_ecri_codevin.py
import os
import sys
import re
import time
import mod_globals
import mod_utils
import mod_ecu
import mod_zip
from mod_utils import pyren_encode
from mod_utils import clearScreen
from mod_utils import hex_VIN_plus_CRC
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

class MyLabel(Label):

    def __init__(self, **kwargs):
        if 'bgcolor' in kwargs:
            self.bgcolor = kwargs['bgcolor']
        else:
            self.bgcolor = (0, 0, 0, 0)
        super(MyLabel, self).__init__(**kwargs)
        self.bind(size=self.setter('text_size'))
        self.halign = 'center'
        self.valign = 'middle'
        if 'size_hint' not in kwargs:
            self.size_hint = (1, None)
        if 'height' not in kwargs:
            self.height = 50

    def on_size(self, *args):
        if not self.canvas:
            return
        self.canvas.before.clear()
        with self.canvas.before:
            Color(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2], self.bgcolor[3])
            Rectangle(pos=self.pos, size=self.size)


class VinWrite(App):

    def __init__(self, **kwargs):
        DOMTree = mod_zip.get_xml_scenario(kwargs['data'])
        self.ScmRoom = DOMTree.documentElement
        ScmParams = self.ScmRoom.getElementsByTagName('ScmParam')
        ScmSets = self.ScmRoom.getElementsByTagName('ScmSet')
        self.elm = kwargs['elm']
        self.command = kwargs['command']
        self.ecu = kwargs['ecu']
        self.ScmParam = {}
        self.ScmSet = {}
        for Param in ScmParams:
            name = pyren_encode(Param.getAttribute('name'))
            value = pyren_encode(Param.getAttribute('value'))
            self.ScmParam[name] = value

        for Set in ScmSets:
            setname = pyren_encode(mod_globals.language_dict[Set.getAttribute('name')])
            ScmParams = Set.getElementsByTagName('ScmParam')
            for Param in ScmParams:
                name = pyren_encode(Param.getAttribute('name'))
                value = pyren_encode(Param.getAttribute('value'))
                self.ScmSet[setname] = value
                self.ScmParam[name] = value

        super(VinWrite, self).__init__(**kwargs)

    def build(self):
        header = '[' + self.command.codeMR + '] ' + self.command.label
        codemr, label, value = self.ecu.get_id(self.ScmParam['identVIN'], True)
        codemr = '%s : %s' % (pyren_encode(codemr), pyren_encode(label))
        self.vin_input = TextInput(text='VF', multiline=False, size_hint=(1, None), height=40)
        root = GridLayout(cols=1, spacing=6)
        layout_current = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        layout_current.add_widget(MyLabel(text=codemr, size_hint=(0.3, 1), bgcolor=(0, 0, 1, 0.3)))
        layout_current.add_widget(MyLabel(text=value, size_hint=(0.7, 1), bgcolor=(0, 1, 0, 0.3)))
        root.add_widget(MyLabel(text=header))
        root.add_widget(MyLabel(text=self.get_message('TextTitre')))
        root.add_widget(MyLabel(text=self.get_message('MessageBox3'), height=100, bgcolor=(1, 0, 0, 0.3)))
        root.add_widget(layout_current)
        root.add_widget(self.vin_input)
        root.add_widget(Button(text='WRITE VIN', on_press=self.write_vin, size_hint=(1, None), height=80))
        root.add_widget(Button(text='CANCEL', on_press=self.stop, size_hint=(1, None), height=80))
        return root

    def write_vin(self, instance):
        vin = self.vin_input.text.upper()
        if not (len(vin) == 17 and 'I' not in vin and 'O' not in vin):
            popup = Popup(title='Status', content=Label(text='Invalid VIN'), auto_dismiss=True, size=(500, 500), size_hint=(None, None))
            popup.open()
            return None
        vin_crc = hex_VIN_plus_CRC(vin)
        self.ecu.run_cmd(self.ScmParam['ConfigurationName'], vin_crc)
        popup = Popup(title='Status', content=Label(text='VIN CHANGED'), auto_dismiss=True, size=(500, 500), size_hint=(None, None))
        popup.open()

    def get_message(self, msg):
        if msg in self.ScmParam.keys():
            value = self.ScmParam[msg]
        else:
            value = msg
        if value.isdigit() and value in mod_globals.language_dict.keys():
            value = pyren_encode(mod_globals.language_dict[value])
        return value

    def get_message_by_id(self, id):
        if id.isdigit() and id in mod_globals.language_dict.keys():
            value = pyren_encode(mod_globals.language_dict[id])
        return value


def run(elm, ecu, command, data):
    app = VinWrite(elm=elm, ecu=ecu, command=command, data=data)
    app.run()
