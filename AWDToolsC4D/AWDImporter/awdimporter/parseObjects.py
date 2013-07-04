import c4d
import struct
import math
import os
import copy
from c4d import documents
from c4d import modules
from awdimporter import helpers
from awdimporter import awdBlocks

def parseTriangleGeometryBlock(body,block,sceneData):

    newTriangleGeometrieBlock=awdBlocks.TriangleGeometrieBlock()

    
    name=helpers.parseVarString(body)
    subMeshCount=struct.unpack('H', body.read(2))[0]
    helpers.parseProperties(body)
    newTriangleGeometrieBlock.polygonObject = c4d.BaseObject(c4d.Opolygon) #Create an empty polygon object
    allSubMeshLength = []
    allSubMeshLengthForUV = []
    allPoints = []
    allTris = []
    allUVs = []
    allNormals = []
    newTriangleGeometrieBlock.allJointIndexe = []
    newTriangleGeometrieBlock.allJointWeights = []
    newTriangleGeometrieBlock.numJoints=[]
    newTriangleGeometrieBlock.indexDics=[]
    newTriangleGeometrieBlock.maxJointIndex=[]
    newTriangleGeometrieBlock.minJointIndex=[]
    newTriangleGeometrieBlock.SubmeshPoints=[]
    newTriangleGeometrieBlock.subMeshSelections=[]
    subMeshesParsed=0
    while subMeshesParsed<subMeshCount:
        subMeshSelection=[]
        newTriangleGeometrieBlock.subMeshSelections.append(subMeshSelection)
        subMeshesParsed+=1
    subMeshesParsed=0
    while subMeshesParsed<subMeshCount:
        subMeshesDataLength=struct.unpack('I', body.read(4))[0]
        helpers.parseProperties(body)
        subMeshTriCounter=0
        oldSubMeshLength=len(allTris)
        oldPointLength=len(allPoints)
        #print "found subMeshDataTyp tris "+str(oldSubMeshLength)
        #print "found subMeshDataTyp verts"+str(oldPointLength)
        newIndexDic={}
        newTriangleGeometrieBlock.indexDics.append(newIndexDic)
        newJointIndexe=[]
        newTriangleGeometrieBlock.allJointIndexe.append(newJointIndexe)
        newJointWeights=[]
        newTriangleGeometrieBlock.allJointWeights.append(newJointWeights)

        subMeshesBytesDone=0
        while subMeshesBytesDone<subMeshesDataLength:
            subMeshDataTyp=struct.unpack('B', body.read(1))[0]
            subMeshDataContentTyp=struct.unpack('B', body.read(1))[0]
            subMeshDataLength=struct.unpack('I', body.read(4))[0]
            subMeshDataDone=0
            #print "found subMeshDataTyp"+str(subMeshDataTyp)
            if subMeshDataTyp==1:# Vertex
                
                while subMeshDataDone<subMeshDataLength:
                    newPoint=c4d.Vector((sceneData.scale*struct.unpack('f', body.read(4))[0]),(sceneData.scale*struct.unpack('f', body.read(4))[0]),(sceneData.scale*struct.unpack('f', body.read(4))[0]))
                    allPoints.append(newPoint)
                    subMeshDataDone+=12
                    

            if subMeshDataTyp==2:# Faces
                #print "found Faces"
                while subMeshDataDone<subMeshDataLength:
                    newPoly=c4d.CPolygon((oldPointLength+struct.unpack('H', body.read(2))[0]),(oldPointLength+struct.unpack('H', body.read(2))[0]),(oldPointLength+struct.unpack('H', body.read(2))[0]))
                    allTris.append(newPoly)
                    subMeshDataDone+=6
                    subMeshCount2=0
                    while subMeshCount2<subMeshCount:
                        newTriangleGeometrieBlock.subMeshSelections[subMeshCount2].append(0)
                        subMeshCount2+=1
                    newTriangleGeometrieBlock.subMeshSelections[subMeshesParsed][len(newTriangleGeometrieBlock.subMeshSelections[subMeshesParsed])-1]=1
    
            if subMeshDataTyp==8:# FacesQuads
                #print "found quads"
                while subMeshDataDone<subMeshDataLength:
                    newPoly=c4d.CPolygon((oldPointLength+struct.unpack('H', body.read(2))[0]),(oldPointLength+struct.unpack('H', body.read(2))[0]),(oldPointLength+struct.unpack('H', body.read(2))[0]),(oldPointLength+struct.unpack('H', body.read(2))[0]))
                    allTris.append(newPoly)
                    subMeshDataDone+=8
                    subMeshCount2=0
                    while subMeshCount2<subMeshCount:
                        newTriangleGeometrieBlock.subMeshSelections[subMeshCount2].append(0)
                        subMeshCount2+=1
                    newTriangleGeometrieBlock.subMeshSelections[subMeshesParsed][len(newTriangleGeometrieBlock.subMeshSelections[subMeshesParsed])-1]=1
            if subMeshDataTyp==3:# Uvs
                while subMeshDataDone<subMeshDataLength:
                    newUV=c4d.Vector((struct.unpack('f', body.read(4))[0]),(struct.unpack('f', body.read(4))[0]),0)
                    allUVs.append(newUV)
                    subMeshDataDone+=8
    
            if subMeshDataTyp==4:# Normals
                pass
            if subMeshDataTyp==5:# Tangents
                pass
            if subMeshDataTyp==6:# Joint Index
                newTriangleGeometrieBlock.isSkinned=True
                newmaxJointIndex=0
                newminJointIndex=1000
                while subMeshDataDone<subMeshDataLength:
                    newJointIndex=struct.unpack('H', body.read(2))[0]
                    if newJointIndex>newmaxJointIndex:
                        newmaxJointIndex=newJointIndex
                    if newJointIndex<newminJointIndex:
                        newminJointIndex=newJointIndex 
                    newIndexDic[str(newJointIndex)]=0
                    newJointIndexe.append(newJointIndex)
                    subMeshDataDone+=2 
            if subMeshDataTyp==7:# Joint weight
                newTriangleGeometrieBlock.isSkinned=True
                while subMeshDataDone<subMeshDataLength:
                    newJointWeights.append(struct.unpack('f', body.read(4))[0])
                    subMeshDataDone+=4 
            if subMeshDataDone==0:# Joint weight
                body.read(subMeshDataLength)
            
            subMeshesBytesDone+=8+subMeshDataLength
        helpers.parseProperties(body)
        newTriangleGeometrieBlock.SubmeshPoints.append(len(allPoints)-oldSubMeshLength)
        allSubMeshLength.append(len(allPoints)-oldSubMeshLength)
        if newTriangleGeometrieBlock.isSkinned==True:
            newTriangleGeometrieBlock.maxJointIndex.append(newmaxJointIndex)
            newTriangleGeometrieBlock.minJointIndex.append(newminJointIndex)
            newTriangleGeometrieBlock.numJoints.append(len(newJointIndexe)/(len(allPoints)-oldPointLength))
        subMeshesParsed+=1
        
    if len(allPoints)>0:
        
        newTriangleGeometrieBlock.polygonObject.ResizeObject(len(allPoints),len(allTris))
        newUVTag=newTriangleGeometrieBlock.polygonObject.MakeVariableTag(c4d.Tuvw,len(allTris))
        newTriangleGeometrieBlock.polygonObject.SetAllPoints(allPoints)

    if len(allTris)>0:
        curPoly=0
        for tri in allTris:
            if len(allUVs)>0:
                newUVTag.SetSlow(curPoly,allUVs[tri.a],allUVs[tri.b],allUVs[tri.c],allUVs[tri.d])
            newTriangleGeometrieBlock.polygonObject.SetPolygon(curPoly,tri)
            curPoly+=1

    #print "triange4 = "+str(newTriangleGeometrieBlock)
    sceneData.geoDic[str(block.blockID)]=newTriangleGeometrieBlock
    helpers.parseProperties(body)
    if sceneData.debug==True:
        print "parsed: TriangleGeometrieBlock ID = "+str(block.blockID)+" SubMeshes = "+str(subMeshCount)+"  geodict = "+str(len(sceneData.geoDic))
    return newTriangleGeometrieBlock

def parsePrimitiveGeometryBlock(body,block,sceneData):  
    #print "parsePrimitiveGeometryBlock is not used yet" 
    newPrimitiveGeometrieBlock=awdBlocks.PrimitiveGeometrieBlock()    
    body.read(block.blockSize)
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: PrimitiveGeometrieBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newPrimitiveGeometrieBlock

def parseSceneBlock(body,block):  
    #print "parseSceneBlock is not used yet" 
    newSceneBlock=awdBlocks.SceneBlock()   
    body.read(block.blockSize)
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: SceneBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newSceneBlock

def parseContainerBlock(body,block,sceneData):    
    newContainerBlock=awdBlocks.ContainerBlock()
    parentID,newMatrix,name= helpers.parseSceneHeader(body,sceneData.scale)
    newContainer = c4d.BaseObject(c4d.Onull)
    parentBlock=sceneData.blockDic.get(str(parentID),None)
    parentObj=None
    if parentBlock!=None:
        parentObj=parentBlock.sceneObject
    prevObj=c4d.documents.GetActiveDocument().GetFirstObject()
    if prevObj:
        while prevObj.GetNext():
            prevObj=prevObj.GetNext()
        if parentObj!=None:
            prevObj=parentObj.GetDownLast()
    c4d.documents.GetActiveDocument().InsertObject(newContainer,parentObj,prevObj)
    newContainer.SetName(name)
    newContainer.SetMl(newMatrix)
    helpers.parseProperties(body)
    helpers.parseProperties(body)
    block.sceneObject=newContainer
    if parentID==0:
        sceneData.rootObjects.append(newContainer)
    if sceneData.debug==True:
        print "parsed: ContainerBlock ID = "+str(block.blockID)+" parentID = "+str(parentID)
    return newContainerBlock

def parseMeshInstanceBlock(body,block,sceneData):  
    newMeshInstanceBlock=awdBlocks.MeshInstanceBlock()   
    parentID,newMatrix,name= helpers.parseSceneHeader(body,sceneData.scale)
    
    parentBlock=sceneData.blockDic.get(str(parentID),None)
    parentObj=None
    if parentBlock!=None:
        parentObj=parentBlock.sceneObject
    meshObjectID=struct.unpack('I', body.read(4))[0]
    meshInstance=sceneData.geoDic.get(str(meshObjectID),None)
    if meshInstance==None:
        #print "No Mesh found = "+str(len(sceneData.geoDic))+"!!!"
        matlength=0
        while matlength<struct.unpack('H', body.read(2))[0]:
            struct.unpack('I', body.read(4))[0]
            matlength+=1
    if meshInstance!=None:
        newMesh= meshInstance.polygonObject.GetClone()
        meshInstance.sceneObject=newMesh
        newMesh.SetName(name)
        if meshInstance.isSkinned==True:
            sceneData.latestSkinnedMesh=meshInstance
            sceneData.latestSkinnedMeshUsed=False
        materialLength=struct.unpack('H', body.read(2))[0]
        materialIDs=[]
        materialCounter=0
        while materialCounter<materialLength:
            materialIDs.append(struct.unpack('I', body.read(4))[0])
            materialCounter+=1 
        materialCounter=materialLength-1
        while materialCounter>=0:
            material=sceneData.materialsDic.get(str(materialIDs[materialCounter]),None)
            if material!=None: 
                tag = newMesh.MakeTag(c4d.Ttexture)          # create new Texturetagc4d.TEXTURETAG_PROJECTION] newTriangleGeometrieBlock.subMeshSelections  TEXTURETAG_RESTRICTION]
                tag[c4d.TEXTURETAG_MATERIAL]=material
                tag[c4d.TEXTURETAG_PROJECTION]=6
                if materialCounter>0: 
                    selecTag = newMesh.MakeTag(c4d.Tpolygonselection)          # create new Texturetagc4d.TEXTURETAG_PROJECTION] newTriangleGeometrieBlock.subMeshSelections 
                    selecTag.SetName("PolygonSelection SubMesh "+str(materialCounter))
                    selecTag.GetBaseSelect().SetAll( meshInstance.subMeshSelections[materialCounter])      # create new Texturetagc4d.TEXTURETAG_PROJECTION] newTriangleGeometrieBlock.subMeshSelections 
                    tag[c4d.TEXTURETAG_RESTRICTION]=selecTag.GetName()

            materialCounter-=1 
        prevObj=c4d.documents.GetActiveDocument().GetFirstObject()
        if prevObj:
            while prevObj.GetNext():
                prevObj=prevObj.GetNext()
            if parentObj!=None:
                prevObj=parentObj.GetDownLast()
        c4d.documents.GetActiveDocument().InsertObject(newMesh,parentObj,prevObj)
        newMesh.SetMl(newMatrix)
        phongTag=newMesh.MakeTag(5612)
        phongTag[c4d.PHONGTAG_PHONG_ANGLELIMIT]=True
        phongTag[c4d.PHONGTAG_PHONG_ANGLE]=(90.0/180)*math.pi
        block.sceneObject=newMesh
        newMesh.Message(c4d.MSG_UPDATE)
        
    helpers.parseProperties(body)
    helpers.parseProperties(body)
    
    #if parentID==0:
    #	sceneData.rootObjects.append(newContainer)
    if sceneData.debug==True:
        print "parsed: MeshInstanceBlock ID = "+str(block.blockID)
    return newMeshInstanceBlock

def parseLightBlock(body,block,sceneData):    
    newLightBlock=awdBlocks.LightBlock()   
    body.read(block.blockSize)
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: LightBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newLightBlock
    
def parseCameraBlock(body,bytes):  
    newCameraBlock=awdBlocks.CameraBlock()    
    body.read(block.blockSize)
    if sceneData.debug==True:    
        print "skiped because parser is not implemented yet: CameraBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newCameraBlock

def parseStandartMaterialBlock(body,block,sceneData):  
    newStandartMaterialBlock=awdBlocks.StandartMaterialBlock()    
    newStandartMaterialBlock.name=helpers.parseVarString(body)  
    newStandartMaterialBlock.MatType=struct.unpack('B', body.read(1))[0]
    newStandartMaterialBlock.numShaders=struct.unpack('B', body.read(1))[0]
    newMaterial=c4d.BaseMaterial(c4d.Mmaterial)
    firstMaterial=c4d.documents.GetActiveDocument().GetFirstMaterial()
    if firstMaterial!=None:
        while firstMaterial.GetNext():
            firstMaterial=firstMaterial.GetNext()
    
    c4d.documents.GetActiveDocument().InsertMaterial(newMaterial,firstMaterial)
    newMaterial.SetName(newStandartMaterialBlock.name)
    #newMaterial[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]="shit"

    #print "MaterialName  =  "+str(newStandartMaterialBlock.name)
    #print "MaterialType  =  "+str(newStandartMaterialBlock.MatType)
    #print "Material numShaders  =  "+str(newStandartMaterialBlock.numShaders)
    length=struct.unpack('I', body.read(4))[0]
    #print "Material Attributes length (bytes)  =  "+str(length)
    
    attributecount=0
    while attributecount<length:
        attributeID = struct.unpack('H', body.read(2))[0]
        #print "Attribute ID = "+str(attributeID)
        attributeLength =  struct.unpack('I', body.read(4))[0]
        #print "Attribute Length = "+str(attributeLength)
        if attributeID==1:
            colorR=struct.unpack('B', body.read(1))[0]
            colorG=struct.unpack('B', body.read(1))[0]
            colorB=struct.unpack('B', body.read(1))[0]
            colorA=struct.unpack('B', body.read(1))[0]
            #print newMaterial[c4d.MATERIAL_COLOR_COLOR]
            newMaterial[c4d.MATERIAL_COLOR_COLOR]=c4d.Vector(float(float(colorB)/255),float(float(colorG)/255),float(float(colorR)/255))

            #print "Attribute Value  R = "+str( colorR)+"   attributeNr: "+str(attributecount)
            #print "Attribute Value G = "+str( colorG)
            #print "Attribute Value B = "+str( colorB)
            #print "Attribute Value A = "+str( colorA)
        elif  attributeID==2:
            textureID=struct.unpack('I', body.read(4))[0]
            #print "Attribute Value textureID = "+str( textureID)
        elif  attributeID==11:
            alphaBlending=struct.unpack('B', body.read(1))[0]
            #print "Attribute Value AlphaBlending = "+str( alphaBlending)
        elif  attributeID==12:
            alphaThreshold=struct.unpack('f', body.read(4))[0]
            #print "Attribute Value alphaThreshold = "+str( alphaThreshold)
        elif  attributeID==13:
            repeat=struct.unpack('B', body.read(1))[0]
            #print "Attribute Value repeat = "+str( repeat)
        else:
            pass#print "skipped conent = "+str(struct.unpack('I', body.read(4))[0])
            #print "Skipped unknown Attribute nr."+str(attributecount)+" type: "+str(attributeID)+" bytelength = "+str(attributeLength)
        attributecount += 6+attributeLength
    

    
    
    shadersDone=0
    while shadersDone< newStandartMaterialBlock.numShaders:
        shaderType=struct.unpack('H', body.read(2))[0]
        helpers.parseProperties(body)
        helpers.parseProperties(body)
        shadersDone+=1

    if newStandartMaterialBlock.MatType==2:
        textureBlock=sceneData.texDic.get(str(textureID),None)
        if textureBlock==None:
            pass#print "No TextureBlock found  "+str(textureID)
        if textureBlock!=None:
            #print "parsed: Texture applied to Material ID = "+str(textureID)
            shdr_texture = c4d.BaseList2D(c4d.Xbitmap)          #Create a bitmap shader in memory
            shdr_texture[c4d.BITMAPSHADER_FILENAME] = textureBlock.filePath #Assign the path to the texture image to your shader 
            newMaterial[c4d.MATERIAL_COLOR_SHADER]= shdr_texture        #Assign the shader to the color channel in memory only
            newMaterial.InsertShader(shdr_texture)                      #Insert the shader into the color channel
            newMaterial.Update(True, True)                              #Re-calculate the thumbnails of the material	
    helpers.parseProperties(body)
    sceneData.materialsDic[str(block.blockID)]=newMaterial
    if sceneData.debug==True:
        print "parsed: StandartMaterialBlock ID = "+str(block.blockID)
    return newStandartMaterialBlock

def parseTextureBlock(body,block,sceneData): 
    newTextureBlock=awdBlocks.TextureBlock()   
    newTextureBlock.name=helpers.parseVarString(body)   
    newTextureBlock.isEmbed=struct.unpack('B', body.read(1))[0]
    newTextureBlock.dataSize=struct.unpack('I', body.read(4))[0]
    newTextureBlock.filePath=""
    if newTextureBlock.isEmbed==0:
        texFilePath=body.read(newTextureBlock.dataSize)
        texFileName=os.path.basename(texFilePath)
        newTextureBlock.filePath=os.path.join(sceneData.texturesExternPath,texFileName)
    if newTextureBlock.isEmbed!=0:
        curPos=body.tell()
        fileExtension=".jpg"
        if struct.unpack('H', body.read(2))[0]==55551:
            fileExtension=".jpg"
        else:
            body.seek(curPos)
            if  struct.unpack('h', body.read(2))[0]==0x424D:
                fileExtension=".bmp"
            else:
                body.seek(int(curPos)+1)
                if body.read(3)=="PNG":
                    fileExtension=".png"
                else:
                    body.seek(curPos)
                    if body.read(3)=="GIF":
                        fileExtension=".gif"
        body.seek(curPos)
        newTextureBlock.data=body.read(newTextureBlock.dataSize)
        try:
            os.makedirs(sceneData.texturesEmbedPath)
        except OSError:
            pass
        newTextureBlock.filePath=os.path.join(c4d.storage.GeGetC4DPath(c4d.C4D_PATH_DESKTOP),"test.jpg")
        f = open(newTextureBlock.filePath, 'wb')
        f.write(newTextureBlock.data)
        f.close()
    
    if sceneData.debug==True:
        print "parsed: TextureBlock ID = "+str(block.blockID)+" embed = "+str(newTextureBlock.isEmbed)+" path = "+str(newTextureBlock.filePath)
    #print newTextureBlock.data
    helpers.parseProperties(body)
    helpers.parseProperties(body)
    sceneData.texDic[str(block.blockID)]=newTextureBlock
    return newTextureBlock

def parseCubeTextureBlock(body,block,sceneData):     
    newCubeTextureBlock=awdBlocks.CubeTextureBlock()  
    body.read(block.blockSize)
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: CubeTextureBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newCubeTextureBlock


def parseSkeletonBlock(body,block,sceneData):   
    newSkeletonBlock=awdBlocks.SkeletonBlock()
    newSkeletonBlock.name=helpers.parseVarString(body)
    newSkeletonBlock.numJoints=struct.unpack('H', body.read(2))[0]
    newSkeletonBlock.jointList=[]
    helpers.parseProperties(body)
    jointsDic={}
    
    doc=c4d.documents.GetActiveDocument()
    if sceneData.latestSkinnedMesh!=None and sceneData.latestSkinnedMeshUsed==False:
        doc.SetActiveObject(sceneData.latestSkinnedMesh.sceneObject,c4d.SELECTION_NEW)	
    
    parsedJoints=0 
    while parsedJoints<newSkeletonBlock.numJoints:
    
        jointID=struct.unpack('H', body.read(2))[0]
        parentJointID=struct.unpack('H', body.read(2))[0]
        #print "parent Joint = "+str(parentJointID)
        newJoint= c4d.BaseObject(c4d.Ojoint)
        if jointID==1:
            newSkeletonBlock.rootJoint=newJoint
            skeletonTag= newJoint.MakeTag(1028937)
            newJoint.SetName(newSkeletonBlock.name)
            skeletonTag[1011]=newSkeletonBlock.name
            parentOBJ=None
            beforeOBJ=None
            if sceneData.latestSkinnedMesh!=None:
                parentOBJ=sceneData.latestSkinnedMesh.sceneObject.GetUp()
                beforeOBJ=sceneData.latestSkinnedMesh.sceneObject
            if sceneData.latestSkinnedMesh==None:
                beforeOBJ=c4d.documents.GetActiveDocument().GetFirstObject()
                if beforeOBJ!=None:
                    while beforeOBJ.GetNext():
                        beforeOBJ=prevObj.GetNext()

            #print "found" +str(skeletonTag[1050])
        if jointID!=1:
            parentOBJ=jointsDic.get(str(parentJointID),None)
            beforeOBJ=None
        jointsDic[str(jointID)]=newJoint
        doc.InsertObject(newJoint,parentOBJ,beforeOBJ)
        doc.SetActiveObject(newJoint,c4d.SELECTION_ADD)	
        lookUpName=helpers.parseVarString(body)
        newJoint.SetName(lookUpName)
        normalizeMatrix=False
        if parsedJoints==0:
            normalizeMatrix=False
        jointMatrix=helpers.parseMatrix(body,sceneData.scaleJoints,normalizeMatrix,1).__invert__()
        #jointMatrix.Scale(c4d.Vector(1))
        newJoint.SetMg(jointMatrix)
    
        if jointID==1:
            newJoint.SetEditorMode(c4d.MODE_OFF)

            
        newSkeletonBlock.jointList.append(newJoint)
        #body.read(48)
        helpers.parseProperties(body)
        helpers.parseProperties(body)
        parsedJoints+=1
    helpers.parseProperties(body)
    if sceneData.latestSkinnedMesh!=None and sceneData.latestSkinnedMeshUsed==False:
        sceneData.latestSkinnedMeshUsed=True
        c4d.CallCommand(1019881) # Bind
        curPoint=0
        allPoints=sceneData.latestSkinnedMesh.sceneObject.GetAllPoints()
        weightTag=sceneData.latestSkinnedMesh.sceneObject.GetTag(1019365)
        jointCounter=0
        curSubMesh=0
        while curPoint<len(allPoints):
            for curJoint in newSkeletonBlock.jointList:
                jointIndex=weightTag.FindJoint(curJoint)
                if jointIndex!=c4d.NOTOK:
                    weightTag.SetWeight(jointIndex, curPoint, 0.0)
            curJointIdx=0
            while curJointIdx<sceneData.latestSkinnedMesh.numJoints[curSubMesh]:
                #print "test 1 = "+str(sceneData.latestSkinnedMesh.allJointIndexe[curSubMesh][jointCounter])
                #print "test 2 = "+str(sceneData.latestSkinnedMesh.allJointIndexe[curSubMesh])
                #print "test 3 = "+str(newSkeletonBlock.jointList[sceneData.latestSkinnedMesh.allJointIndexe[curSubMesh][jointCounter]-1])
                jointIndex=weightTag.FindJoint(newSkeletonBlock.jointList[sceneData.latestSkinnedMesh.allJointIndexe[curSubMesh][jointCounter]])
                weight=sceneData.latestSkinnedMesh.allJointWeights[curSubMesh][jointCounter]
                if jointIndex!=c4d.NOTOK:
                    weightTag.SetWeight(jointIndex, curPoint, weight)
                curJointIdx+=1
                jointCounter+=1
            curPoint+=1
            if curPoint>=sceneData.latestSkinnedMesh.SubmeshPoints[curSubMesh]:
                curSubMesh+=1
                jointCounter=0
    sceneData.lastSkeleton=newSkeletonBlock
    if sceneData.debug==True:
        pass#print "parsed: SkeletonBlock ID = "+str(block.blockID)+" jointNum = "+str(newSkeletonBlock.numJoints)+" applied to mesh ID = "+str(sceneData.latestSkinnedMesh)
    return newSkeletonBlock

def parseSkeletonPoseBlock(body,block,sceneData):   
    newSkeletonPoseBlock=awdBlocks.SkeletonPoseBlock()
    newSkeletonPoseBlock.name = helpers.parseVarString(body)
    newSkeletonPoseBlock.numJoints=struct.unpack('H', body.read(2))[0]
    newSkeletonPoseBlock.transformations=[]
    helpers.parseProperties(body)
    transformationsDone=0
    while transformationsDone<newSkeletonPoseBlock.numJoints:
        hasTransform=struct.unpack('B', body.read(1))[0]
        newSkeletonPoseBlock.transformations.append(hasTransform)
        if hasTransform==0:
            newSkeletonPoseBlock.transformations.append(c4d.Matrix())
        if hasTransform!=0:
            normalizeMatrix=True
            if transformationsDone==0:
                normalizeMatrix=True
            newSkeletonPoseBlock.transformations.append(helpers.parseMatrix(body,sceneData.scaleJoints,normalizeMatrix,1))
        transformationsDone+=1
    helpers.parseProperties(body)
    if sceneData.debug==True:
        print "parsed: SkeletonPoseBlock ID = "+str(block.blockID)+" jointNum = "+str(newSkeletonPoseBlock.numJoints)
    return newSkeletonPoseBlock


def parseSkeletonAnimationBlock(body,block,sceneData): 
    #print "123456"
    newSkeletonAnimationBlock=awdBlocks.SkeletonAnimationBlock()
    newSkeletonAnimationBlock.name=helpers.parseVarString(body)
    newSkeletonAnimationBlock.numFrames=struct.unpack('H', body.read(2))[0]
    helpers.parseProperties(body)
#    if newSkeletonAnimationBlock.numFrames==len(sceneData.skeletonPoses):
#	print "Animation PARSED = "+str(newSkeletonAnimationBlock.name)+" /  frames excpected = "+str(newSkeletonAnimationBlock.numFrames)+"  frames found = "+str(len(sceneData.skeletonPoses))
#      


    IDPOSX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
    IDPOSY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
    IDPOSZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_POSITION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
    IDSCALEX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_SCALE,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
    IDSCALEY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_SCALE,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
    IDSCALEZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_SCALE,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
    IDROTX=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_X,c4d.DTYPE_REAL,0))
    IDROTY=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Y,c4d.DTYPE_REAL,0))
    IDROTZ=c4d.DescID(c4d.DescLevel(c4d.ID_BASEOBJECT_ROTATION,c4d.DTYPE_VECTOR,0),c4d.DescLevel(c4d.VECTOR_Z,c4d.DTYPE_REAL,0))
    doc=c4d.documents.GetActiveDocument() 
    keyTime=doc.GetMinTime().Get()*1000
    lastDuration=0
    framesDone=0
    while framesDone<newSkeletonAnimationBlock.numFrames:
        poseID=struct.unpack('I', body.read(4))[0]
        frameDoration=struct.unpack('H', body.read(2))[0]
        poseBlock=sceneData.blockDic.get(str(poseID),None)
        newkeyTime=c4d.BaseTime((keyTime+lastDuration)/1000)
        lastDuration+=frameDoration
        if framesDone==0:
            if sceneData.lastSkeleton.hasRetargetTag!=None:
                newHirarchy=sceneData.lastSkeleton.refObject.GetClone()
                if newHirarchy.GetTag(1028937):
                    newHirarchy.GetTag(1028937).Remove()
                skeletonAnimationTag=newHirarchy.MakeTag(1028938)
                skeletonAnimationTag[1011]=newSkeletonAnimationBlock.name
                parentObj=sceneData.lastSkeleton.jointList[0].GetUp()
                prevObj=None
                if parentObj!=None:
                    prevObj=parentObj.GetDownLast()
                if parentObj==None:
                    beforeOBJ=c4d.documents.GetActiveDocument().GetFirstObject()
                    if beforeOBJ!=None:
                        while beforeOBJ.GetNext():
                            beforeOBJ=beforeOBJ.GetNext()


                doc.InsertObject(newHirarchy,parentObj,prevObj)
                newHirarchy.SetName(newSkeletonAnimationBlock.name)
                skeletonAnimationTag[1011]=newSkeletonAnimationBlock.name

            if sceneData.lastSkeleton.hasRetargetTag==None: 
                sceneData.lastSkeleton.refObject=sceneData.lastSkeleton.jointList[0].GetClone()
                newHirarchy=sceneData.lastSkeleton.refObject.GetClone()
                if newHirarchy.GetTag(1028937):
                    newHirarchy.GetTag(1028937).Remove()
                skeletonAnimationTag=newHirarchy.MakeTag(1028938)
                skeletonAnimationTag[1011]=newSkeletonAnimationBlock.name
                parentObj=sceneData.lastSkeleton.jointList[0].GetUp()
                prevObj=None
                if parentObj!=None:
                    prevObj=parentObj.GetDownLast()
                doc.InsertObject(newHirarchy,parentObj,prevObj)
                newHirarchy.SetName(newSkeletonAnimationBlock.name)
                sceneData.lastSkeleton.hasRetargetTag=sceneData.lastSkeleton.jointList[0].MakeTag(1024237)  
                sceneData.lastSkeleton.hasRetargetTag[c4d.ID_CA_POSE_HIERARCHY]=True
                sceneData.lastSkeleton.hasRetargetTag[c4d.ID_CA_POSE_P]=True
                sceneData.lastSkeleton.hasRetargetTag[c4d.ID_CA_POSE_R]=True
                sceneData.lastSkeleton.hasRetargetTag[c4d.ID_CA_POSE_R]=True
                sceneData.lastSkeleton.hasRetargetTag.AddMorph()
                sceneData.lastSkeleton.hasRetargetTag.UpdateMorphs()
                
                #hasRetargetTag2=newHirarchy.MakeTag(1024237)  
                #hasRetargetTag2[c4d.ID_CA_POSE_HIERARCHY]=True
                #hasRetargetTag2[c4d.ID_CA_POSE_P]=True
                #hasRetargetTag2[c4d.ID_CA_POSE_R]=True
                #hasRetargetTag2[c4d.ID_CA_POSE_R]=True
                #newbase=hasRetargetTag2.AddMorph()
                #hasRetargetTag2.UpdateMorphs()
                
                #newMorph=sceneData.lastSkeleton.hasRetargetTag.AddMorph()
                #newMorph.CopyFrom(newbase,None,c4d.CAMORPH_COPY_FLAGS_0)
                #newMorph.SetMode(doc, sceneData.lastSkeleton.hasRetargetTag, c4d.CAMORPH_MODE_FLAGS_EXPAND,c4d.CAMORPH_MODE_ABS)
                #sceneData.lastSkeleton.hasRetargetTag[c4d.ID_CA_POSE_TARGET]=newHirarchy
                #sceneData.lastSkeleton.hasRetargetTag.UpdateMorphs()

            
            newHirarchy.SetEditorMode(c4d.MODE_OFF)
            sceneData.latestjointList=[]
            helpers.createJointListRekursive(newHirarchy,sceneData)
            
            createTrackCounter=0
            while createTrackCounter<len(sceneData.latestjointList):
                joint =sceneData.latestjointList[createTrackCounter]
                newTrackROTX = c4d.CTrack(joint,IDROTX)
                newTrackROTY = c4d.CTrack(joint,IDROTY)
                newTrackROTZ = c4d.CTrack(joint,IDROTZ)
                joint.InsertTrackSorted(newTrackROTX)
                joint.InsertTrackSorted(newTrackROTY)
                joint.InsertTrackSorted(newTrackROTZ)
                if ((createTrackCounter==0) and  (sceneData.skeletonTrannslationsRoot==True)) or ((createTrackCounter>0) and  (sceneData.skeletonTrannslations==True)):
                    newTrackPOSX = c4d.CTrack(joint,IDPOSX)
                    newTrackPOSY = c4d.CTrack(joint,IDPOSY)
                    newTrackPOSZ = c4d.CTrack(joint,IDPOSZ)
                    joint.InsertTrackSorted(newTrackPOSX)
                    joint.InsertTrackSorted(newTrackPOSY)
                    joint.InsertTrackSorted(newTrackPOSZ)
                if ((createTrackCounter==0) and  (sceneData.skeletonScalesRoot==True)) or ((createTrackCounter>0) and  (sceneData.skeletonScales==True)):
                    newTrackSCALEX = c4d.CTrack(joint,IDSCALEX)
                    newTrackSCALEY = c4d.CTrack(joint,IDSCALEY)
                    newTrackSCALEZ = c4d.CTrack(joint,IDSCALEZ)
                    joint.InsertTrackSorted(newTrackSCALEX)
                    joint.InsertTrackSorted(newTrackSCALEY)
                    joint.InsertTrackSorted(newTrackSCALEZ)
                createTrackCounter+=1
                
        if poseBlock==None:
            pass#print "SkeletonAnimation could not find the skeletonPoseBlock nr "+str(framesDone)+" id "+str(poseID)
        if poseBlock!=None:
            if isinstance(poseBlock.blockDataObject,awdBlocks.SkeletonPoseBlock)==False: 
                pass#print "SkeletonAnimation could find the poseBlock nr "+str(framesDone)+" id "+str(poseID)+" but it is not a SkeletonPoseBlock"
            if isinstance(poseBlock.blockDataObject,awdBlocks.SkeletonPoseBlock)==True: 
                if len(sceneData.latestjointList)>poseBlock.blockDataObject.numJoints:
                    pass#print "Found more Transformation-Matrixes in the SkeletonPose "+str(poseID)+" than there are available in the Skeleton"
                if len(sceneData.latestjointList)>=poseBlock.blockDataObject.numJoints:
                    dataCount=0
                    jointCount=0
                    while dataCount<len(poseBlock.blockDataObject.transformations):
                        if poseBlock.blockDataObject.transformations[dataCount]!=0:
                            dataCount+=1
                            sceneData.latestjointList[jointCount].SetMl(poseBlock.blockDataObject.transformations[dataCount])
                            trackrotx=sceneData.latestjointList[jointCount].FindCTrack(IDROTX)
                            trackroty=sceneData.latestjointList[jointCount].FindCTrack(IDROTY)
                            trackrotz=sceneData.latestjointList[jointCount].FindCTrack(IDROTZ)

                            curverotx=trackrotx.GetCurve()
                            keysrotx=c4d.CKey()
                            trackrotx.FillKey(doc,sceneData.latestjointList[jointCount],keysrotx)
                            keysrotx.SetTime(curverotx,newkeyTime)
                            curverotx.InsertKey(keysrotx)
                            curveroty=trackroty.GetCurve()
                            keysroty=c4d.CKey()
                            trackroty.FillKey(doc,sceneData.latestjointList[jointCount],keysroty)
                            keysroty.SetTime(curveroty,newkeyTime)
                            curveroty.InsertKey(keysroty)
                            curverotz=trackrotz.GetCurve()
                            keysrotz=c4d.CKey()
                            trackrotz.FillKey(doc,sceneData.latestjointList[jointCount],keysrotz)
                            keysrotz.SetTime(curverotz,newkeyTime)
                            curverotz.InsertKey(keysrotz)

                            if ((jointCount==0) and  (sceneData.skeletonTrannslationsRoot==True)) or ((jointCount>0) and  (sceneData.skeletonTrannslations==True)):
                                trackx=sceneData.latestjointList[jointCount].FindCTrack(IDPOSX)
                                tracky=sceneData.latestjointList[jointCount].FindCTrack(IDPOSY)
                                trackz=sceneData.latestjointList[jointCount].FindCTrack(IDPOSZ)
                                
                                #print "create track"
                                curvex=trackx.GetCurve()
                                keyx=c4d.CKey()
                                trackx.FillKey(doc,sceneData.latestjointList[jointCount],keyx)
                                keyx.SetTime(curvex,newkeyTime)
                                curvex.InsertKey(keyx)
                                curvey=tracky.GetCurve()
                                keyy=c4d.CKey()
                                tracky.FillKey(doc,sceneData.latestjointList[jointCount],keyy)
                                keyy.SetTime(curvey,newkeyTime)
                                curvey.InsertKey(keyy)
                                curvez=trackz.GetCurve()
                                keyz=c4d.CKey()
                                trackz.FillKey(doc,sceneData.latestjointList[jointCount],keyz)
                                keyz.SetTime(curvez,newkeyTime)
                                curvez.InsertKey(keyz)
                                
                            if ((jointCount==0) and  (sceneData.skeletonScalesRoot==True)) or ((jointCount>0) and  (sceneData.skeletonScales==True)):
                                trackscalex=sceneData.latestjointList[jointCount].FindCTrack(IDSCALEX)
                                trackscaley=sceneData.latestjointList[jointCount].FindCTrack(IDSCALEY)
                                trackscalez=sceneData.latestjointList[jointCount].FindCTrack(IDSCALEZ)
                                curvescalex=trackscalex.GetCurve()
                                keyscalex=c4d.CKey()
                                trackscalex.FillKey(doc,sceneData.latestjointList[jointCount],keyscalex)
                                keyscalex.SetTime(curvescalex,newkeyTime)
                                curvescalex.InsertKey(keyscalex)
                                curvescaley=trackscaley.GetCurve()
                                keyscaley=c4d.CKey()
                                trackscaley.FillKey(doc,sceneData.latestjointList[jointCount],keyscaley)
                                keyscaley.SetTime(curvescaley,newkeyTime)
                                curvescaley.InsertKey(keyscaley)
                                curvescalez=trackscalez.GetCurve()
                                keyscalez=c4d.CKey()
                                trackscalez.FillKey(doc,sceneData.latestjointList[jointCount],keyscalez)
                                keyscalez.SetTime(curvescalez,newkeyTime)
                                curvescalez.InsertKey(keyscalez)
                                


                        if poseBlock.blockDataObject.transformations[dataCount]==0:
                            #print "no matrix for this joint"

                            dataCount+=1
                            
                        dataCount+=1
                        jointCount+=1
        framesDone+=1
    helpers.parseProperties(body)
    if sceneData.debug==True:
        print "parsed: SkeletonAnimationBlock ID = "+str(block.blockID)+" name = "+str(newSkeletonAnimationBlock.name)+" numFrames = "+str(newSkeletonAnimationBlock.numFrames)
    
    #sceneData.latestSkeletonAnimation=newSkeletonAnimation
    return newSkeletonAnimationBlock

def parseUVAnimationBlock(body,block,sceneData):    
    #print "parseUVAnimationBlock is not used yet"
    newUVAnimationBlock=awdBlocks.UVAnimationBlock()
    body.read(block.blockSize)
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: UVAnimationBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newUVAnimationBlock

def parseNameSpaceBlock(body,block,sceneData):  
    #print "parseNameSpaceBlock is not used yet"   
    newNameSpaceBlock=awdBlocks.NameSpaceBlock()
    body.read(block.blockSize) 
    if sceneData.debug==True:
        print "skiped because parser is not implemented yet: NameSpaceBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize)
    return newNameSpaceBlock

def parseMetaDataBlock(body,block,sceneData):  
    if sceneData.debug==True:
        print "parsed MetaDataBlock ID = "+str(block.blockID)+" size = "+str(block.blockSize) 
    newMetaDataBlock=awdBlocks.MetaDataBlock() 
    blocksparsed=0
    creationTime=0
    encoderName=""
    encoderVersion=""
    generatorName=""
    generatorVersion=""
    body.read(block.blockSize)
    if False==True:#skip for now
        metaDataLength=struct.unpack('I', body.read(4))[0]
        while blocksparsed<metaDataLength:
            attributeID=struct.unpack('H', body.read(2))[0]
            attributeLength=struct.unpack('I', body.read(4))[0]
            blocksparsed+=6
            if attributeID==1:
                creationTime=struct.unpack('I', body.read(4))[0]
                blocksparsed+=attributeLength
            if attributeID==2:
                str(body.read(2))
                encoderName=str(body.read(attributeLength))
                blocksparsed+=attributeLength+2
            if attributeID==3:
                str(body.read(2))
                encoderVersion=str(body.read(attributeLength))
                blocksparsed+=attributeLength+2
            if attributeID==4:
                str(body.read(2))
                generatorName=str(body.read(attributeLength))
                blocksparsed+=attributeLength+2
            if attributeID==5:
                str(body.read(2))
                generatorVersion=str(body.read(attributeLength))
                blocksparsed+=attributeLength+2
    
        if blocksparsed!=(block.blockSize-4):
            str((body.read((block.blockSize-4)-blocksparsed)))
    if sceneData.debug==True:
        print "finished MetaDataBlock = creationTime: "+str(creationTime)+" / encoderName = "+str(encoderName)+" / encoderVersion = "+str(encoderVersion)+" / generatorName = "+str(generatorVersion)+" / generatorVersion = "+str(generatorVersion)
    return newMetaDataBlock
