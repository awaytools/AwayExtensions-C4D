#AWD Skeleton Tag (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1028937    #ID for the tag

AWDSKELETON_EXPORT              = 1010
AWDSKELETON_NAME                = 1011
AWDSKELETON_EXPORTSCENEOBJECTS  = 1014
AWDSKELETON_WRONOBJECTTYPE      = 1013
AWDSKELETON_CREATEPOSETAG      = 1015
AWDSKELETON_JPP_TEXT1= 1020
AWDSKELETON_JPP_REDUCE1= 1021
AWDSKELETON_JPP_CHECK= 1022
AWDSKELETON_JPP_LINK1= 1023
    
AWDSKELETON_JPP_TEXT2= 1024
AWDSKELETON_JPP_REDUCE2= 1025
AWDSKELETON_JPP_LINK2= 1027
    
AWDSKELETON_JPP_TEXT3= 1028    
AWDSKELETON_JPP_REDUCE3= 1029
AWDSKELETON_JPP_LINK3= 1031
    
AWDSKELETON_JPP_TEXT4= 1032
AWDSKELETON_JPP_REDUCE4= 1033
AWDSKELETON_JPP_LINK4= 1035
    
AWDSKELETON_JPP_TEXT5= 1036
AWDSKELETON_JPP_REDUCE5= 1037
AWDSKELETON_JPP_LINK5= 1039
    
AWDSKELETON_JPP_TEXT6= 1040
AWDSKELETON_JPP_REDUCE6= 1041
AWDSKELETON_JPP_LINK6= 1043    
    
AWDSKELETON_JPP_TEXT7= 1044
AWDSKELETON_JPP_REDUCE7= 1045
AWDSKELETON_JPP_LINK7= 1047
    
AWDSKELETON_JPP_TEXT8= 1045
AWDSKELETON_JPP_REDUCE8= 1046
AWDSKELETON_JPP_LINK8= 1048
   
AWDSKELETON_JPP_TEXT9= 1049
AWDSKELETON_JPP_REDUCE9= 1050
AWDSKELETON_JPP_LINK9= 1052
    
AWDSKELETON_JPP_TEXT10= 1053
AWDSKELETON_JPP_REDUCE10= 1054
AWDSKELETON_JPP_LINK10= 1056
AWDSKELETON_JPP_STATUS = 1030
AWDSKELETON_JPP_REDUCE= 1034
# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDSkeletonTagXpression(plugins.TagData):

    allLinkIDs=None
    allLinkText=None
    allLinkReduceIds=None
    jointCounter=0
    allWeightTags=[]
    inProcess=False
    hasCalculation=False
    def Init(self,node):
        self.allLinkIDs=[]
        self.allLinkText=[]
        self.allLinkReduceIds=[]
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK1)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT1)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE1)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK2)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT2)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE2)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK3)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT3)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE3)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK4)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT4)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE4)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK5)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT5)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE5)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK6)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT6)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE6)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK7)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT7)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE7)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK8)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT8)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE8)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK9)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT9)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE9)
        self.allLinkIDs.append(AWDSKELETON_JPP_LINK10)
        self.allLinkText.append(AWDSKELETON_JPP_TEXT10)
        self.allLinkReduceIds.append(AWDSKELETON_JPP_REDUCE10)
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(AWDSKELETON_EXPORT,True)#children
        bc.SetBool(AWDSKELETON_EXPORTSCENEOBJECTS,True)#children
        bc.SetString(AWDSKELETON_NAME ,"")
        node.SetData(bc)
        self.getWeightTagsFromUI(bc)
        if len(self.allWeightTags)>0:
            self.hasCalculation=True
            
        return True
        
    # this function gets called for every gui-item of the tag, 
    # using the id (c4d.DescID) we check which gui-item is processed in this function-call
    # by returning True/False, we tell C4D to enable/disable the gui-item
    def GetDEnabling (self, node, id, t_data, flags, itemdesc):
         
        testerString="("+str(AWDSKELETON_JPP_REDUCE)+", 8, 1028937)"
        if str(id)==str(testerString):
            if self.hasCalculation==False:
                return False   
        # test if the gui-item is one of the 'Weight-Tag-JointPerPoint-Strings' - they should allways be disabled, so we return False
        for tester in self.allLinkText:
            testerString="("+str(tester)+", 130, 1028937)"
            if str(id)==str(testerString):
                return False   
        # test if the gui-item is one of the 'Weight-Tag-LinkBoxes' - they should allways be disabled, so we return False  
        for tester in self.allLinkIDs:
            testerString="("+str(tester)+", 133, 1028937)"
            if str(id)==str(testerString):
                return False   
        # test if the gui-item is one of the 'Weight-Tag-LinkBoxes' - they should only be enabled if a Weight-Tag is set in the associated linkbox     
        tester=0
        while tester < len(self.allLinkReduceIds):
            if tester>=len(self.allWeightTags):# only if no WeightTag is set for the associated linkbox, we return False
                testerString="("+str(self.allLinkReduceIds[tester])+", 400006001, 1028937)"
                if str(id)==str(testerString):
                    return False   
            tester+=1
        #print str(id)
        #if the function has not returned False by now, the gui-element is set to be enabled by returning True
        return True
        
        
    # this function gets called for every Message the Tag recieves from C4D 
    def Message(self, node, type, data):
        #check if the Message was send from a Description-Dialog (such as this Tag)
        if type == c4d.MSG_DESCRIPTION_COMMAND:
            #check if a gui-element of this tag has send the Message, and if so, call a the function: 
            if data["id"][0].id == AWDSKELETON_JPP_REDUCE:
                self.reduceJpP(node)#reduce the "Joints per Point-Value" of the current 'active' (in this Plugin enabled) weight-tags
            if data["id"][0].id == AWDSKELETON_CREATEPOSETAG:
                self.createPoseMorph(node.GetObject())# create a Pose-Tag on the host-object, and set to it enable "hirarchie", "Translation", "Rotation"
            if data["id"][0].id == AWDSKELETON_JPP_CHECK:
                self.checkBindData(node)# check which WeightTags are using this skeleton, and calculate how many Joints-per-points are used
        return True
        
    # gets called everyTime C4D redraws this tag
    def Draw(self, tag, op, bd, bh):    
        if len(self.allWeightTags)>0:
            self.hasCalculation=True
        return True
       
    # recursive function to collect all weight-tags found on all objects in the current active C4D scene
    def getAllWeightTags(self,objlist,op):
        for curObj in  objlist:
            allTags=curObj.GetTags()
            for tag in allTags:
                if tag.GetType()==1019365:
                    if self.hasWeight([op],tag)==True:
                        self.allWeightTags.append(tag)
            self.getAllWeightTags(curObj.GetChildren(),op)
            
    # main function to get all weight-tags that acctually uses this skeleton, and calculate the used Joints-per-point     
    def checkBindData(self,node):
        self.inProcess=True
        if node is None:
            return
        op=node.GetObject()
        if op is None:
            return
        bc=node.GetDataInstance()
        if bc is None:
            return
        answer=c4d.gui.QuestionDialog("Calculate Joints-per-Point\n\nThe C4D-Editor will freeze for a moment...\n\nA Dialog will inform you when the calulation is done!\n\nStart calculations ?")
        if answer==False:
            return
        self.hasCalculation=False
        c4d.EventAdd()
        self.resetWeightGroup(bc)#set all 'weight-tag-checkboxes' to False
        self.allWeightTags=[]#reset the weight-tag-list  
        doc=c4d.documents.GetActiveDocument()
        if doc:
            print "Start Processing: Calculate Joints-Per-Point"
            allObjects=doc.GetObjects()
            self.getAllWeightTags(allObjects,op)#call to get all weighttags found in this document
            tagCnt=0
            tagCnt2=0
            newTags=[]
            #for each point we calculate the maximum used Joints-per-point, and update the ui
            for weightTag in self.allWeightTags:            
                polyObj=weightTag.GetObject()
                allPoints=polyObj.GetAllPoints()
                lenPoints=len(allPoints)
                pointIdx=0
                maxJoints=0
                hasJoints=0
                while pointIdx<lenPoints:
                    self.jointCounter=0
                    self.isUsedForPoint([op],weightTag,pointIdx)
                    if self.jointCounter>maxJoints:
                        hasJoints+=1
                        maxJoints=self.jointCounter
                    pointIdx+=1
                if hasJoints>0:
                    bc.SetLink(self.allLinkIDs[tagCnt2],weightTag)
                    bc.SetString(self.allLinkText[tagCnt2],str(maxJoints))
                    bc.SetBool( self.allLinkReduceIds[tagCnt2],True)
                    newTags.append(weightTag)
                tagCnt2+=1     
                tagCnt+=1   
        print "End Processing: Calculate Joints-Per-Point"
        self.inProcess=False
        self.allWeightTags=newTags
        if (len(self.allWeightTags))>0:
            self.hasCalculation=True
        c4d.gui.MessageDialog("Calculate Joints-per-Point: Finished !")
        bc.SetString( AWDSKELETON_JPP_STATUS,"")
        c4d.EventAdd()
        
    #reset all Data
    def resetWeightGroup(self,bc):
        cnt=0
        while cnt<len(self.allLinkReduceIds):
            bc.SetString(self.allLinkText[cnt],"")
            bc.SetBool( self.allLinkReduceIds[cnt],False)
            bc.SetLink(self.allLinkIDs[cnt],c4d.BaseObject(c4d.Onull))
            cnt+=1
        c4d.EventAdd()
         
    def getWeightTagsFromUI(self,bc):
        self.allWeightTags=[]
        for tag in self.allLinkIDs:
            newTag=bc.GetLink(tag)
            if newTag is not None:
                if newTag.GetType()==1019365:
                    self.allWeightTags.append(newTag)
                
    #reduce the Joints per Point for all active weighttags
    def reduceJpP(self,node):
        if node is None:
            return
        op=node.GetObject()
        if op is None:
            return
        bc=node.GetDataInstance()
        if bc is None:
            return
        answer=c4d.gui.QuestionDialog("Reduce Joints-per-Point....\n\nThe C4D-Editor will freeze for a moment...\n\nA Dialog will inform you when the calulation is done!\n\nStart calculation ?")
        c4d.EventAdd()
        if answer==False:
            return
        print "Start Processing: Reduce Joints-Per-Point"
        self.getWeightTagsFromUI(bc)
        if (len(self.allWeightTags))>0:
            tagCounter=0
            while tagCounter<len(self.allWeightTags):
                if bc.GetBool(self.allLinkReduceIds[tagCounter])==True:
                    newJointsPerPoint=int(bc.GetString(self.allLinkText[tagCounter]))-1
                    if newJointsPerPoint>0:
                        weightTag=self.allWeightTags[tagCounter]
                        polyObj=weightTag.GetObject()
                        allPoints=polyObj.GetAllPoints()
                        lenPoints=len(allPoints)
                        pointIdx=0
                        maxJoints=0
                        while pointIdx<lenPoints:
                            self.jointCounter=0
                            self.smallestWeight=1
                            self.smallestWeightIdx=0
                            self.jointIdxs=[]
                            self.jointWeights=[]
                            self.isUsedForPoint2([op],weightTag,pointIdx)
                            if self.jointCounter>newJointsPerPoint:
                                weightTag.SetWeight(self.smallestWeightIdx,pointIdx,0.0)
                                jointChangeCnt=0                            
                                while jointChangeCnt<len(self.jointIdxs):
                                    if self.jointIdxs[jointChangeCnt]!=self.smallestWeightIdx:
                                        weightTag.SetWeight(self.jointIdxs[jointChangeCnt],pointIdx,self.jointWeights[jointChangeCnt]+((self.jointWeights[jointChangeCnt]/(1-self.smallestWeight))*self.smallestWeight))
                                    jointChangeCnt+=1
                            pointIdx+=1
                        bc.SetString(self.allLinkText[tagCounter],str(newJointsPerPoint))
                        weightTag.WeightDirty()
                tagCounter+=1
        print "End Processing: Reduce Joints-Per-Point"
        c4d.gui.MessageDialog("Reduce Joints-per-Point: Finished !")
        c4d.EventAdd()
    
    def hasWeight(self,jointList,weightTag):
        maxJointIdx=weightTag.GetJointCount()
        for curObj in  jointList:
            if curObj.GetType()==c4d.Ojoint:
                jointIndex=weightTag.FindJoint(curObj)
                if jointIndex is not None and jointIndex and jointIndex<maxJointIdx and jointIndex>0:
                    return True
            if self.hasWeight(curObj.GetChildren(),weightTag)==True:
                return True
        return False
        
    def isUsedForPoint(self,jointList,weightTag,pointIdx):
        maxJointIdx=weightTag.GetJointCount()
        for curObj in  jointList:
            if curObj.GetType()==c4d.Ojoint:
                jointIndex=weightTag.FindJoint(curObj)
                if jointIndex is not None and jointIndex and jointIndex<maxJointIdx and jointIndex>0:
                    thisWeight=weightTag.GetWeight(jointIndex,pointIdx)
                    if float(thisWeight)>0.0:
                        self.jointCounter+=1
            self.isUsedForPoint(curObj.GetChildren(),weightTag,pointIdx)
    
    def isUsedForPoint2(self,jointList,weightTag,pointIdx):
        maxJointIdx=weightTag.GetJointCount()
        for curObj in  jointList:
            if curObj.GetType()==c4d.Ojoint:
                jointIndex=weightTag.FindJoint(curObj)
                if jointIndex is not None and jointIndex and jointIndex<maxJointIdx and jointIndex>0:
                    thisWeight=weightTag.GetWeight(jointIndex,pointIdx)
                    if float(thisWeight)>0.0:
                        if self.smallestWeight>thisWeight:
                            self.smallestWeight=thisWeight
                            self.smallestWeightIdx=jointIndex
                        self.jointIdxs.append(jointIndex)
                        self.jointWeights.append(thisWeight)
                        self.jointCounter+=1
            self.isUsedForPoint2(curObj.GetChildren(),weightTag,pointIdx)
    def createPoseMorph(self,op):
        newTag=op.MakeTag(1024237)  
        newTag[c4d.ID_CA_POSE_HIERARCHY]=True
        newTag[c4d.ID_CA_POSE_P]=True
        newTag[c4d.ID_CA_POSE_R]=True
        newTag[c4d.ID_CA_POSE_R]=True
        newTag.AddMorph()
        newTag.UpdateMorphs()
        c4d.EventAdd(c4d.EVENT_ANIMATE)
# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Skeleton", g=AWDSkeletonTagXpression, description="AWDSkeletonTag", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_EXPRESSION|c4d.TAG_VISIBLE)