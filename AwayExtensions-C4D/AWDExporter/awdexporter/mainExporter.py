# functions running in mainthread of c4d

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classMainScene
from awdexporter import classesHelper
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers
from awdexporter import mainSkeletonReader
from awdexporter import maindialogHelpers
from awdexporter import mainParseObjectToAWDBlock
from awdexporter import mainMaterials
from awdexporter import mainVertexAnimationReader

# called by "maindialog.Command()" to start the export-process
def startExport(mainDialog,doc):   
    exportData=classMainScene.mainScene(doc,mainDialog)         # create a new "mainScene". this class will store all the data collected for export
     
    # not needed anymor ?
    #exportData.doc.SetMode(11)#set EditMode to 11 (Model-Mode) - otherwise the triangulate method will only affect the selected polygons!     
    objectsToExport=exportData.doc.GetObjects()                             # get a list of all objects in the scene
    
    # check if there is anything to export
    if len(objectsToExport)==0:                                             # if no object is in the scene:
        if exportData.unusedMats==False:                                        # if no unsued materials should be exported:
            newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)           # create a new errorObject
            exportData.AWDerrorObjects.append(newError)                             # append the new errorObject to the errorlist, so it will be displayed at the end of export process 
            return exportData                                                       # return from function
        if exportData.unusedMats==True:                                         # if unused materials should be exported:
            exportData.allc4dMaterials=doc.GetMaterials()                           # get a list of all materials
            if len(exportData.allc4dMaterials)==0:                                  # if no material was found:
                newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)           # create a new errorObject
                exportData.AWDerrorObjects.append(newError)                             # append the new errorObject to the errorlist, so it will be displayed at the end of export process 
                return exportData                                                       # return from function    
    exportData.objList=objectsToExport
    
    # calculate progressbar
    exportData.allStatusLength=2    # used to calculate the progress-bar
    exportData.allStatus=1                                      # used to calculate the progress-bar
    exportData.status=1   
    
    # open save as dialog
    datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save as *.AWD", "awd")
    if datei is None:     
        newError=classesHelper.AWDerrorObject(ids.ERRORMESSAGE2,None)           # create a new errorObject
        exportData.AWDerrorObjects.append(newError)                             # append the new errorObject to the errorlist, so it will be displayed at the end of export process 
        return None
        
    # disable the all GUI-elements, so the user can not change anything while exporting  
    maindialogHelpers.enableAll(mainDialog,False)              
    exportData.datei=datei
    
    
    # if this is executed, we know there is something to export!
    
    # create the MetaDataBlock
    newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(None,"",255)
    exportData.idCounter+=1
    newMetaDataBlock=classesAWDBlocks.MetaDataBlock(0,0)
    newMetaDataBlock.timestamp=0# to do
    newMetaDataBlock.encoder="AWDToolsC4D"
    newMetaDataBlock.encoderVersion="0.9"
    newMetaDataBlock.app="Cinema4D"
    newMetaDataBlock.appVersion="R13 / R14" # to do
    newAWDWrapperBlock.data=newMetaDataBlock
    newAWDWrapperBlock.tagForExport=True   
    exportData.allAWDBlocks.append(newAWDWrapperBlock)  
    
    # create a AWD-Material-Block for the C4D-Default-Color, in case some Objects have no Materials/ObjectColors Applied
    newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(None,"C4D-DefaultMaterial",81)
    defaultColor=exportData.doc[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR]
    newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,True)
    newAWDBlock.saveLookUpName="C4D-DefaultMat"
    exportData.allMatBlocks.append(newAWDBlock)
    defaultColorString="#"+str(defaultColor)
    exportData.colorMaterials[defaultColorString]=newAWDBlock
    newAWDBlock.matColor=[defaultColor.z*255,defaultColor.y*255,defaultColor.x*255,0]
    newAWDBlock.saveMatProps.append(1)
    newAWDBlock.isCreated=True
    newAWDWrapperBlock.data=newAWDBlock
    newAWDWrapperBlock.tagForExport=False 
    exportData.allAWDBlocks.append(newAWDWrapperBlock)  
    exportData.idCounter+=1
    
    # create a AWD-Material-Block for all the C4D-Materials in the scene, regardless if they will be exported or not. 
    for mat in exportData.allc4dMaterials:
        newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(mat,mat.GetName(),81)
        newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,False)
        newAWDBlock.saveLookUpName=mat.GetName()
        newAWDBlock.name=mat.GetName()
        newAWDBlock.mat=mat
        mat.SetName(str(exportData.idCounter))
        exportData.idCounter+=1
        newAWDWrapperBlock.data=newAWDBlock
        newAWDWrapperBlock.tagForExport=False    
        exportData.allAWDBlocks.append(newAWDWrapperBlock)
        exportData.allMatBlocks.append(newAWDBlock) 	
    
    # create a AWD-Block for all Objects in the Scene (and their tags) regardless if they will be exported or not
    mainParseObjectToAWDBlock.createAllAWDBlocks(exportData,objectsToExport)
    
    # create a SceneBlock for all Objects that should be exported
    mainParseObjectToAWDBlock.createAllSceneBlocks(exportData,objectsToExport,exportData.defaultObjectSettings)
    
    exportData.allStatusLength=2+(10*int(exportData.animationCounter))+(10*len(exportData.allMeshObjects))# used to calculate the progress-bar
    exportData.allStatus=1                                      # used to calculate the progress-bar
    exportData.status=1                                         # used to calculate the progress-bar
    mainHelpers.updateCanvas(mainDialog,exportData)             # update the progress-bar
    mainSkeletonReader.createSkeletonBlocks(exportData.objList,exportData,mainDialog) 
    if mainDialog.GetBool(ids.CBOX_VANIMATION)==True:
        mainVertexAnimationReader.getVertexAnimationData(exportData.objList,exportData,mainDialog)
    exportData.status=2  
    mainHelpers.updateCanvas(mainDialog,exportData)
    return exportData         
	
	
# called by "maindialog.Timer()" to end the exportprocess when background-Thread has finished
def endExport(mainDialog,exportData):        
    #mainHelpers.deleteCopiedMeshes(exportData.allMeshObjects)
    if exportData is not None:
        if len(exportData.AWDerrorObjects)>0:  
            newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
            for errorMessage in exportData.AWDerrorObjects:
                newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
                if errorMessage.errorData!=None:
                    newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
            c4d.gui.MessageDialog(newMessage)
            if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
                exportData=None
                c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                mainDialog.Close()
                return True  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            return True  
        if len(exportData.AWDwarningObjects)>0:  
            newMessage=c4d.plugins.GeLoadString(ids.WARNINGMESSAGE)+"\n"
            for errorMessage in exportData.AWDwarningObjects:
                newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
                if errorMessage.errorData!=None:
                    newMessage+="AWDWarningObject: "+str(errorMessage.errorData)
            print "Warning "+str(newMessage)
            if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
                exportData=None
                c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                c4d.EventAdd(c4d.EVENT_ANIMATE) 
                mainDialog.Close()    
                return True  
        if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True and exportData.cancel!=True:  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            mainDialog.Close()
            return True  
    exportData=None
    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE) 
    maindialogHelpers.enableAll(mainDialog,True)
    #print c4d.plugins.GeLoadString(ids.SUCCESSMESSAGE)
    mainHelpers.updateCanvas(mainDialog,exportData)
    c4d.EventAdd(c4d.EVENT_ANIMATE) 
    mainDialog.SetTimer(0)   
 