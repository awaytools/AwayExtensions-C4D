import c4d
from c4d import gui
#Welcome to the world of Python
# functions running in the c4d-main-thread

# some functions to convert skeleton-animations from c4d to awd2-data

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks


#AWD Skeleton Tag (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math


class SkeletonHelper(object):

    curObj=None
    jointCounter=0
    allWeightTags=[]
    expressionTagsToRestore=[]
    def __init__(self,curObj,wasSelected=None,printErrors=True):
        self.doc=c4d.documents.GetActiveDocument()
        if wasSelected is None:
            wasSelected=curObj
        self.allWeightTags=[]
        self.curObj=curObj   
        doc=c4d.documents.GetActiveDocument()
        allobjects=doc.GetObjects()
        messageStr="OK"
        self.getAllWeightTags(allobjects)
        self.expressionTagsToRestore=[]
        self.disableExpressionsOnJoints([curObj],self.expressionTagsToRestore)
        c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW)
        c4d.EventAdd()           
        self.resetBindPose(curObj,wasSelected)
        if self.isRightScale([curObj])==False:
            rvalue = gui.QuestionDialog("Skeleton contains Joints with other Scale than '1,1,1'.\n\n Fix automatically?")
            if rvalue==True:      
                self.setRightScale([self.curObj])
                self.setNewBindPose(curObj,wasSelected)
            if rvalue==False:      
                messageStr="ERROR: Some Joints have Scale-Values other than '1,1,1' !!!\n\n"
        skinnedMatrices=self.checkBind() 
        rvalue1=False             
        if len(skinnedMatrices)>=1:
            rvalue1 = gui.QuestionDialog("Joints are bound to a 'Skinning-Matrix' thats not the Global Matrix of the C4D-Scene.\nTo prevent errors all meshes should be skinned to the GLobal-C4D-Matrix.\nFix automaticcaly ?")            
            if rvalue1==True:
                self.setSkinMgToGlobal()  
                self.setNewBindPose(curObj,wasSelected)     
            if rvalue1==False:      
                if messageStr=="OK":
                    messageStr=""
                messageStr+="ERROR: Joints are bound to a 'Skinning-Matrix', thats not the Global Matrix of the C4D-Scene.\nTo prevent Errors all Objects should be skinned to the GLobal-C4D-Matrix.\n\n"  
         
        #print ("Skeleton Status\n"+str(messageStr))
        if printErrors==True:
            gui.MessageDialog("Skeleton Status\n"+str(messageStr))
            for tag in self.expressionTagsToRestore:
                tag[c4d.EXPRESSION_ENABLE]=True
            
    def disableExpressionsOnJoints(self,jointObjs,returnList): 
        for curObj in jointObjs:
            allTags=curObj.GetTags()
            for tag in allTags:
                if tag.GetType()!=1028937:
                    if tag[c4d.EXPRESSION_ENABLE]:
                        tag[c4d.EXPRESSION_ENABLE]=False
                        returnList.append(tag)
            if len(curObj.GetChildren())>0:
                self.disableExpressionsOnJoints(curObj.GetChildren(),returnList)       
    
    def resetBindPose(self,curObj,oldSelecObj):
        tagCnt=0
        doc=c4d.documents.GetActiveDocument()
        while tagCnt<len(self.allWeightTags):
            if tagCnt==0:
                doc.SetActiveObject(self.allWeightTags[tagCnt].GetObject(),c4d.SELECTION_NEW)
            if tagCnt>0:
                doc.SetActiveObject(self.allWeightTags[tagCnt].GetObject(),c4d.SELECTION_ADD)
            tagCnt+=1
        c4d.EventAdd()
        self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, curObj) # Support redo the insert operation
        c4d.CallCommand(1019937)
        c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW)
        doc.SetActiveObject(oldSelecObj,c4d.SELECTION_NEW)
        c4d.EventAdd()           

    def setNewBindPose(self,curObj,oldSelecObj):
        tagCnt=0
        doc=c4d.documents.GetActiveDocument()
        while tagCnt<len(self.allWeightTags):
            if tagCnt==0:
                doc.SetActiveObject(self.allWeightTags[tagCnt].GetObject(),c4d.SELECTION_NEW)
            if tagCnt>0:
                doc.SetActiveObject(self.allWeightTags[tagCnt].GetObject(),c4d.SELECTION_ADD)
            tagCnt+=1
        c4d.EventAdd()
        self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, curObj) # Support redo the insert operation
        c4d.CallCommand(1019954)
        doc.SetActiveObject(oldSelecObj,c4d.SELECTION_NEW)
        c4d.EventAdd()
        
        
    def checkBind(self):
        matrices=[]
        matrix=c4d.Matrix()        
        for weightTag in self.allWeightTags:
            curMatrix=weightTag.GetGeomMg()
            if matrix!=curMatrix:
                tester=0
                for k in matrices:                    
                    if k==curMatrix:
                        tester+=1
                if tester==0:
                    matrices.append(curMatrix)
        return matrices
    
    def setSkinMgToGlobal(self):
        newMatrix=c4d.Matrix()
        for weightTag in self.allWeightTags:
            self.getPointsPositions( weightTag.GetObject(),newMatrix)            
        return
    
        
    def getPointsPositions(self,obj,newMg):
        points=obj.GetAllPoints()
        lokalMl=obj.GetMl()
        pointsNew=[]
        for point in points:
            pointsNew.append(c4d.Vector(point*lokalMl))
        self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Support redo the insert operation
        obj.SetMg(newMg)
        c4d.EventAdd()
        pointsNew2=[]
        for point in pointsNew:
            pointsNew2.append(c4d.Vector(newMg.__invert__()*point))
        obj.SetAllPoints(pointsNew2)
        c4d.EventAdd()
        

            
    def getAllWeightTags(self,objlist):
        for curObj in  objlist:
            allTags=curObj.GetTags()
            for tag in allTags:
                if tag.GetType()==1019365:
                    if self.hasWeight([self.curObj],tag)==True:
                        self.allWeightTags.append(tag)
            if curObj.GetChildren():
                self.getAllWeightTags(curObj.GetChildren())
            
    def hasWeight(self,jointList,weightTag):
        for curObj in  jointList:
            if weightTag.FindJoint(curObj) is not None and weightTag.FindJoint(curObj)>=0 :
                return True
            if curObj.GetChildren():
                if self.hasWeight(curObj.GetChildren(),weightTag)==True:
                    return True
        return False
        
    def hasTracks(self,jointList):
        for curObj in  jointList:
            tracks=curObj.GetCTracks()
            if tracks is not None:
                if len(tracks)>0:
                    return True
            if curObj.GetChildren():
                if self.hasTracks(curObj.GetChildren())==True:
                    return True
        return False
        
    def deleteTracks(self,jointList):
        for curObj in  jointList:
            tracks=curObj.GetCTracks()
            if tracks is not None:
                if len(tracks)>0:
                    for track in tracks:
                        track.Remove()
            if curObj.GetChildren():
                self.deleteTracks(curObj.GetChildren())
        
    def isRightScale(self,jointList):
        for curObj in  jointList:
            scaleStandart=c4d.Vector(1,1,1)
            scaleVec=curObj.GetAbsScale()
            if str(scaleStandart)!=str(scaleVec):
                #print curObj.GetName()+" / "+str(scaleStandart)+" / "+str(scaleVec)
                return False
            if curObj.GetChildren():
                if self.isRightScale(curObj.GetChildren())==False:
                    return False
        return True
         
    def setRightScale(self,jointList):
        for curObj in  jointList:
            scaleVec=curObj.GetAbsScale()
            newScaleVec=c4d.Vector(1,1,1)
            newDifferenceVec=c4d.Vector(0,0,0)
            if scaleVec.x!=1:
                newDifferenceVec.x=scaleVec.x        
            if scaleVec.y!=1:
                newDifferenceVec.y=scaleVec.y
            if scaleVec.z!=1:
                newDifferenceVec.z=scaleVec.z
            curObj.SetAbsScale(newScaleVec)
            for child in curObj.GetChildren(): 
                self.setNewCoordinates2(child,newDifferenceVec)    
            self.setRightScale(curObj.GetChildren())
                
    def setNewCoordinates2(self,op,differenceVec):
        frozenPosVec=op.GetFrozenPos()
        posVec=op.GetRelPos()
        if differenceVec.x!=0:
            frozenPosVec.x=frozenPosVec.x*differenceVec.x
            posVec.x=posVec.x*differenceVec.x
        if differenceVec.y!=0:
            frozenPosVec.y=frozenPosVec.y*differenceVec.y
            posVec.y=posVec.y*differenceVec.y
        if differenceVec.z!=0:
            frozenPosVec.z=frozenPosVec.z*differenceVec.z
            posVec.z=posVec.z*differenceVec.z
        self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, op) # Support redo the insert operation
        op.SetRelPos(posVec)
        self.doc.AddUndo(c4d.UNDOTYPE_CHANGE, op) # Support redo the insert operation
        op.SetFrozenPos(frozenPosVec)
        for child in op.GetChildren(): 
            self.setNewCoordinates2(child,differenceVec)    
     


