# some helper-functions for the part of the export process running in the c4d-mainthread

import c4d
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import maindialogHelpers
from awdexporter import mainVertexAnimationHelper



def checkforValidSelectedSkeleton():     
    doc=c4d.documents.GetActiveDocument()       # we check if a C4D-document is open
    if doc is not None:
        op=doc.GetActiveObject()                    # we check if a single Object is selected
        if op is not None:
            if len(op.GetChildren())>0:
                return op
        tag=doc.GetActiveTag() 
        if tag is not None:
            tagType=tag.GetType()
            if tagType==1028937 or tagType==1028938:
                return tag.GetObject()
    return None
  
def bakeVertexAnimation(doc):
    thisTag=doc.GetActiveTag()
    if thisTag is None:
        print "Please select a VertexAnimationTag to use this function"
    if thisTag:
        print thisTag.GetType()
        if thisTag.GetType()!=1030484:
            print "Please select a VertexAnimationTag to use this function"
            return
        animationTagCounter=0
        for tag in thisTag.GetObject().GetTags():
            if tag.GetType()==1030484:
                animationTagCounter+=1
        if animationTagCounter>1:
            print "Object to bake must have only 1 AnimationTag applied!"
            return
        if animationTagCounter==1:
            newName=c4d.gui.InputDialog("Animation-Name",thisTag[1011])
            mainVertexAnimationHelper.createAnimationObject(thisTag.GetObject(),thisTag,newName,doc) 


def copySkeletonAndApplySkeletonAnimation(curObj): 
    doc=c4d.documents.GetActiveDocument()       # we check if a C4D-document is open
    doc.StartUndo()                     # Start undo support

    newObj=curObj.GetClone()
    getAllTags=newObj.GetTags()
    for tag in getAllTags:
        tag.Remove()
    newTag=newObj.MakeTag(1028938)
    newName=c4d.gui.InputDialog("Animation-Name","Animation 01")
    newTag[1011]=newName
    newObj.SetName(newName)
    doc.InsertObject(newObj,curObj.GetUp(),curObj)
    doc.AddUndo(c4d.UNDOTYPE_NEW, newObj) # Support redo the insert operation
    doc.SetActiveObject(newObj,c4d.SELECTION_NEW)
    doc.SetActiveTag(newTag,c4d.SELECTION_NEW)
    doc.EndUndo()                       # Do not forget to close the undo support 
    c4d.EventAdd()
    
def deleteCopiedMeshes(meshBlockList):
    for meshBlock in meshBlockList:            
        pass#meshBlock.copiedMesh.Remove()
        
def printErrors(mainDialog,exportData):  
    if len(exportData.AWDerrorObjects)>0:  
        maindialogHelpers.enableAll(mainDialog,True)
        newMessage=c4d.plugins.GeLoadString(ids.ERRORMESSAGE)+"\n"
        for errorMessage in exportData.AWDerrorObjects:
            newMessage+=c4d.plugins.GeLoadString(errorMessage.errorID)
            if errorMessage.errorData!=None:
                newMessage+="\n\n"+str(c4d.plugins.GeLoadString(ids.ERRORMESSAGEOBJ))+" = "+str(errorMessage.errorData)
        c4d.gui.MessageDialog(newMessage)
        exportData=None
        if mainDialog.GetBool(ids.CBOX_CLOSEAFTEREXPORT) == True:  
            exportData=None
            c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            c4d.EventAdd(c4d.EVENT_ANIMATE) 
            mainDialog.Close()
        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
        c4d.EventAdd(c4d.EVENT_ANIMATE)  
        exportData=None  
        return False   
    return True	
		

def updateCanvas(mainDialog,exportData):
    doc=c4d.documents.GetActiveDocument()
    if doc is None:
        statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
        mainDialog.userarea.draw([statusStr,0,0])
        return
    if doc is not None:
        if doc.GetDocumentPath() is None or doc.GetDocumentPath()=="":
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
            mainDialog.userarea.draw([statusStr,0,0])
            return
        if exportData is None:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE2)
            mainDialog.userarea.draw([statusStr,0,0])
            return
        if exportData.status==0:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE3)
            mainDialog.userarea.draw([statusStr,0,0])
            return
        curPercent=float(float(exportData.allStatus)/float(exportData.allStatusLength))
        c4d.StatusSetBar(curPercent)
        if exportData.status==1:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE4)+"  "+str(int(curPercent*100))+" %"
            mainDialog.userarea.draw([statusStr,curPercent,0])     
            return
        if exportData.status==2:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE5)+"  "+str(int(curPercent*100))+" %"
            mainDialog.userarea.draw([statusStr,curPercent,float(exportData.subStatus)])
            return
        if exportData.status==3:
            statusStr=c4d.plugins.GeLoadString(ids.STATUSMESSAGE)+c4d.plugins.GeLoadString(ids.STATUSMESSAGE6)+"  "+str(int(curPercent*100))+" %"
            mainDialog.userarea.draw([statusStr,curPercent,0])
            return	


# i think this could be removed
def resetAllObjectsAtBeginning(objList=None):
    for curObj in objList:
        #if curObj.GetTag(c4d.Tweights):#	
            #c4d.documents.GetActiveDocument().SetActiveObject(curObj)
            #c4d.CallCommand(1019937)
            #c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
            #c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
            #c4d.documents.GetActiveDocument().SetTime(c4d.documents.GetActiveDocument().GetTime())
            #c4d.EventAdd(c4d.EVENT_ANIMATE)
        if curObj.GetTag(c4d.Tposemorph):#	reset morphtags
            all_tags=curObj.GetTags()#get all tags applied to object
            for morphtag in all_tags:#do for each tag:
                if morphtag.GetType()==c4d.Tposemorph:#do if the tag is a morphtag
                    if morphtag.GetMode()==1:#do if the tag is in animation-mode:
                        exportData.doc.SetTime(c4d.BaseTime(0, exportData.doc.GetFps()))
                        c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
                        c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
                        exportData.doc.SetTime(exportData.doc.GetTime())
                        c4d.EventAdd(c4d.EVENT_ANIMATE)
                        for track in morphtag.GetCTracks():
                            curve = track.GetCurve()
                            if curve.GetKeyCount()==0:
                               pass#print "skipped morphpose"
                            if curve.GetKeyCount()>0:
                               curve.GetKey(0).SetValue(curve,0.0)
        resetAllObjectsAtBeginning(curObj.GetChildren())
