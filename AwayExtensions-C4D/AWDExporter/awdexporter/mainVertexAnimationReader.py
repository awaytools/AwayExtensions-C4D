# functions running in the c4d-main-thread

# some functions to convert skeleton-animations from c4d to awd2-data

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers
from awdexporter import mainSkeletonHelper

# this is the function that gets called from the "mainExporter"
def getVertexAnimationData(objList,exportData,mainDialog,newAWDBlockAnimSetoriginal=None):
    for object in objList:      
        newAWDBlockAnimSet=newAWDBlockAnimSetoriginal                          
        exportThisObj=True
        exportThisObjChild=True            
        exporterSettingsTag=object.GetTag(1028905)
        if exporterSettingsTag is not None:
            if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== True:                             
                exportThisObj=False
                exportThisObjChild=False
            if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== False:
                exportThisObj=False
                exportThisObjChild=True
        if exportThisObj==True: 
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
            if tag is None:
                alltags=object.GetTags()
                for animTag in alltags:
                    if animTag.GetType()==1030484:
                        vertexAnimationTag=animTag            
                        if vertexAnimationTag is not None:                      
                            if vertexAnimationTag[1010]==True:                     
                                if vertexAnimationTag[1011] is not None:       
                                    if vertexAnimationTag[1050] is None: 
                                        print "ERROR = No Animation-Target Set"
                                    if vertexAnimationTag[1050] is not None: 
                                        if str(vertexAnimationTag[1050].GetName())==str(object.GetName()):
                                            print "ERROR = Animation Data must not target itself"
                                        if str(vertexAnimationTag[1050].GetName())!=str(object.GetName()):
                                            anim=buildVertexAnimation(exportData,object,mainDialog,vertexAnimationTag) 
                                            if exportData.debug==True:
                                                print "Animationset = "+str(newAWDBlockAnimSet)
                                            if newAWDBlockAnimSet is not None and anim.blockType==112:                                            
                                                newAWDBlockAnimSet.poseBlockIDs.append(anim)                           
        if exportThisObjChild==True:        
            if len(object.GetChildren())>0:                           
               getVertexAnimationData(object.GetChildren(),exportData,mainDialog,newAWDBlockAnimSet)


    

# build a skeletonAnimationBlock
def buildVertexAnimation(exportData,curObj,mainDialog,vertexAnimationTag):   
    globalMinFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)                                                            # get the first frame for the global animation range 
    globalMaxFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)                                                           # get the last frame for the global animation range
    minFrame=globalMinFrame                                                         # set the minFrame to the global minFrame
    maxFrame=globalMaxFrame                                                         # set the maxFrame to the global maxFrame
    animationRange=vertexAnimationTag[1015]                                       # get the range mode of the current Animation
    if animationRange!=1021:                                                        # if it is not set to "Global" we update the minframe/maxFrame using the skeletonAnmiationTags input values
        minFrame=vertexAnimationTag[1018]
        maxFrame=vertexAnimationTag[1020]
        
    #print "Start Exporting Animation Range = "+str(minFrame)+"  -  "+str(maxFrame)
    
    keyFrameStyle=vertexAnimationTag[1054]   
    curFrame=minFrame                                                                                           # set the first frame to be the current frame
    frameDurations=[]                                                                                             # list to store all frame-durations
    framePositions=[]  
    lastFramesDuration=0
    keyTime=minFrame*(float(1000/exportData.doc.GetFps())/1000)
    if keyFrameStyle==1055 or keyFrameStyle==1058:
        if keyFrameStyle==1055:    # all Frames
            keyLength=maxFrame-minFrame    
            durationTime=(float(1000/exportData.doc.GetFps())/1000)
        if keyFrameStyle==1058:  # keyframe Number   
            allKeysLength=maxFrame-minFrame            
            keyLength=vertexAnimationTag[1061] 
            difKey=allKeysLength-keyLength
            keyLength2=float(difKey/(keyLength-1))
            durationTime=(float(1000/exportData.doc.GetFps())/1000)  
            durationTime+=float((float(1000/exportData.doc.GetFps())/1000)*(keyLength2))
        keyCounter=0   
        while keyCounter<keyLength: 
            if keyCounter==(keyLength-1):
                durationTime=lastFramesDuration      
            frameDurations.append(durationTime)
            keyTime+=durationTime
            newTime=c4d.BaseTime(keyTime)
            #if keyFrameStyle==1055:    # all Frames
            #    newTime.Quantize(exportData.doc.GetFps())
            framePositions.append(getMeshPosePosition(exportData,curObj,newTime,vertexAnimationTag[1051]))
            keyCounter+=1        
    
    if keyFrameStyle==1056 or keyFrameStyle==1057:
        if keyFrameStyle==1056:
            cloneObj= curObj.GetClone() 
            firstTrack=cloneObj.GetFirstCTrack()
            firstCurve=firstTrack.GetCurve()   
            tracks=curObj.GetCTracks()
            keysDic={}
            keysList=[]
            keysList2=[]
            for track in tracks:   
                curve=track.GetCurve() 
                keyCounter=0    
                while keyCounter<curve.GetKeyCount(): 
                    key=curve.GetKey(keyCounter)   
                    keyTime=key.GetTime()      
                    isKey=firstCurve.FindKey(keyTime)         
                    if isKey is None:
                        firstCurve.AddKey(keyTime)                                                      
                    keyCounter+=1  
        if keyFrameStyle==1057:     
            tracks=curObj.GetTag(1030484).GetCTracks()
            if tracks is not None:
                for track in tracks:
                    testerString="(1052, 130, 1030484)"
                    if testerString==str(track.GetDescriptionID()):
                        firstCurve=track.GetCurve()  
        if firstCurve is None:
            pass
        if firstCurve is not None:
            keyCounter=0   
            frametimes=[] 
            startOffset=0
            firstKeyTime=None
            while keyCounter<firstCurve.GetKeyCount():        
                key=firstCurve.GetKey(keyCounter)    
                keyTimeInFrame=key.GetTime().GetFrame(exportData.doc.GetFps())
                if float(keyTimeInFrame)>=float(minFrame) and float(keyTimeInFrame)<=float(maxFrame):
                    if firstKeyTime is None:
                        firstKeyTime=key.GetTime().Get()
                    if firstKeyTime!=startOffset:
                        startOffset=firstKeyTime
                    frametimes.append(c4d.BaseTime(key.GetTime().Get()-firstKeyTime))                                                     
                keyCounter+=1
            if len(frametimes)==0:
                frametimes.append(c4d.BaseTime(0))
            endOffset=float((float(1000/exportData.doc.GetFps())/1000)*(maxFrame))-(frametimes[len(frametimes)-1].Get()+startOffset)
            keyCounter=0   
            #print keyCount     
            firstKeyTime=None
            keyCount=len(frametimes)
            for keyBaseTime in frametimes:
                keyTime=keyBaseTime.Get()
                exportData.allStatus+=float(10/float(keyCount)) 
                mainHelpers.updateCanvas(mainDialog,exportData)   
                if (keyCounter+1)<keyCount:
                    frameDurations.append(float(frametimes[keyCounter+1].Get())-float(keyTime))
                if (keyCounter+1)>=keyCount:
                    endDuration=startOffset+endOffset
                    if endDuration<=0:
                        endDuration=0
                    frameDurations.append(endDuration)
                framePositions.append(getMeshPosePosition(exportData,curObj,c4d.BaseTime(keyTime+startOffset),vertexAnimationTag[1051]))
                keyCounter+=1
                       
    if len(frameDurations)==1:
        newAnimBlock=buildMeshPoseBlock(exportData,curObj,frameDurations,framePositions,vertexAnimationTag) 
    if len(frameDurations)>1:
        newAnimBlock=buildMeshPoseAnimationBlock(exportData,curObj,frameDurations,framePositions,vertexAnimationTag) 
    return newAnimBlock
                                          # create the SkeletonAnimationBlock 



def buildMeshPoseAnimationBlock(exportData,curObj,durationList,positionList,vertexAnimationTag):   
    if exportData.debug==True:
        print "Build Mesh Pose Animation"
    newAWDBlock=classesAWDBlocks.MeshPoseAnimationBlock(int(vertexAnimationTag.GetName()),0,vertexAnimationTag[1011],len(durationList))
    newAWDBlock.name=vertexAnimationTag[1011]
    newAWDBlock.targetMesh=int(vertexAnimationTag[1050].GetName())
    newAWDBlock.frameDurations=durationList
    newAWDBlock.framePoints=positionList
    exportData.allAWDBlocks[int(vertexAnimationTag[1050].GetName())].data.poseAnimationBlocks.append(newAWDBlock)
    exportData.allVertexAnimations.append(newAWDBlock)
    if vertexAnimationTag[1053]!=True:
        newAWDBlock.savePoseProps.append(1)
    if vertexAnimationTag[1059]!=False:
        newAWDBlock.savePoseProps.append(2)
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].data=newAWDBlock
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].blockType=112
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].tagForExport=True
    return exportData.allAWDBlocks[int(vertexAnimationTag.GetName())]
    
def buildMeshPoseBlock(exportData,curObj,durationList,positionList,vertexAnimationTag):   
    if exportData.debug==True: 
        print "Build Mesh Pose"
    newAWDBlock=classesAWDBlocks.MeshPoseBlock(int(vertexAnimationTag.GetName()),0,vertexAnimationTag[1011]) # create a new AWDSkeletonAnimationBlock
    newAWDBlock.name=vertexAnimationTag[1011]
    newAWDBlock.targetMesh=int(vertexAnimationTag[1050].GetName())
    newAWDBlock.duration=durationList[0]
    newAWDBlock.points=positionList[0]
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].data=newAWDBlock
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].blockType=111
    exportData.allAWDBlocks[int(vertexAnimationTag.GetName())].tagForExport=True
    return exportData.allAWDBlocks[int(vertexAnimationTag.GetName())]

# creates a new SkeletonPoseBlock - called by "buildSkeletonAnimation()"
def getMeshPosePosition(exportData,curObj,curTime, doCopy):   
    
    c4d.documents.SetDocumentTime(exportData.doc, curTime)# set original Time
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_NO_REDUCTION|c4d.DRAWFLAGS_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW)
    c4d.GeSyncMessage(c4d.EVMSG_ASYNCEDITORMOVE)
    
    newPositions=[] 
    extraRemove=None
    if doCopy==True:
        exportData.doc.SetActiveObject(curObj,c4d.SELECTION_NEW)
        c4d.CallCommand(12233)
        curObj=curObj.GetNext()        
        if curObj.GetType()!=c4d.Opolygon:
            extraRemove=curObj
            curObj=curObj.GetDown()   
                
    newPositions=getPositions(curObj,exportData) 
    if doCopy==True:
        curObj.Remove()
        if extraRemove is not None:
            extraRemove.Remove()
    return newPositions
    
# saves the skeleton-joint-matricies while playing trough timeline - called by "buildSkeletonPose()"
def getPositions(curObj,exportData):   
    exportData.doc.SetActiveObject(curObj,c4d.SELECTION_NEW)
    newList=[]
    newList=curObj.GetAllPoints()
    return newList
            
    


