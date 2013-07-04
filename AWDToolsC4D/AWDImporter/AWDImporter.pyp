import os
import sys

# add this plugin to the python search path
folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)
    
import c4d
    
from awdimporter import ids
from awdimporter import cmddata
from awdimporter import maindialog

#access to the *.res or *.str files
maindialog.__res__ = __res__


#register the plugin
if __name__ == "__main__":

    iconID = 1390383
    icon2 = c4d.bitmaps.BaseBitmap()
    icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "importerPic.png"))
    c4d.gui.RegisterIcon(iconID,icon2)
    # load an icon from the 'res' folder
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), "res", "icon.tif"))
    
    # get the plugin title from the string resource
    title = c4d.plugins.GeLoadString(ids.STR_TITLE)
        
    c4d.plugins.RegisterCommandPlugin(ids.PLUGINID, title, 0, icon, title, cmddata.CMDData())