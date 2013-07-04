# functions that will run inside the background-worker-thread
# more-functions for mesh-converting 
import math
import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import classesHelper
   
# returns a new Material-list, conatining only one Material that is applied to all the polygons. 
def clearSubmeshIndexe(meshBlock,materialList):
    count=len(meshBlock.sceneObject.GetAllPolygons()) 
    for index in xrange(count): 
        materialList[0][1].selectionIndexe.append(1) 
    while len(materialList)>1:
        materialList.pop(len(materialList)-1)
    return materialList

# if a polygon is used by multiply selections ons different meshInstances, we create a new Selection for this polygons.
def createNewMultiSelection(meshBlock,materialList,foundIndicies,newMatDic):
    newMatName=""
    matCnt=0
    while matCnt<len(foundIndicies):
        newMatName+=str(materialList[foundIndicies[matCnt]][1].name)+"#"
        matCnt+=1
    foundMat=newMatDic.get(newMatName,None)
    if foundMat is None:
        foundMat=[]
        foundMat.append(str(1))  
        foundMat.append(classesHelper.PolySelection(newMatName,[]))
        foundMat.append(None)  
        matCnt=0
        while matCnt<len(foundIndicies):
            foundMat[1].multiNames.append(str(materialList[foundIndicies[matCnt]][1].name))
            foundMat[1].multiMats.append(str(materialList[foundIndicies[matCnt]][0]))
            matCnt+=1
        count=len(meshBlock.sceneObject.GetAllPolygons()) 
        for index in xrange(count): 
            foundMat[1].selectionIndexe.append(0)
        newMatDic[newMatName]=foundMat
        foundMat[1].isUsed=True
        materialList.append(foundMat)
    return foundMat

# loops trough all polygons of a mesh and make shure every polygon has only one material Applied - for polygons that are applied to different materials, a "merged material" is created
def mergeMaterialRestriction(meshBlock,materialList):
    count=len(meshBlock.sceneObject.GetAllPolygons()) 
    newMatDic={}
    for index in xrange(count): 
        foundIndicies=[]
        materialCnt=1
        while materialCnt <len(materialList):
            if index>=len(materialList[materialCnt][1].selectionIndexe):
                materialList[materialCnt][1].selectionIndexe.append(0)
            if materialList[materialCnt][1].selectionIndexe[index]==1:
                foundIndicies.append(materialCnt)
            materialCnt+=1
        if len(foundIndicies)>0:
            materialList[0][1].selectionIndexe[index]=0
            if len(foundIndicies)==1:
                materialList[foundIndicies[0]][1].isUsed=True   
            if len(foundIndicies)>1:
                materialList[(len(foundIndicies)-1)][1].isUsed=True            
                foundCnt=0
                while foundCnt<(len(foundIndicies)):
                    materialList[foundIndicies[foundCnt]][1].selectionIndexe[index]=0
                    foundCnt+=1
                createNewMultiSelection(meshBlock,materialList,foundIndicies,newMatDic)[1].selectionIndexe[index]=1
        if len(foundIndicies)==0:
            materialList[0][1].isUsed=True
            materialList[0][1].selectionIndexe[index]=1
    newMaterials=[]        
    for mat in materialList: 
        #
        "Mat = "+str(mat[1].name)+"  /  "+str(mat[1].isUsed)
        if mat[1].isUsed==True:
            newMaterials.append(mat)
            
    return newMaterials  
    
# loops trough all polygons of a mesh and make shure every polygon has only one material Applied
def cleanMaterialRestriction(meshBlock,materialList):
    count=len(meshBlock.sceneObject.GetAllPolygons()) 
    for index in xrange(count): 
        foundIndicies=[]
        materialCnt=1
        while materialCnt <len(materialList):
            if materialList[materialCnt][1].selectionIndexe[index]==1:
                foundIndicies.append(materialCnt)
            materialCnt+=1
        if len(foundIndicies)>0:
            materialList[0][1].selectionIndexe.append(0)
            if len(foundIndicies)==1:
                materialList[foundIndicies[0]][1].isUsed=True   
            if len(foundIndicies)>1:
                materialList[(len(foundIndicies)-1)][1].isUsed=True            
                foundCnt=0
                while foundCnt<(len(foundIndicies)-1):
                    materialList[foundIndicies[foundCnt]][1].selectionIndexe[index]=0
                    foundCnt+=1
        if len(foundIndicies)==0:
            materialList[0][1].isUsed=True
            materialList[0][1].selectionIndexe.append(1) 
    newMaterials=[]        
    for mat in materialList: 
        #print "Mat = "+str(mat[1].name)+"  /  "+str(mat[1].isUsed)
        if mat[1].isUsed==True:
            newMaterials.append(mat)
            
    return newMaterials   


           
#checks if a vert/normal/uv - combination allready exists in the uniquePool of the given Submesh.
def buildSharedPoint(exportData,faceStyle,meshBlock,curMesh,curPoint,curUV,curSubMesh,pointNr,normal,normalf,anglelimit,useAngle,isEdgeBreak,animations,subMeshNr):
                    
        
    checkerstring=str(curPoint)             # get the vector as string to use as "dictionary-look-up-key"
    if curUV!=None:                         # if uv values are given:
        checkerstring+="#"+str(curUV)           #  add them to the string
        
    # for the real "dictionary-look-up", we create another string. it consitsts of the previous created string plus a "0" for first point on this position (+uv).
    # if another point will be found at this position (+uv), we add it to the dictionary with the same key, but instead of a 0 we use a 1
    checkerstring2=checkerstring+str(0)    
    pointIndex=-1
    #pointMorphedIndex=-1
            
    if meshBlock.pointsUsed[pointNr]==True:                                     # only do if the point has allready been used
        if isEdgeBreak==1:                                                          # if the point is on a edge break, we need do make shure its parsed as a new point
            phongbreaknr1=0                                                         
            allkeyslength=len(curSubMesh.uniquePoolDict)
            while phongbreaknr1<allkeyslength:
                checkerstring2=checkerstring+str(phongbreaknr1)
                pointIndex2=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
                if pointIndex2 ==-1:
                    phongbreaknr=phongbreaknr1
                    break
                phongbreaknr1+=1
                    
        if isEdgeBreak==0:#the point is not on a edge break, so we need to find all points that are sharing this position and calculate the angle between there face normals.  
            pointIndex=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
            if pointIndex>=0:
                if useAngle==True:
                    angle=c4d.utils.VectorAngle(curSubMesh.faceNormal[pointIndex].GetNormalized(), normalf.GetNormalized())
                    if angle>=anglelimit:
                        allkeyslength=len(curSubMesh.uniquePoolDict)
                        phongbreaknr=1
                        while phongbreaknr<allkeyslength:
                            checkerstring2=checkerstring+str(phongbreaknr)
                            pointIndex=curSubMesh.uniquePoolDict.get(checkerstring2,-1)  
                            if pointIndex ==-1:
                                break
                            if pointIndex >= 0:
                                angle=c4d.utils.VectorAngle(curSubMesh.faceNormal[pointIndex].GetNormalized(), normalf.GetNormalized())
                                if angle<anglelimit:
                                    phongbreaknr=allkeyslength
                            phongbreaknr+=1
                                        
                                        
                                    
        #if pointIndex==-1:
        #    if checkerstring in curSubMesh.uniquePoolMorphed:
        #        pointMorphedIndex=curSubMesh.uniquePoolMorphed.index(checkerstring)   
                 
    #if pointMorphedIndex>=0:
    #    curSubMesh.indexBuffer.append(pointIndex) 
    if pointIndex>=0:
        if str(faceStyle)=="tri":
            curSubMesh.indexBuffer.append(pointIndex)        
        if str(faceStyle)=="quad":
            curSubMesh.quadBuffer.append(pointIndex)
        #curSubMesh.indexBufferMorphed.append("p")   
                
    if pointIndex==-1:# and pointMorphedIndex==-1:
        meshBlock.pointsUsed[pointNr]=True   
        buildPoint(exportData,faceStyle,meshBlock,curMesh,curSubMesh,curPoint,pointNr,curUV,normal,normalf,checkerstring2,animations,subMeshNr)

                         
def buildPoint(exportData,faceStyle,meshBlock,curMesh,curSubMesh,curPoint,pointNr,curUv,curNormal=None,curNormalf=None,checkerstring=None,animations=None,subMeshNr=None):
                     
    ismorph=False
    #morphCounter=0
    #while morphCounter<len(morphes):
        #morphedPoint=morphes[morphCounter].morphedPoints[pointNr]
        #if curPoint.x!=morphedPoint.x or curPoint.y!=morphedPoint.y or curPoint.z!=morphedPoint.z:
            #relativeMorph=str(len(curSubMesh.vertexBufferMorphed))+"#"
            #relativeMorph+=str(curPoint.x-morphedPoint.x)+"#"
            #relativeMorph+=str(curPoint.y-morphedPoint.y)+"#"
            #relativeMorph+=str(curPoint.z-morphedPoint.z)
            #curSubMesh.morphs[morphCounter][2]=True
            #curSubMesh.morphs[morphCounter][0].append(relativeMorph)
            #ismorph=True
        #morphCounter+=1
    weights=None
    joints=None
    if meshBlock.weightTag is not None:#if the mesh is skinned to one valid skeleton, we collect the weights and JointIndicies used by this point:
        jointcounter=0
        weights=[]  
        joints=[] 
        jointCount=meshBlock.weightTag.GetJointCount()
        while jointcounter<jointCount:   
            newWeight=meshBlock.weightTag.GetWeight(jointcounter,pointNr)
            newJoint=meshBlock.weightTag.GetJoint(jointcounter)
            if newWeight>0 and newJoint is not None:
                newIndex=exportData.jointIDstoJointBlocks[str(newJoint.GetName())].jointID-1
                if newIndex>=0:
                    weights.append(newWeight)
                    joints.append(newIndex) 
                ismorph=False
            jointcounter+=1      
    if ismorph==False:
        if str(faceStyle)=="tri":
            curSubMesh.indexBuffer.append(len(curSubMesh.vertexBuffer))        
        if str(faceStyle)=="quad":
            curSubMesh.quadBuffer.append(len(curSubMesh.vertexBuffer))

        if checkerstring is not None:
            curSubMesh.uniquePoolDict[checkerstring]=len(curSubMesh.vertexBuffer)
        #curSubMesh.indexBufferMorphed.append("p") 
        curSubMesh.vertexBuffer.append(curPoint)
        if animations is not None:
            for anim in animations:
                frameCnt=0
                while frameCnt<len(anim.frameSubMeshStreams):
                    anim.frameSubMeshStreams[frameCnt][subMeshNr].append(anim.framePoints[frameCnt][pointNr])
                    frameCnt+=1
                
        #curSubMesh.sharedvertexBuffer.append(-1) faceStyle
        if curUv is not None:
            curSubMesh.uvBuffer.append(curUv)
        if curNormal is not None:
            curSubMesh.normalBuffer.append(curNormal)
        if curNormalf is not None:
            curSubMesh.faceNormal.append(curNormalf)
        if weights is not None:
            curSubMesh.weightsBuffer.append(weights)
        if joints!= None:
            curSubMesh.jointidxBuffer.append(joints)



"""

        if ismorph==True:
            curSubMesh.indexBuffer.append(len(curSubMesh.vertexBufferMorphed))
            curSubMesh.indexBufferMorphed.append("m")  
            curSubMesh.vertexBufferMorphed.append(curPoint) 
            curSubMesh.sharedvertexBufferMorphed.append(-1) 
            if curUV != None:
                curSubMesh.uvBufferMorphed.append(curUV)
            curSubMesh.uniquePoolMorphed.append(checkerstring)
            curSubMesh.weightsBuffer.append(weights)
            curSubMesh.jointidxBuffer.append(joints) 
"""  
                        

# this is the main - mesh-parsing function....  it loops through all polygons, and created all data for all submeshes          
def collectSubmeshData(meshBlock,exportData,workerthreat):
    animations=meshBlock.poseAnimationBlocks
    allSubMeshCount=len(meshBlock.saveSubMeshes) # the length of all submeshes, needed for looping through all submeshes, to check which of it should get the current polygon  applied
    exportData.useInsteadSubMeshDic = {} # dictionary to translate submeshes that have reached their ressourcelimits to new created submeshes
    usePhong=False  # if true, the object has a phong tag applied, and the phong shading will be considered (shared verticles)
    usePhongAngle=False # if true a maximal phongangle is set in the phongTag, and it will be considered (shared verticles)
    useEdgeBreaks=False # if true a edgeBreaks are set in the phongTag, and it will be considered (shared verticles)
    edgebreaks=None # the edgebreaks
    phoneAngle=-1 # the max PhongeAngle
    normalData=meshBlock.sceneObject.CreatePhongNormals() # create the normalData for the Object
    normalCounter=0 
    for anim in animations:
        anim.frameSubMeshStreams=[]
        anim.saveFrameSubMeshStreams=[]
        frameCnt=0
        while frameCnt<len(anim.framePoints):
            newList=[]
            newSaveList=[]
            for subMesh in meshBlock.saveSubMeshes:
                newPointsList=[]
                newSavePointsList=[]
                newList.append(newPointsList)  
                newSaveList.append(newSavePointsList)            
            anim.frameSubMeshStreams.append(newList)      
            anim.saveFrameSubMeshStreams.append(newSaveList)
            frameCnt+=1
            
            
            
    phongTag=meshBlock.sceneObject.GetTag(c4d.Tphong)
    if phongTag is not None:
        usePhong=True
        usePhongAngle=phongTag[c4d.PHONGTAG_PHONG_ANGLELIMIT]
        useEdgeBreaks=phongTag[c4d.PHONGTAG_PHONG_USEEDGES]
        phoneAngle=phongTag[c4d.PHONGTAG_PHONG_ANGLE]
        if useEdgeBreaks==True:
            edgebreaks=meshBlock.sceneObject.GetPhongBreak()
        
    allOldPoints=meshBlock.sceneObject.GetAllPoints()
    meshBlock.pointsUsed=[]
    for point in allOldPoints:
        meshBlock.pointsUsed.append(False)
    polys=meshBlock.sceneObject.GetAllPolygons()    # get a list of all polygons
    count=len(polys)                                # get the llength of the polygon-list
    count2=float(10/float(count))                   # used to calulate the status of the progress bar
    uvTag=meshBlock.sceneObject.GetTag(c4d.Tuvw)                         # get the first UV-Tag applied to the mesh
    allFoundSelection=0# this will be incremeted for each polygon that was not exported correctly (should not happen)
    for faceIndex in xrange(count):                                     # iterate trough all polygons 
        if workerthreat.TestBreak():                                        # if the user cancelled the export, 
            return                                                              # we return
        exportData.subStatus=float(float(faceIndex)/float(count))           # used to update the progress bar
        exportData.allStatus+=count2                                        # used to update the progress bar
        oldpoints=polys[faceIndex]                                          # store the original point-indicies
                                              
        uva=uvb=uvc=uvd=None                                                
        if uvTag is not None :   
            uv = uvTag.GetSlow(faceIndex)     # we get the UVs for the Polygon and store them in "uv"
            uva=uv["a"]
            uvb=uv["b"]
            uvc=uv["c"]
            uvd=uv["d"]                
               
        faceStyle="tri"                 # set faceStyle to "tri", than we chack if we have to set it to "quad"
        if oldpoints.c!=oldpoints.d:    # if the pointIndex of the points c and d are not the same, this could be a "quad"
            if (str(allOldPoints[oldpoints.c]))!=(str(allOldPoints[oldpoints.d])):  # if the position of the both points are not the same, this is definitiv a "quad" 
                faceStyle="quad"
            if (str(allOldPoints[oldpoints.c]))==(str(allOldPoints[oldpoints.d])):  # if the position of the both points are the same:
                if uvTag is not None:   # if the object has uvs:
                    if str(uvc)!=str(uvd):  # if the uvs for the both points are note the same, this is a "quad"
                        faceStyle="quad"
                   
        normala=normalb=normalc=normald=None             
                            
        if usePhong==True: # if the phongshading should be considered:
        
            normalf=None # this will hold the normalVector of the Polygon
            if usePhongAngle==True: # if the PhongAngle should be considered, we calulate the normalVector (otherwise the normalVector will stay None)
                edge1=allOldPoints[oldpoints.a].__sub__(allOldPoints[oldpoints.c])
                edge2=allOldPoints[oldpoints.b].__sub__(allOldPoints[oldpoints.d])
                normalf=edge1.Cross(edge2)
                
            # get the normalVector of each Point
            normala=normalData[normalCounter]
            normalCounter+=1
            normalb=normalData[normalCounter]
            normalCounter+=1
            normalc=normalData[normalCounter]
            normalCounter+=1
            normald=normalData[normalCounter]
            normalCounter+=1
                                  
            isEdgeBreakA=isEdgeBreakB=isEdgeBreakC=isEdgeBreakD=isEdgeBreakD=isEdgeBreakA1=isEdgeBreakB1=isEdgeBreakC1=isEdgeBreakD1=0
            if edgebreaks is not None: # if edgeBreaks are used:
                # calculate the edgebreaks for the edges of this polygon 
                # the edgebreaks are given in Booleans for each Point of the Polygon, and we want to have them for each Line...
                isEdgeBreakA1=edgebreaks.IsSelected(4*faceIndex)
                isEdgeBreakB1=edgebreaks.IsSelected(4*faceIndex+1)
                isEdgeBreakC1=edgebreaks.IsSelected(4*faceIndex+3)
                     
                # first set the edges that will be the same calulation for both polgon-modes (tri/quad)
                if isEdgeBreakA1==True and isEdgeBreakB1==True:
                    isEdgeBreakA=1    
                if isEdgeBreakA1==True and isEdgeBreakB1==True:
                    isEdgeBreakB=1
                if isEdgeBreakB1==True and isEdgeBreakC1==True:
                    isEdgeBreakB=1    
                if isEdgeBreakB1==True and isEdgeBreakC1==True:
                    isEdgeBreakC=1
                            
                if str(faceStyle)=="tri": # than do the calulations unique for tri
                    if isEdgeBreakA1==True and isEdgeBreakC1==True:
                        isEdgeBreakA=1
                    if isEdgeBreakA1==True and isEdgeBreakC1==True:
                        isEdgeBreakC=1
                               
                if str(faceStyle)=="quad": # than do the calulations unique for tri
                    isEdgeBreakD1=edgebreaks.IsSelected(4*faceIndex+4)
                    if isEdgeBreakA1==True and isEdgeBreakD1==True:
                        isEdgeBreakA=1
                    if isEdgeBreakD1==True and isEdgeBreakC1==True:
                        isEdgeBreakC=1
                    if isEdgeBreakD1==True and isEdgeBreakA1==True:
                        isEdgeBreakD=1
                    if isEdgeBreakD1==True and isEdgeBreakC1==True:
                        isEdgeBreakD=1
        subcount=0     
        foundSelection=False# this should be allways set to true until end of this function, but you never know :)
        while subcount < allSubMeshCount:# loop trough all SubMeshes
            if meshBlock.saveSubMeshes[subcount].selectionIndexe[faceIndex]==1:  # if the polygon is selected by this submesh, the polygon will be insterted into this submesh
                subcount=checkForRessourceLimits(exportData,meshBlock,subcount,faceIndex,faceStyle,meshBlock.saveSubMeshes[subcount],animations) # check if this submesh has allready reached its limits. if it allready has, the index of the submesh to use instead is returned
                if usePhong==True:    # if phongshading should be considered, execute the "buildSharedPoint()" for each of the points of the polygon
                    buildSharedPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,allOldPoints[oldpoints.a],uva,meshBlock.saveSubMeshes[subcount],oldpoints.a,normala,normalf,phoneAngle,usePhongAngle,isEdgeBreakA,animations,subcount)
                    buildSharedPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,allOldPoints[oldpoints.b],uvb,meshBlock.saveSubMeshes[subcount],oldpoints.b,normalb,normalf,phoneAngle,usePhongAngle,isEdgeBreakB,animations,subcount)
                    buildSharedPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,allOldPoints[oldpoints.c],uvc,meshBlock.saveSubMeshes[subcount],oldpoints.c,normalc,normalf,phoneAngle,usePhongAngle,isEdgeBreakC,animations,subcount)
                    if str(faceStyle)=="quad":
                        buildSharedPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,allOldPoints[oldpoints.d],uvd,meshBlock.saveSubMeshes[subcount],oldpoints.d,normald,normalf,phoneAngle,usePhongAngle,isEdgeBreakD,animations,subcount)
                
                if usePhong==False: # if phongshading should not be considered, execute the "buildPoint()" for each of the points of the polygon
                    buildPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.a],oldpoints.a,uva,None,animations,subcount)
                    buildPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.b],oldpoints.b,uvb,None,animations,subcount)
                    buildPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.c],oldpoints.c,uvc,None,animations,subcount)
                    if str(faceStyle)=="quad":
                        buildPoint(exportData,faceStyle,meshBlock,meshBlock.sceneObject,meshBlock.saveSubMeshes[subcount],allOldPoints[oldpoints.d],oldpoints.d,uvd)
                foundSelection=True# set this to true, so we now a polygon was set to a submesh    
                break
            subcount+=1
        if foundSelection==False: # if the polygon was not set to a submesh:
            allFoundSelection+=1 # we count the "error-polgons for the mesh, so we do not raise a error for each polgon, but only inform the user how many polygons hasnt been exported proper 
    if allFoundSelection>0:
        print "Error: Not all Polygons were put into Submeshes !!!! This should never happen!!! Please contact 80prozent@differentdesign.de"
    exportData.subStatus=0
    

# checks if a submesh reached its ressource-limits - returns the index of the Submesh to use - if the submesh has its limits reached, the index of the new Submesh is returned
def checkForRessourceLimits(exportData,meshBlock,subcount,faceIndex,faceStyle,curSubMesh,animations):
    multiplyForFace=3      # if this polygon is a triangle, we will add at max three new item to all the lists   
    ressourceLimit=65535    # the max ressource limit for one list
    if str(faceStyle)=="quad":  # if this polygon is a rectangle: 
        multiplyForFace=6   # six values will be added to the list add maximum
    returnSubCnt=subcount   # set the returnSubcount
    getSubCount=exportData.useInsteadSubMeshDic.get(str(subcount),None) # check if this Submesh-Index is allready translated to a new Submesh
    if getSubCount is not None: # if the Submesh is allready translated: 
        curSubMesh=meshBlock.saveSubMeshes[getSubCount] # set the curSubMesh to be the subMehs, the translation points to
        returnSubCnt=getSubCount # set the reutrnIndex to be the translated Index 
    limitExceed=False # set LimitsExceed to false - if this is true later, the limit has been reached
    if (len(curSubMesh.vertexBuffer)+(multiplyForFace))>=ressourceLimit:    # check the verticles-list for reaching its limits
        limitExceed=True
    if (len(curSubMesh.indexBuffer)+(multiplyForFace))>=ressourceLimit:     # check the verticles-list for reaching its limits
        limitExceed=True
    if ((len(curSubMesh.quadBuffer)*(6/4))+(multiplyForFace))>=ressourceLimit:     # check the verticles-list for reaching its limits
        limitExceed=True
    if limitExceed==True: # if any limit has been reached
        #print "LIMITREACHED"
        newSubMesh=classesAWDBlocks.awdSubMesh(curSubMesh.materialName,curSubMesh.selectionName,[],curSubMesh.textureTag)# create a new Submesh with empty selection and the material and textureTag from its origin
        #TO DO: expand the animations #for anim in animations:
            #newPointsList=[]
            #anim.frameSubMeshStreams.append(newPointsList)
        
        for instanceBlock in meshBlock.sceneBlocks: # for each instance that uses this Geiometry we need to append one more Material for this new subgeometry
            instanceBlock.saveMaterials.append(instanceBlock.saveMaterials[subcount])
        exportData.useInsteadSubMeshDic[str(subcount)]=len(meshBlock.saveSubMeshes) # make a item in the dictionary to tranlate the origional submeshes to this addional created one       
        meshBlock.saveSubMeshes.append(newSubMesh) # append the new submesh to the geometryBlock
        return (len(meshBlock.saveSubMeshes)-1) # return the index to the new Submesh, so it will be used
        
    return returnSubCnt # if this gets executed, no limit is reached and the tranlated submesh-index is returned
    
    
# this function needs to be redone, but since the current awd does not allow for all uv-depentent stuff, its tricky
def transformUVS(subMesh):
    if subMesh.textureTag is not None:
        if len(subMesh.uvBuffer)>0:
            repeat=subMesh.textureTag[c4d.TEXTURETAG_TILE]
            scaleU=subMesh.textureTag[c4d.TEXTURETAG_TILESX]
            scaleV=subMesh.textureTag[c4d.TEXTURETAG_TILESY]
            if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]>0:
                pass# raise error 
            if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]>0:
                pass# raise error
                repeat=False
                scaleU=scaleU
                scaleV=scaleV
            for uv in subMesh.uvBuffer:
                uv.x=(uv.x)-(subMesh.textureTag[c4d.TEXTURETAG_OFFSETX])
                uv.y=(uv.y)-(subMesh.textureTag[c4d.TEXTURETAG_OFFSETY])
                if subMesh.textureTag[c4d.TEXTURETAG_REPETITIONX]==0 and subMesh.textureTag[c4d.TEXTURETAG_REPETITIONY]==0:
                    tmpX=uv.x*scaleU
                    uv.y=uv.y*scaleV
						
        #print "texuretag repeat = "+str(repeat)+" scaleU = "+str(scaleU)+" scaleV = "+str(scaleV)    
        #build all the geometryStreams (the geometry-streams contain the data still as python-list, and will be parsed into binary



# create the final AWD-GeometryStream-Objects for one SubMeshBlock. 
def buildGeometryStreams(subMesh,scale,animations, subMeshNr):

    for anim in animations:
        frameCnt=0
        while frameCnt<len(anim.frameSubMeshStreams):
            pointData=[]
            for point in anim.frameSubMeshStreams[frameCnt][subMeshNr]:
                pointData.append(point.x*scale)
                pointData.append(point.y*scale)
                pointData.append(point.z*scale)
            anim.saveFrameSubMeshStreams[frameCnt][subMeshNr].append(classesAWDBlocks.awdGeometryStream(1,pointData))
            frameCnt+=1
                
        
    # create the final AWD-GeometryStream-Object for Point-Data (type=1)
    if len(subMesh.vertexBuffer)>0:
        pointData=[]
        for point in subMesh.vertexBuffer:
            pointData.append(point.x*scale)
            pointData.append(point.y*scale)
            pointData.append(point.z*scale)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(1,pointData))
        
    # create the final AWD-GeometryStream-Object for Normal-Data (type=4)
    if len(subMesh.normalBuffer)>0:
        normalData=[]
        for point in subMesh.normalBuffer:
            normalData.append(point.x)
            normalData.append(point.y)
            normalData.append(point.z)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(4,normalData))
        
    # create the final AWD-GeometryStream-Object for Quad-Index-Data (type=8) - NOT USED BY OFFICIAL AWD2
    if len(subMesh.quadBuffer)>0:
        quadData=[]
        indexCnt=0
        while indexCnt<len(subMesh.quadBuffer):
            indexA=(subMesh.quadBuffer[indexCnt])
            indexCnt+=1
            quadData.append(indexA)
            quadData.append(subMesh.quadBuffer[indexCnt])
            indexCnt+=1
            indexC=(subMesh.quadBuffer[indexCnt])
            indexCnt+=1
            quadData.append(indexC)
            quadData.append(indexA)
            quadData.append(indexC)
            quadData.append(subMesh.quadBuffer[indexCnt])
            indexCnt+=1
        for indexPoint in subMesh.indexBuffer:
            quadData.append(indexPoint)
           
        subMesh.indexBuffer=quadData
        #for indexPoint in subMesh.quadBuffer:
            #quadData.append(indexPoint)
        #subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(8,quadData))
        
    # create the final AWD-GeometryStream-Object for Index-Data (type=2)
    if len(subMesh.indexBuffer)>0:
        indexData=[]
        for indexPoint in subMesh.indexBuffer:
            indexData.append(indexPoint)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(2,indexData))
        
    # create the final AWD-GeometryStream-Object for UV-Data (type=3)
    if len(subMesh.uvBuffer)>0:
        uvData=[]
        for uv in subMesh.uvBuffer:
            uvData.append(uv.x)
            uvData.append(uv.y)
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(3,uvData))
        
    # prepare Weight-Data and JointIndex-Data for the final AWD.GeometryStream-Object:
    if len(subMesh.weightsBuffer)>0 and len(subMesh.jointidxBuffer)>0:
        
        # Get the Maximum number of Joints used on one point, and create some lists to store the new weight data:        
        maxJoints=0                     # this will hold the maximum of joints per point, e.g. the length of weights-lists and jointIndex-lists
        subMesh.saveWeightsBuffer=[]    # this will hold a new list of weight for each point of the submesh
        subMesh.saveIndexBuffer=[]      # this will hold a new list of joindIndicies for each point of the submesh
        for weights in subMesh.weightsBuffer:       # for each weightList (same as "for each point of submesh")
            subMesh.saveWeightsBuffer.append([])        # create a new list, that will store all weights for this point later
            subMesh.saveIndexBuffer.append([])          # create a new list, that will store all JointIndicies for this point later
            if len(weights)>maxJoints:                  # if the length of this weight-list is bigger than a previous processed weight-list:
                maxJoints=len(weights)                      # set maxJoints to the length of this weight-list
                
        jointCount=0                                
        while jointCount<maxJoints:                         # do for 0-maxJoints
            bufferCount=0
            while bufferCount<len(subMesh.weightsBuffer):       # do for every list of weights:
                newWeight=float(0.0)
                newIndex=1
                biggestWeight=float(0.0)
                curweightcount=-1
                weightcount=0
                while weightcount<len(subMesh.weightsBuffer[bufferCount]):              # find the biggest weight of the old-weight-list
                    if subMesh.weightsBuffer[bufferCount][weightcount]>=biggestWeight:      # and store it to biggestWeight and curweightcount (weight + jointIndex)
                        biggestWeight=float(subMesh.weightsBuffer[bufferCount][weightcount])
                        curweightcount=weightcount
                    weightcount+=1
                    
                if curweightcount>=0:                                                   # if the curweightcount was set (another weight/joint was found for this list)
                    newIndex=subMesh.jointidxBuffer[bufferCount][curweightcount]            # get the "real" Index of the JointIndex
                    subMesh.weightsBuffer[bufferCount].pop(curweightcount)                  # delete the newly found weight from the old weight-list
                    subMesh.jointidxBuffer[bufferCount].pop(curweightcount)                 # delete the newly found joindindex from the old joindindex-list
                    
                subMesh.saveIndexBuffer[bufferCount].append(newIndex)                   # save the new JointIndex to the new JointIndex-list
                subMesh.saveWeightsBuffer[bufferCount].append(biggestWeight)            # save the new JointIndex to the new JointIndex-list
                bufferCount+=1
            jointCount+=1
            
        bufferCount=0
        while bufferCount<len(subMesh.weightsBuffer):                           # for every weight-list do:
            jointCount=0
            allWeight=0                 # here will store the sum of all weights applied to one point, so we can check if they are == 1.0 as they should
            while jointCount<maxJoints:                                             # iterate trough list (using the maxJoints-value instead of len(weight-list)
                if float(subMesh.saveWeightsBuffer[bufferCount][jointCount])>float(1.0):        # check if this weight alone is bigger than 1.0
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=float(1.0)                    # and if so, set it back to 1
                if float(subMesh.saveWeightsBuffer[bufferCount][jointCount])<float(0.0):        # check if this weight alone is smaller than 0.0
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]=float(0.0)                    # and if so, set it back to 0.0
                allWeight+=float(subMesh.saveWeightsBuffer[bufferCount][jointCount])            # add this weight to allWeight        
                jointCount+=1
                
            if float(allWeight) == float(0.0):                                      # if the allWeight for this point is 0.0 
                subMesh.saveWeightsBuffer[bufferCount][0]=float(1.0)                    # we set the first weight in the list to 1.0
                allWeight=float(1.0)                                                    # and fix the allWeight to 1.0 so the next calculation will be skipped
            if float(allWeight) != float(1.0):                                      # if the allWeight for this point is not 1.0
                jointCount=0                                                                                
                while jointCount<maxJoints:                                             # for every weight in the list do:                          
                    subMesh.saveWeightsBuffer[bufferCount][jointCount]*=(1/allWeight)       # multiply with 1/allWeight to set the allWeight back to 1
                    jointCount+=1
            bufferCount+=1

        # build final AWD-GeometryStream-Object for JointIndicies (type=6)
        indexData=[]                                # will hold the final weight-list
        for index in subMesh.saveIndexBuffer:
            for index2 in index:
                indexData.append(index2)            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(6,indexData))

        # build final AWD-GeometryStream-Object for Weights (type=7)
        weightData=[]
        for weight in subMesh.saveWeightsBuffer:
            for weight2 in weight:
                weightData.append(weight2)            
        subMesh.saveGeometryStreams.append(classesAWDBlocks.awdGeometryStream(7,weightData))
    
