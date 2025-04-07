import psd_tools
from psd_tools.psd.header import FileHeader
from psd_tools.constants import ColorMode

class PsdPsb(psd_tools.PSDImage):

    def getDesignSize(self):
        
