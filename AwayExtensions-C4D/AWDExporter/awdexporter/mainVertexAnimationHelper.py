import c4d
from c4d import gui
    
# build a skeletonAnimationBlock
def setNewtracks(curCurve,curObj,newObj,vertexAnimationTag,doc):   
    globalMinFrame=0#mainDialog.GetReal(ids.REAL_FIRSTFRAME)                                                            # get the first frame for the global animation range 
    globalMaxFrame=25#mainDialog.GetReal(ids.REAL_LASTFRAME)                                                           # get the last frame for the global animation range
    minFrame=globalMinFrame                                                         # set the minFrame to the global minFrame
    maxFrame=globalMaxFrame                                                         # set the maxFrame to the global maxFrame
    
    animationRange=vertexAnimationTag[1015]                                       # get the range mode of the current Animation
    if animationRange!=1021:                                                        # if it is not set to "Global" we update the minframe/maxFrame using the skeletonAnmiationTags input values
        minFrame=vertexAnimationTag[1018]
        maxFrame=vertexAnimationTag[1020]
        
    #print "Start Exporting Animation Range = "+str(minFrame)+"  -  "+str(maxFrame)
    firstCurve=None
    keyFrameStyle=vertexAnimationTag[1054]   
    curFrame=minFrame                                                                                           # set the first frame to be the current frame
    frameDurations=[]                                                                                             # list to store all frame-durations
    framePositions=[]  
    lastFramesDuration=0
    keyTime=minFrame*(float(1000/doc.GetFps())/1000)
    if keyFrameStyle==1055 or keyFrameStyle==1058:
        if keyFrameStyle==1055:    # all Frames
            keyLength=maxFrame-minFrame    
            durationTime=(float(1000/doc.GetFps())/1000)
        if keyFrameStyle==1058:  # keyframe Number   
            allKeysLength=maxFrame-minFrame            
            keyLength=vertexAnimationTag[1061] 
            difKey=allKeysLength-keyLength
            keyLength2=float(difKey/(keyLength))
            durationTime=(float(1000/doc.GetFps())/1000)  
            durationTime+=float((float(1000/doc.GetFps())/1000)*(keyLength2))
        keyCounter=0   
        while keyCounter<=keyLength: 
            #if keyCounter==(keyLength-1):
            #    durationTime=lastFramesDuration      
            frameDurations.append(durationTime)
            if keyCounter>0:
                keyTime+=durationTime
            newTime=c4d.BaseTime(keyTime)
            #if keyFrameStyle==1055:    # all Frames
            #    newTime.Quantize(exportData.doc.GetFps())
            framePositions.append(setMeshPosePosition(curObj,newTime,vertexAnimationTag[1051],curCurve,newObj,doc))
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
        if firstCurve is not None:
            keyCounter=0   
            frametimes=[] 
            startOffset=0
            firstKeyTime=None
            while keyCounter<firstCurve.GetKeyCount():        
                key=firstCurve.GetKey(keyCounter)    
                keyTimeInFrame=key.GetTime().GetFrame(doc.GetFps())
                if float(keyTimeInFrame)>=float(minFrame) and float(keyTimeInFrame)<=float(maxFrame):
                    if firstKeyTime is None:
                        firstKeyTime=key.GetTime().Get()
                    if firstKeyTime!=startOffset:
                        startOffset=firstKeyTime
                    frametimes.append(c4d.BaseTime(key.GetTime().Get()-firstKeyTime))                                                     
                keyCounter+=1
            if len(frametimes)==0:
                frametimes.append(c4d.BaseTime(0))
            endOffset=float((float(1000/doc.GetFps())/1000)*(maxFrame))-(frametimes[len(frametimes)-1].Get()+startOffset)
            keyCounter=0   
            #print keyCount     
            firstKeyTime=None
            keyCount=len(frametimes)
            for keyBaseTime in frametimes:
                keyTime=keyBaseTime.Get()
                if (keyCounter+1)<keyCount:
                    frameDurations.append(float(frametimes[keyCounter+1].Get())-float(keyTime))
                if (keyCounter+1)>=keyCount:
                    endDuration=startOffset+endOffset
                    if endDuration<=0:
                        endDuration=0
                    frameDurations.append(endDuration)
                framePositions.append(setMeshPosePosition(curObj,c4d.BaseTime(keyTime+startOffset),vertexAnimationTag[1051],curCurve,newObj,doc))
                keyCounter+=1
                
    return

def setMeshPosePosition(curObj,curTime, doCopy,curTrack,newObj,doc):   
    
    c4d.documents.SetDocumentTime(doc, curTime)# set original Time
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_NO_REDUCTION|c4d.DRAWFLAGS_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    c4d.DrawViews( c4d.DRAWFLAGS_FORCEFULLREDRAW)
    c4d.GeSyncMessage(c4d.EVMSG_ASYNCEDITORMOVE)
    
    newPositions=[] 
    extraRemove=None
    if doCopy==True:
        doc.SetActiveObject(curObj,c4d.SELECTION_NEW)
        c4d.CallCommand(12233)
        stateObj=curObj.GetNext()        
        curObj=getPolyObject(stateObj)
                
    newPositions=getPositions(curObj,doc) 
    thisCurve=curTrack.GetCurve()            
    dictKey = thisCurve.AddKey(curTime)
    key = dictKey["key"]
    newObj.SetAllPoints(newPositions)
    newObj.Message(c4d.MSG_UPDATE)
    curTrack.FillKey(doc,newObj,key)
    if doCopy==True:
        stateObj.Remove()
    return newPositions
    
# saves the skeleton-joint-matricies while playing trough timeline - called by "buildSkeletonPose()"
def getPositions(curObj,doc):   
    doc.SetActiveObject(curObj,c4d.SELECTION_NEW)
    newList=[]
    newList=curObj.GetAllPoints()
    return newList

def getPolyObject(thisObj):
    if thisObj.GetType()==c4d.Opolygon:
        return thisObj.GetClone()
    for child in thisObj.GetChildren():
        returneFromChild=getPolyObject(child) 
        if returneFromChild is not None:
            return returneFromChild
    return None
    

def createAnimationObject(curObj, animTag,newName,doc):
    
    #newObj=curObj.GetClone()
    #doc.InsertObject(newObj)
    doc.SetActiveObject(curObj,c4d.SELECTION_NEW)
    c4d.CallCommand(12233)# perform "current state to object" on the selected object
    # search the newly created object
    stateObj=curObj.GetNext() 
    newObj=getPolyObject(stateObj)
    stateObj.Remove()
    doc.InsertObject(newObj,curObj.GetUp(),curObj)
        
    cleanTracks(newObj)
    id = c4d.DescID(c4d.DescLevel(c4d.CTpla, c4d.CTpla, 0))
    plaTrack = c4d.CTrack(newObj, id)
    newObj.InsertTrackSorted(plaTrack)
    setNewtracks(plaTrack,curObj,newObj,animTag,doc)
    newAnimationTag=newObj.GetTag(1030484)
    newAnimationTag[1054]=1056
    newAnimationTag[1051]=False
    newAnimationTag[1010]=True
    newAnimationTag[1011]=newName
    animTag[1010]=False
    newObj.SetName(newName)
    c4d.EventAdd()
    
def cleanTracks(object):
    allowedTags=[]
    allowedTags.append(c4d.Tweights)
    allowedTags.append(c4d.Tposemorph)
    #allowedTags.append(1030484)
    #allowedTags.append(5671)
    #allowedTags.append(5616)
    #allowedTags.append(5612)
    for track in object.GetCTracks():
        track.Remove()
    for child in object.GetChildren():
        child.Remove()
    for tag in object.GetTags():
        tagtype=tag.GetType()
        isAllowed=True
        if tag[c4d.EXPRESSION_ENABLE]:
            tag[c4d.EXPRESSION_ENABLE]=False   
        for allowedTagType in allowedTags:              
            if tagtype == allowedTagType:
                isAllowed=False
        if isAllowed==False:
            tag.Remove() 

