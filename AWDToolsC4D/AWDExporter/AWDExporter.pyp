"""
Cinema4D AWD Exporter 2013 by 80prozent[a]differentdesign.de

This Plugin exports C4D-Scenes to Away3d 4 using the AWD2-File-Format

Enjoy!

"""

import os
import sys
import c4d

folder = os.path.dirname(__file__)
if folder not in sys.path:
    sys.path.insert(0, folder)

from awdexporter import ids
from awdexporter import cmddata
from awdexporter import maindialog
from awdexporter import mainHelpers   
from awdexporter import mainExporter
from awdexporter import maindialogCreator
 
# listen for any C4D internal messages that will indicate that the background-thread have to be closed 
def PluginMessage(id, data):
    if id==c4d.C4DPL_ENDPROGRAM or id==c4d.C4DPL_ENDACTIVITY:
        if maindialog.workerThread!=None:
            #print "Plugin:AWDExporter = One WorkerThread found = "+str(maindialog.workerThread)+" !"
            if maindialog.workerThread.IsRunning():
                #print "Plugin:AWDExporter = WorkerThread ("+str(maindialog.workerThread)+") is running, and gets shut down"
                maindialog.workerThread.End(False)   
            maindialog.workerThread=None
        return True
    return False

# this needs to be done for each module that needs to acces the "c4d.plugins.GeLoadString(id)"
maindialog.__res__ = __res__
mainExporter.__res__ = __res__
mainHelpers.__res__ = __res__
maindialogCreator.__res__ = __res__

# main plugin code:
if __name__ == "__main__":

#register a pic for display withhin the plugin:
    iconID = 1390382
    icon2 = c4d.bitmaps.BaseBitmap()
    icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "exporterPic.png"))
    c4d.gui.RegisterIcon(iconID,icon2)

#register a icon for the plugin:
    icon = c4d.bitmaps.BaseBitmap()
    icon.InitWith(os.path.join(os.path.dirname(__file__), "res", "icon.tif"))
   
#set the title for the plugin (multi-lingual) 
    title = c4d.plugins.GeLoadString(ids.STR_TITLE)
        
#register the plugin as a Commandline Plugin.   
    c4d.plugins.RegisterCommandPlugin(ids.PLUGINID, title, 0, icon, title, cmddata.CMDData())