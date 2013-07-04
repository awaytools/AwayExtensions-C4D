
# some classes tio help with the dialog management 

import c4d
from awdexporter import ids    
import urllib2
from xml.dom import minidom
import xml.dom.minidom as dom


def loadVersionFilefromNet():
    req = urllib2.Request("http://www.differentdesign.de/awdtoolsc4dversion.xml")
    try:
        response = urllib2.urlopen(req)
    except:
        c4d.gui.MessageDialog("cannot connect to the server")
        return ""
    datei = response
    outputString=""
    if datei is None:  
        c4d.gui.MessageDialog("cannot not load the online versionfile")  
    if datei is not None:               
        dom1 = dom.parse(datei) 
        outputString+=dom1.firstChild.getAttribute("Major")+"."
        outputString+=dom1.firstChild.getAttribute("Minor")+"."
        outputString+=dom1.firstChild.getAttribute("Revision")+" - "
        outputString+=dom1.firstChild.getAttribute("Message")+"\n"
    return outputString

def loadVersionFile(datei):
    outputString=""
    if datei is None:  
        c4d.gui.MessageDialog("cannot find the local versionfile")  
    if datei is not None:             
        dom1 = dom.parse(datei) 
        outputString+=dom1.firstChild.getAttribute("Major")+"."
        outputString+=dom1.firstChild.getAttribute("Minor")+"."
        outputString+=dom1.firstChild.getAttribute("Revision")+" - "
        outputString+=dom1.firstChild.getAttribute("Message")+"\n"
    return outputString

def InitValues(mainDialog): 
        
    mainDialog.awdExporterData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
    if mainDialog.awdExporterData:

        if mainDialog.awdExporterData[ids.REAL_SCALE]:
            mainDialog.scale = mainDialog.awdExporterData[ids.REAL_SCALE]
        if mainDialog.awdExporterData[ids.CBOX_LIGHTMATERIALS]:
            mainDialog.exportExtraMats = mainDialog.awdExporterData[ids.CBOX_LIGHTMATERIALS]
        if mainDialog.awdExporterData[ids.CBOX_UNSUPPORTETTEX]:
            mainDialog.exportUnsupportedTex = mainDialog.awdExporterData[ids.CBOX_UNSUPPORTETTEX]
        if mainDialog.awdExporterData[ids.CBOX_UNUSEDMATS]:
            mainDialog.unusedMats = mainDialog.awdExporterData[ids.CBOX_UNUSEDMATS]
        if mainDialog.awdExporterData[ids.CBOX_STREAMING]:
            mainDialog.streaming = mainDialog.awdExporterData[ids.CBOX_STREAMING]
        if mainDialog.awdExporterData[ids.CBOX_COMPRESSED]:
            mainDialog.compressData = mainDialog.awdExporterData[ids.CBOX_COMPRESSED]
        if mainDialog.awdExporterData[ids.CBOX_DEBUG]:
            mainDialog.debug = mainDialog.awdExporterData[ids.CBOX_DEBUG]
        if mainDialog.awdExporterData[ids.CBOX_CLOSEAFTEREXPORT]:
            mainDialog.closeAfter = mainDialog.awdExporterData[ids.CBOX_CLOSEAFTEREXPORT]
        if mainDialog.awdExporterData[ids.COMBO_TEXTURESMODE  ]:
            mainDialog.textures = mainDialog.awdExporterData[ids.COMBO_TEXTURESMODE]
        if mainDialog.awdExporterData[ids.CBOX_ANIMATION]:
            mainDialog.animationBool = mainDialog.awdExporterData[ids.CBOX_ANIMATION]
        if mainDialog.awdExporterData[ids.CBOX_VANIMATION]:
            mainDialog.vanimationBool = mainDialog.awdExporterData[ids.CBOX_VANIMATION]
        if mainDialog.awdExporterData[ids.COMBO_RANGE]:
            mainDialog.animationRange = mainDialog.awdExporterData[ids.COMBO_RANGE]
        if mainDialog.awdExporterData[ids.REAL_FIRSTFRAME]:
            mainDialog.firstFrameUser = mainDialog.awdExporterData[ids.REAL_FIRSTFRAME]
        if mainDialog.awdExporterData[ids.REAL_LASTFRAME]:
            mainDialog.lastFrameUser = mainDialog.awdExporterData[ids.REAL_LASTFRAME]
        if mainDialog.awdExporterData[ids.CBOX_OPENPREFAB]:
            mainDialog.openInPreFab = mainDialog.awdExporterData[ids.CBOX_OPENPREFAB]
        if mainDialog.awdExporterData[ids.CBOX_EXPORTLIGHTXML]:
            mainDialog.exportSceneLights = mainDialog.awdExporterData[ids.CBOX_EXPORTLIGHTXML]
    else:
        mainDialog.awdExporterData = c4d.BaseContainer()
    setUI(mainDialog)
    return True   

def setUI(mainDialog):
    mainDialog.SetReal(ids.REAL_SCALE, mainDialog.scale, 0.001, 99999999, 1.0, c4d.FORMAT_REAL)
    mainDialog.SetBool(ids.CBOX_LIGHTMATERIALS, mainDialog.exportExtraMats)
    mainDialog.SetBool(ids.CBOX_UNSUPPORTETTEX, mainDialog.exportUnsupportedTex)
    mainDialog.SetBool(ids.CBOX_UNUSEDMATS, mainDialog.unusedMats)
    mainDialog.SetBool(ids.CBOX_STREAMING, mainDialog.streaming)
    mainDialog.SetBool(ids.CBOX_COMPRESSED, mainDialog.compressData)
    mainDialog.SetBool(ids.CBOX_DEBUG, mainDialog.debug)
    mainDialog.SetBool(ids.CBOX_CLOSEAFTEREXPORT, mainDialog.closeAfter)
    mainDialog.SetBool(ids.CBOX_OPENPREFAB, mainDialog.openInPreFab)
    mainDialog.SetBool(ids.CBOX_EXPORTLIGHTXML, mainDialog.exportSceneLights)
    mainDialog.SetBool(ids.CBOX_ANIMATION, mainDialog.animationBool)
    mainDialog.SetBool(ids.CBOX_VANIMATION, mainDialog.vanimationBool)

    mainDialog.SetLong(ids.COMBO_TEXTURESMODE, mainDialog.textures)
    mainDialog.SetLong(ids.COMBO_RANGE, mainDialog.animationRange)

    mainDialog.Enable(ids.REAL_FIRSTFRAME, False)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, False)
    mainDialog.Enable(ids.REAL_LASTFRAME, False)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, False)
    mainDialog.Enable(ids.COMBO_RANGE, False)
    mainDialog.Enable(ids.COMBO_RANGE_STR, False)

    if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True and mainDialog.GetBool(ids.CBOX_STREAMING)==True:
        mainDialog.SetBool(ids.CBOX_STREAMING,False)
        mainDialog.streaming=False


    doc=c4d.documents.GetActiveDocument()
    #print mainDialog.GetBool(ids.CBOX_ANIMATION)
    if mainDialog.GetBool(ids.CBOX_ANIMATION)==True or mainDialog.GetBool(ids.CBOX_VANIMATION)==True:
        mainDialog.Enable(ids.COMBO_RANGE, True)
        mainDialog.Enable(ids.COMBO_RANGE_STR, True)
        mainDialog.Enable(ids.REAL_LASTFRAME_STR, True)
        mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, True)
        if mainDialog.GetLong(ids.COMBO_RANGE)==0:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,doc.GetMaxTime().GetFrame(doc.GetFps()),doc.GetMaxTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
        if mainDialog.GetLong(ids.COMBO_RANGE)==1:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), doc.GetLoopMinTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), doc.GetLoopMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
        if mainDialog.GetLong(ids.COMBO_RANGE)==2:
            mainDialog.SetReal(ids.REAL_FIRSTFRAME,mainDialog.firstFrameUser, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.SetReal(ids.REAL_LASTFRAME,mainDialog.lastFrameUser, doc.GetMinTime().GetFrame(doc.GetFps()), doc.GetMaxTime().GetFrame(doc.GetFps()), 1.0, c4d.FORMAT_LONG)
            mainDialog.Enable(ids.REAL_FIRSTFRAME, True)
            mainDialog.Enable(ids.REAL_LASTFRAME, True)
    return True
    
    
def setValues(mainDialog):
    mainDialog.exportExtraMats=mainDialog.GetBool(ids.CBOX_LIGHTMATERIALS)
    mainDialog.awdExporterData.SetBool(ids.CBOX_LIGHTMATERIALS, mainDialog.exportExtraMats)
    mainDialog.exportUnsupportedTex=mainDialog.GetBool(ids.CBOX_UNSUPPORTETTEX)
    mainDialog.awdExporterData.SetBool(ids.CBOX_UNSUPPORTETTEX, mainDialog.exportUnsupportedTex)
    mainDialog.scale=mainDialog.GetReal(ids.REAL_SCALE)
    mainDialog.awdExporterData.SetReal(ids.REAL_SCALE, mainDialog.scale)
    mainDialog.openInPreFab=mainDialog.GetBool(ids.CBOX_OPENPREFAB)
    mainDialog.awdExporterData.SetBool(ids.CBOX_OPENPREFAB, mainDialog.openInPreFab)
    mainDialog.exportSceneLights=mainDialog.GetBool(ids.CBOX_EXPORTLIGHTXML)
    mainDialog.awdExporterData.SetBool(ids.CBOX_EXPORTLIGHTXML, mainDialog.exportSceneLights)
    mainDialog.unusedMats=mainDialog.GetBool(ids.CBOX_UNUSEDMATS)
    mainDialog.awdExporterData.SetBool(ids.CBOX_UNUSEDMATS, mainDialog.unusedMats)
    mainDialog.streaming=mainDialog.GetBool(ids.CBOX_STREAMING)
    mainDialog.awdExporterData.SetBool(ids.CBOX_STREAMING, mainDialog.streaming)
    mainDialog.compressData=mainDialog.GetBool(ids.CBOX_COMPRESSED)
    mainDialog.awdExporterData.SetBool(ids.CBOX_COMPRESSED, mainDialog.compressData)
    mainDialog.debug=mainDialog.GetBool(ids.CBOX_DEBUG)
    mainDialog.awdExporterData.SetBool(ids.CBOX_DEBUG, mainDialog.debug)
    mainDialog.closeAfter=mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT)
    mainDialog.awdExporterData.SetBool(ids.CBOX_CLOSEAFTEREXPORT, mainDialog.closeAfter)
    mainDialog.textures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)
    mainDialog.awdExporterData.SetLong(ids.COMBO_TEXTURESMODE  , mainDialog.textures)
    mainDialog.animationBool=mainDialog.GetBool(ids.CBOX_ANIMATION)
    mainDialog.awdExporterData.SetBool(ids.CBOX_ANIMATION, mainDialog.animationBool)
    mainDialog.vanimationBool=mainDialog.GetBool(ids.CBOX_VANIMATION)
    mainDialog.awdExporterData.SetBool(ids.CBOX_VANIMATION, mainDialog.vanimationBool)
    mainDialog.animationRange=mainDialog.GetLong(ids.COMBO_RANGE)
    mainDialog.awdExporterData.SetLong(ids.COMBO_RANGE, mainDialog.animationRange)        

    if mainDialog.GetLong(ids.COMBO_RANGE)==2:
        mainDialog.firstFrameUser=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        mainDialog.lastFrameUser=mainDialog.GetReal(ids.REAL_LASTFRAME)
    mainDialog.awdExporterData.SetReal(ids.REAL_FIRSTFRAME, mainDialog.firstFrameUser)
    mainDialog.awdExporterData.SetReal(ids.REAL_LASTFRAME, mainDialog.lastFrameUser)  

    c4d.plugins.SetWorldPluginData(ids.PLUGINID, mainDialog.awdExporterData)  

def enableAll(mainDialog, enableBool):
    mainDialog.Enable(ids.CBOX_UNUSEDMATS, enableBool)
    mainDialog.Enable(ids.CBOX_CLOSEAFTEREXPORT, enableBool)
    mainDialog.Enable(ids.CBOX_COMPRESSED, enableBool)
    mainDialog.Enable(ids.CBOX_ANIMATION, enableBool)
    mainDialog.Enable(ids.BTN_EXPORT, enableBool)
    mainDialog.Enable(ids.BTN_SAVEWITHASSETS, enableBool)
    mainDialog.Enable(ids.BTN_CHECKSKELETON, enableBool)
    mainDialog.Enable(ids.BTN_CREATESKELETONANIMATION, enableBool)
    mainDialog.Enable(ids.CBOX_OPENPREFAB, enableBool)       
    mainDialog.Enable(ids.CBOX_EXPORTLIGHTXML, enableBool)      
    mainDialog.Enable(ids.CBOX_LIGHTMATERIALS, enableBool)       
    mainDialog.Enable(ids.CBOX_UNSUPPORTETTEX, enableBool)       
        
        
    mainDialog.Enable(ids.GRP_TEXTURES, enableBool)
    mainDialog.Enable(ids.CBOX_UNUSEDMATS, enableBool)
    mainDialog.Enable(ids.CBOX_STREAMING, enableBool)
    mainDialog.Enable(ids.CBOX_DEBUG, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE, enableBool)
    mainDialog.Enable(ids.COMBO_TEXTURESMODE_STR, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE, enableBool)
    mainDialog.Enable(ids.COMBO_RANGE_STR, enableBool)
    mainDialog.Enable(ids.REAL_SCALE, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME, enableBool)
    mainDialog.Enable(ids.REAL_SCALE_STR, enableBool)
    mainDialog.Enable(ids.REAL_FIRSTFRAME_STR, enableBool)
    mainDialog.Enable(ids.REAL_LASTFRAME_STR, enableBool)
    if enableBool==True:
        mainDialog.Enable(ids.BTN_CANCEL, False)
    if enableBool==True:
        mainDialog.Enable(ids.BTN_CANCEL, False)
        setUI(mainDialog)
