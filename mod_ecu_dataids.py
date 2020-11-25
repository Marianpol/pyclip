#Embedded file name: /build/PyCLIP/android/app/mod_ecu_dataids.py
from mod_ecu_service import ecu_mnemolocation
from mod_utils import pyren_encode

class ecu_dataid:
    id = ''
    dataBitLength = ''
    mnemolocations = {}

    def __str__(self):
        ml = ''
        for k in self.mnemolocations.keys():
            ml = ml + str(self.mnemolocations[k])

        out = '\n  id             = %s\n  dataBitLength  = %s\n  mnemolocations = \n%s\n    ' % (self.id, self.dataBitLength, ml)
        return pyren_encode(out)

    def __init__(self, di, opt, tran):
        self.id = di.getAttribute('id')
        self.dataBitLength = di.getAttribute('dataBitLength')
        self.mnemolocations = {}
        MnemoLocations = di.getElementsByTagName('MnemoLocation')
        if MnemoLocations:
            for ml in MnemoLocations:
                mnemoloc = ecu_mnemolocation(ml)
                self.mnemolocations[mnemoloc.name] = mnemoloc


class ecu_dataids:

    def __init__(self, dataid_list, mdoc, opt, tran):
        DataIds = mdoc.getElementsByTagName('DataId')
        if DataIds:
            for di in DataIds:
                dataid = ecu_dataid(di, opt, tran)
                dataid_list[dataid.id] = dataid
