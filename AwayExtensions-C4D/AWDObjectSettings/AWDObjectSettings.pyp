#AWD Object Settings (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

#be sure to use a unique ID obtained from www.plugincafe.com
PLUGIN_ID = 1028905    #ID for the tag

DAPE_APPLYTOCHILDS       = 1016
DAPE_EXPORT              = 1014

# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDObjectSettingsXpression(plugins.TagData):

    def Init(self,op):
        #print("init")
        bc = op.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(DAPE_APPLYTOCHILDS,True)
        bc.SetBool(DAPE_EXPORT,False)
        op.SetData(bc)
        return True

# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Object Settings", g=AWDObjectSettingsXpression, description="AWDObjectSettings", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)