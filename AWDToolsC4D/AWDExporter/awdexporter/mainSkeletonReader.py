# functions running in the c4d-main-thread

# some functions to convert skeleton-animations from c4d to awd2-data

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers
from awdexporter import mainSkeletonHelper

# this is the function that gets called from the "mainExporter"
def createSkeletonBlocks(objList,exportData,mainDialog,newAWDBlockAnimSetoriginal=None):
    for object in objList:                                      # for every object do:
        newAWDBlockAnimSet=newAWDBlockAnimSetoriginal   
        exportThisObj=True
        exportThisObjChild=True
            
        exporterSettingsTag=object.GetTag(1028905)
        if exporterSettingsTag is not None:
            if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== True:                                # for every object do:
                exportThisObj=False
                exportThisObjChild=False
            if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== False:
                exportThisObj=False
                exportThisObjChild=True
                
        if exportThisObj==True:        
            skeletonTag=object.GetTag(1028937)                          # try to find a "SkeletonTag" on this object 
            if skeletonTag is not None:                                 # if a "SkeletonTag" is found:
                if skeletonTag[1010]==True:                                 # if the "SkeletonTag" is enabled for export:
                    if skeletonTag[1011] is not None:                           # if the "SkeletonTag"-Name is not None:
                        buildSkeleton(exportData,object)                            # build the skeletonBlock
            tag=object.GetTag(1030508)
            if tag is not None:
                if tag[1050] is None: 
                    print "ERROR = No AnimationSet-Target Set"
                if tag[1050] is not None: 
                    if str(tag[1050].GetName())==str(object.GetName()): 
                        print "ERROR = AnimationSet must not target itself"
                    if str(tag[1050].GetName())!=str(object.GetName()):
                        
                        meshBlock=exportData.allAWDBlocks[int(tag[1050].GetName())]  
                        newAWDBlockAnimSet=classesAWDBlocks.AnimationSetBlock(int(tag.GetName()),0,meshBlock,tag[1011])
                        exportData.allAWDBlocks[int(tag.GetName())].data=newAWDBlockAnimSet
                        exportData.allAWDBlocks[int(tag.GetName())].blockType=113
                        exportData.allAWDBlocks[int(tag.GetName())].tagForExport=True
                        print "Create ANimationSET "+str(exportData.allAWDBlocks[int(tag.GetName())])+" mdslk = "+str(int(tag.GetName())) 
            if tag is None:
                alltags=object.GetTags()
                for skeletonAnimationTag in alltags:
                    if skeletonAnimationTag.GetType()==1028938:                        # if a "SkeletonAnimationTag" is found:
                        if skeletonAnimationTag[1010]==True:                        # if the "SkeletonAnimationTag" is enabled for export:
                            if skeletonAnimationTag[1011] is not None:                  # if the "SkeletonAnimationTag"-Name is not None:
                                anim=buildSkeletonAnimation(exportData,object,mainDialog,skeletonAnimationTag)        # build the SkeletonAnimationBlock
                                print "animationCount "+str(len(newAWDBlockAnimSet.poseBlockIDs))
                                if newAWDBlockAnimSet is not None:
                                    newAWDBlockAnimSet.poseBlockIDs.append(anim)    
        if exportThisObjChild==True:        
            if len(object.GetChildren())>0:                             # if the object has any Children:
               createSkeletonBlocks(object.GetChildren(),exportData,mainDialog,newAWDBlockAnimSet)# execute this function again, passing the children as objList


       
        
    
# build a new skeletonBlock 
def buildSkeleton(exportData,curObj):

    newAWDBlock=classesAWDBlocks.SkeletonBlock(int(curObj.GetTag(1028937).GetName()),0,curObj.GetTag(1028937)[1011],curObj)  # create a new block for the skeleton
    newAWDBlock.name=curObj.GetTag(1028937)[1011]                                                           # set the name of the AWDBlock
    newSkeleton=mainSkeletonHelper.SkeletonHelper(curObj,None,False)                                        # use the skeletonHelper to check if the skeletonBlock is a valid skeleton
    weightTags=newSkeleton.allWeightTags     
    if len(weightTags)==0:                                                                                  # if no weightTag is found:
        newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())                              # create a Warning that the Skeleton has no valid binding 
        exportData.AWDwarningObjects.append(newWarning)                                                         # append the warning to the warnings-list, so it will get displayed when finished
        
    buildSkeletonJoint([curObj],newAWDBlock.saveJointList,0,exportData,newAWDBlock)                         # build all the skeleton-joint-blokcs (bindingMatrix etc)
    for tag in newSkeleton.expressionTagsToRestore:                                                         # after reading the skeleton positions, we enabl
        tag[c4d.EXPRESSION_ENABLE]=True                                                                         # we enable the expression-tags that have been disabled by the skeletonHelper earlier

    exportData.allAWDBlocks[int(curObj.GetTag(1028937).GetName())].data=newAWDBlock
    exportData.allAWDBlocks[int(curObj.GetTag(1028937).GetName())].blockType=101
    exportData.allAWDBlocks[int(curObj.GetTag(1028937).GetName())].tagForExport=True
    
#recursive function to create all the jointBlocks for one Skeleton
def buildSkeletonJoint(jointObjs,jointList,parentID,exportData,skeletonBlock): 
    for jointObj in jointObjs:
        newJoint=classesAWDBlocks.jointBlock((len(jointList)+1),parentID,jointObj)          # create a new jointblock
        exportData.jointIDstoSkeletonBlocks[str(jointObj.GetName())]=skeletonBlock          # create a dictionary-entrance in jointIDStoSkeletonBlocks, so we can get the skeleton this joint is used by, by using the joints name 
        exportData.jointIDstoJointBlocks[str(jointObj.GetName())]=newJoint                  # create a dictionary-entrance in jointIDstoJointBlocks, so we can get the joints-index  by using its name
        newJoint.lookUpName=exportData.allAWDBlocks[int(jointObj.GetName())].name          # get the original joint-name

        newJoint.transMatrix=((jointObj.GetMg().__invert__()))                       # set the InversBindMatrix for this Joint        
        jointList.append(newJoint)                                                          # append this joint-block to the skeletonBlocks-jointList
        parentID2=(len(jointList))                                                          # get the parentID to use for the next joints 
        if len(jointObj.GetChildren())>0:                                                   # if the object has any childs:
            buildSkeletonJoint(jointObj.GetChildren(),jointList,parentID2,exportData,skeletonBlock) # execute the function for the childs 

# build a skeletonAnimationBlock
def buildSkeletonAnimation(exportData,curObj,mainDialog,skeletonAnimationTag):   
    globalMinFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)                                                            # get the first frame for the global animation range 
    globalMaxFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)                                                           # get the last frame for the global animation range
    minFrame=globalMinFrame                                                         # set the minFrame to the global minFrame
    maxFrame=globalMaxFrame                                                         # set the maxFrame to the global maxFrame
    animationRange=skeletonAnimationTag[1015]                                       # get the range mode of the current Animation
    if animationRange!=1021:                                                        # if it is not set to "Global" we update the minframe/maxFrame using the skeletonAnmiationTags input values
        minFrame=skeletonAnimationTag[1018]
        maxFrame=skeletonAnimationTag[1020]
        
    #print "Start Exporting Animation Range = "+str(minFrame)+"  -  "+str(maxFrame)
    
    curFrame=minFrame                                                                                           # set the first frame to be the current frame
    durationList=[]                                                                                             # list to store all frame-durations
    idList=[]  
    if skeletonAnimationTag[1021]==True:    
        keyLength=maxFrame-minFrame                                                                      # get the curve for this track
        keyCounter=0   
        keyTime=minFrame*(float(1000/exportData.doc.GetFps())/1000)
        durationTime=(float(1000/exportData.doc.GetFps())/1000)
        while keyCounter<keyLength: 
            durationList.append(durationTime)
            keyTime+=durationTime
            newTime=c4d.BaseTime(keyTime)
            newTime.Quantize(exportData.doc.GetFps())
            idList.append(buildSkeletonPose(exportData,curObj,newTime))
            keyCounter+=1
        buildSkeletonAnimationBlock(exportData,curObj,durationList,idList) 
        return 
        # list to store all frame-IDs
    track=curObj.GetFirstCTrack()                                                                               # get the first track of the curObj
    if track==None:                                                                                             # if no track is found
        durationList.append(1*exportData.doc.GetFps())                                                              # set only one duration
        idList.append(buildSkeletonPose(exportData,curObj,c4d.BaseTime((curFrame*exportData.doc.GetFps())/1000)))   # add one skeletonPoseBlock to the idLis
        buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)                                          # create a SkeletonAnimationBlock containing only one Frame
        return                                                                                                      # exit this function
    curve=track.GetCurve()                                                                                 # get the curve for this track
    keyCounter=0   
    keyCount=curve.GetKeyCount()  
    #print keyCount     
    firstKeyTime=None
    while keyCounter<keyCount:                                                                                  # iterate over the keyCount
        key=curve.GetKey(keyCounter)                                                                            # get a key   
        keyTime=key.GetTime()    
        if firstKeyTime < keyTime:
            firstKeyTime=keyTime
        #exportData.doc.SetTime(curTime)                                                                   # get a key   
        keyTimeInFrame=keyTime.GetFrame(exportData.doc.GetFps())
        exportData.allStatus+=float(10/float(curve.GetKeyCount()))                                                  # used to calculate processbar
        mainHelpers.updateCanvas(mainDialog,exportData)                                                             # update processbar
        # if the keys time is within the range to export:
        if float(keyTimeInFrame)>=float(minFrame) and float(keyTimeInFrame)<=float(maxFrame):
            if (keyCounter+1)<keyCount:# if this is not the last key, we calculate the duration-time like this: durationTime = nextKeyTime - thisKeyTime
                durationList.append(float(curve.GetKey(keyCounter+1).GetTime().Get())-float(keyTime.Get()))
            if (keyCounter+1)>=keyCount:# if this is the last keyframe within the range, we set its duration 
                endDuration=float(maxFrame*float(1000/exportData.doc.GetFps())/float(1000))-float(keyTime.Get())
                if endDuration<=0:
                    endDuration=0
                durationList.append(endDuration)#100*(1000/exportData.doc.GetFps()))
            idList.append(buildSkeletonPose(exportData,curObj,keyTime))
        keyCounter+=1
    if firstKeyTime is not None:
        #durationList.append((1000/exportData.doc.GetFps())/1000)
        pass#print durationList
        #idList.append(buildSkeletonPose(exportData,curObj,firstKeyTime))
    return buildSkeletonAnimationBlock(exportData,curObj,durationList,idList)                                          # create the SkeletonAnimationBlock 

def buildSkeletonAnimationBlock(exportData,curObj,durationList,idList):   
    newAWDBlock=classesAWDBlocks.SkeletonAnimationBlock(int(curObj.GetTag(1028938).GetName()),0,curObj.GetTag(1028938)[1011],len(durationList)) # create a new AWDSkeletonAnimationBlock
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    newAWDBlock.framesDurationsList=durationList
    newAWDBlock.framesIDSList=idList
    #exportData.allSkeletonAnimations.append(newAWDBlock)
    exportData.allAWDBlocks[int(curObj.GetTag(1028938).GetName())].data=newAWDBlock
    exportData.allAWDBlocks[int(curObj.GetTag(1028938).GetName())].blockType=103
    exportData.allAWDBlocks[int(curObj.GetTag(1028938).GetName())].tagForExport=True
    return exportData.allAWDBlocks[int(curObj.GetTag(1028938).GetName())]

# creates a new SkeletonPoseBlock - called by "buildSkeletonAnimation()"
def buildSkeletonPose(exportData,curObj,curTime): 

    
    newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(None,"",0)
    exportData.allAWDBlocks.append(newAWDWrapperBlock)  
    
    newAWDBlock=classesAWDBlocks.SkeletonPoseBlock(exportData.idCounter,0,curObj.GetTag(1028938)[1011])
    exportData.idCounter+=1
    newAWDBlock.name=curObj.GetTag(1028938)[1011]
    c4d.documents.SetDocumentTime(exportData.doc, curTime)# set original Time
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_NO_REDUCTION|c4d.DRAWFLAGS_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW)
    c4d.GeSyncMessage(c4d.EVMSG_ASYNCEDITORMOVE)
    newAWDBlock.transformations=[]
    buildJointTransform([curObj],newAWDBlock.transformations,exportData,True) # recursive function to get all Joints as JointBlocks
    newAWDWrapperBlock.data=newAWDBlock
    newAWDWrapperBlock.blockType=102
    newAWDWrapperBlock.tagForExport=True
    return newAWDWrapperBlock
    
# saves the skeleton-joint-matricies while playing trough timeline - called by "buildSkeletonPose()"
def buildJointTransform(curObjList,jointTransforms,exportData,firstJoint):   
    for curObj in curObjList:
        if firstJoint==False:
            newMatrix=curObj.GetMl()    
        if firstJoint==True:
            newMatrix=curObj.GetMg()
        newMatrix.off=newMatrix.off*exportData.scale
        jointTransforms.append(newMatrix)
        if len(curObj.GetChildren())>0:
            buildJointTransform(curObj.GetChildren(),jointTransforms,exportData,False)
            
    


