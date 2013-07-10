# different classes for different types of awd-blocks, all inheriting from the "BaseBlock"-class
# these classes are used for storing awd-block-data
# a BaseBlock-Class has a function called "writeBinary" wich will wirte out the binary Data of a Block.
# the "writeBinary" functions are all called by "workerHelpers.py function exportAllData"

import c4d
import struct



class BaseBlock(object):# baseclass for all blocks - not to be instanced directly
    def __init__(self,blockID=0,nameSpace=0,blockType=0):
        self.blockID = blockID
        self.saveBlockID = 0
        self.name = ""
        self.nameSpace = nameSpace
        self.blockType = blockType
        self.blockFlags= 0
        self.blockSize= 0
        self.isSkinned=False
        self.saveColorTextureID= -1
        self.tagForExport = False # part of a workarround
        self.isReordered = False
        self.objectSettings= 0

    def writeBinary(self,exportData):
        outputBits=struct.pack("< I",self.saveBlockID)
        outputBits+=struct.pack("< B",self.nameSpace)
        outputBits+=struct.pack("< B",self.blockType)
        outputBits+=struct.pack("< B",self.blockFlags)
        if exportData.debug==True:
            print "Exported Block:     BlockID= "+str(self.saveBlockID)+" NameSpcae= "+str(self.nameSpace)+" blockType= "+str(self.blockType) 
        return outputBits

class WrapperBlock(object):# baseclass for sceneObjects - not to be instanced directly 
    
    def __init__(self,targetObject=None,name="",blockType=0):
        self.targetObject=targetObject
        self.blockType=blockType
        self.name=name
        self.tagForExport=False
        self.isReordered=False
        self.saveBlockID=0
        
        self.data=None

    def writeBinary(self,exportData):# this needs to be removed as soon as all refactor is done
        baseBlockBytes=""#this should never get excecuted
        return baseBlockBytes



class BaseSceneContainerBlock(BaseBlock):# baseclass for sceneObjects - not to be instanced directly 
    
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None,blockType=0):
        super(BaseSceneContainerBlock, self ).__init__(blockID,nameSpace,blockType)
        self.sceneObject=sceneObject
        self.dataParentBlockID=0
        self.dataMatrix=c4d.Matrix()

    def writeBinary(self,exportData):
        baseBlockBytes=super(BaseSceneContainerBlock, self).writeBinary(exportData)
        outputBits=struct.pack("< I",self.dataParentBlockID)
        outputBits+=struct.pack("< f",self.dataMatrix.v1.x)+struct.pack("< f",self.dataMatrix.v1.y)+struct.pack("< f",self.dataMatrix.v1.z)
        outputBits+=struct.pack("< f",self.dataMatrix.v2.x)+struct.pack("< f",self.dataMatrix.v2.y)+struct.pack("< f",self.dataMatrix.v2.z)
        outputBits+=struct.pack("< f",self.dataMatrix.v3.x)+struct.pack("< f",self.dataMatrix.v3.y)+struct.pack("< f",self.dataMatrix.v3.z)
        outputBits+=struct.pack("< f",self.dataMatrix.off.x*exportData.scale)+struct.pack("< f",self.dataMatrix.off.y*exportData.scale)+struct.pack("< f",self.dataMatrix.off.z*exportData.scale)
        outputBits+=struct.pack("< H",len (self.name))+str(self.name)
        if exportData.debug==True:
            print "ParentBlockID= "+str(self.dataParentBlockID)
        return baseBlockBytes, outputBits

class TriangleGeometrieBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(TriangleGeometrieBlock, self ).__init__(blockID,nameSpace,1)
        self.sceneObject=sceneObject
        self.sceneBlocks=[]
        self.isSkinned=False
        self.polygonObjects = []
        self.allJointIndexe = []
        self.allJointWeights = []
        self.numJoints = []
        self.indexDics = []
        self.maxJointIndex = []
        self.jointTranslater = []
        self.minJointIndex = []
        self.SubmeshPointCount = []
        self.SubmeshTrisCount = []
        self.pointsUsed = []
        self.pointsUsed = []
        self.weightTag=None
        self.poseAnimationBlocks=[]

        self.name = "testName"
        self.saveGeometryProps = []
        self.saveSubMeshes = []
        self.saveUserAttributes = []

    def writeBinary(self,exportData):
        baseBlockBytes=super(TriangleGeometrieBlock, self).writeBinary(exportData)
        triangleGeometrieBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
        triangleGeometrieBlockBytes+=struct.pack("< H",len(self.saveSubMeshes))
        triangleGeometrieBlockBytes+=struct.pack("< I",len(self.saveGeometryProps))
        if exportData.debug==True:
            print "SubMeshes Length = "+str(len(self.saveSubMeshes))
        subMeshCount=0
        while subMeshCount<len(self.saveSubMeshes):
            subMeshBlockBytes=self.saveSubMeshes[subMeshCount].writeBinary(exportData)
            triangleGeometrieBlockBytes+=struct.pack("< I",int(len(subMeshBlockBytes)-8))+subMeshBlockBytes
            subMeshCount+=1
        triangleGeometrieBlockBytes+=struct.pack("< I",len(self.saveUserAttributes))
        return baseBlockBytes+struct.pack("< I",len(triangleGeometrieBlockBytes))+triangleGeometrieBlockBytes



class PrimitiveGeometrieBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(PrimitiveGeometrieBlock, self ).__init__(blockID,nameSpace,11)
        self.sceneObject=sceneObject
        self.sceneBlocks=[]
        self.name="lookupName"
        self.wireStyle=0
        self.primType = 0
        self.primitiveProps = []
        self.saveUserAttributes = []
        self.primitiveValues = []
        self.baseMat = None
        self.colorStyle =False
        self.hasMats=False
        

    def writeBinary(self,exportData):
        baseBlockBytes=super(PrimitiveGeometrieBlock, self).writeBinary(exportData)
        primitiveGeometrieBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
        primitiveGeometrieBlockBytes+=struct.pack("< B",self.primType)
        
        
        primitiveAttributesBytes=str()
        propCnt=0
        for primitiveProperty in self.primitiveProps:
            if primitiveProperty>100 and primitiveProperty<=200:
                primitiveAttributesBytes+=struct.pack("< H",primitiveProperty)
                primitiveAttributesBytes+=struct.pack("< I",4)
                primitiveAttributesBytes+=struct.pack("< f",float(self.primitiveValues[propCnt]))
            if primitiveProperty>300 and primitiveProperty<=400:
                primitiveAttributesBytes+=struct.pack("< H",primitiveProperty)
                primitiveAttributesBytes+=struct.pack("< I",2)
                primitiveAttributesBytes+=struct.pack("< H",int(self.primitiveValues[propCnt]))
            if primitiveProperty>700 and primitiveProperty<=800:
                primitiveAttributesBytes+=struct.pack("< H",primitiveProperty)
                primitiveAttributesBytes+=struct.pack("< I",1)
                primitiveAttributesBytes+=struct.pack("< B",self.primitiveValues[propCnt])
            propCnt+=1
        
        primitiveGeometrieBlockBytes+=struct.pack("< I",len(primitiveAttributesBytes))+primitiveAttributesBytes
        
        print "primitiveProperties-length = "+str(len(primitiveAttributesBytes))
        primitiveGeometrieBlockBytes+=struct.pack("< I",len(self.saveUserAttributes))
        return baseBlockBytes+struct.pack("< I",len(primitiveGeometrieBlockBytes))+primitiveGeometrieBlockBytes

        

class LightPickerBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0,lightList=[]):
        super(LightPickerBlock, self ).__init__(blockID,nameSpace,51)
        self.lightList=lightList
        self.saveLightList=[]
        self.name="LightPicker_"
        

    def writeBinary(self,exportData):
        baseBlockBytes=super(LightPickerBlock, self).writeBinary(exportData)
        lightPickBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
        lightPickBlockBytes+=struct.pack("< H",len(self.saveLightList))
        for light in self.saveLightList:
            lightPickBlockBytes+=struct.pack("< I",light)
            
        lightPickBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(lightPickBlockBytes))+lightPickBlockBytes


class ContainerBlock(BaseSceneContainerBlock):
    
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(ContainerBlock, self ).__init__(blockID,nameSpace,sceneObject,22)

    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(ContainerBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes
    
class MeshInstanceBlock(BaseSceneContainerBlock):
    def __init__(self,blockID=0,nameSpace=0,geoBlockID=None,sceneObject=None):
        super(MeshInstanceBlock, self ).__init__(blockID,nameSpace,sceneObject,23)
        self.geoBlockID=geoBlockID
        self.saveGeoBlockID=0
        self.geoObj=None
        self.lightPickerIdx=None
        self.saveMaterials=[]
        self.saveMaterials2=[]
        self.usedSkeleton=None
        self.poseAnimationBlocks=[]
        self.isRenderInstance=False#if this is true, the meshInstance in c4d is a instanceObject set to be a renderInstance e.g. uses same displaymaterials as reference
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(MeshInstanceBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< I",self.saveGeoBlockID)
        if exportData.debug==True:
            print "MeshInstance GeometryID = "+str(self.saveGeoBlockID)+" Materials = "+str(self.saveMaterials2)
        sceneBlockBytes+=struct.pack("< H",len(self.saveMaterials2))
        for mat in self.saveMaterials2:
            sceneBlockBytes+=struct.pack("< I",int(mat))
        
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

class LightBlock(BaseSceneContainerBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None,lightType=None):
        super(LightBlock, self ).__init__(blockID,nameSpace,sceneObject,41)
        self.name = "undefined"
        self.lightType = lightType
        self.lightProps = []
        self.nearRadius = 0.0
        self.farRadius = 0.0
        self.color = []
        self.specIntestity = 0.0
        self.diffuseIntensity = 0.0
        self.castShadows = False
        self.directionVec=None
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(LightBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< B",self.lightType)
        lightAttributesBytes=str()
        for lightProperty in self.lightProps:
            if lightProperty==1:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.nearRadius))
            if lightProperty==2:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.farRadius))
            if lightProperty==3 or lightProperty==7:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< B",int(self.color[0]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[1]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[2]))
                lightAttributesBytes+=struct.pack("< B",int(self.color[3]))
            if lightProperty==4:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.specIntestity))
            if lightProperty==5:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.diffuseIntensity))
            if lightProperty==8:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",float(self.ambientIntensity))     
            if lightProperty==10:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",1)
                lightAttributesBytes+=struct.pack("< B",self.castShadows)   
            if lightProperty==21:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",self.directionVec.x)
            if lightProperty==22:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",self.directionVec.y)
            if lightProperty==23:
                lightAttributesBytes+=struct.pack("< H",lightProperty)
                lightAttributesBytes+=struct.pack("< I",4)
                lightAttributesBytes+=struct.pack("< f",self.directionVec.z)

        sceneBlockBytes+=struct.pack("< I",len(lightAttributesBytes))+str(lightAttributesBytes)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

      
        
class CameraBlock(BaseSceneContainerBlock):
    def __init__(self,blockID=0,nameSpace=0,sceneObject=None):
        super(CameraBlock, self ).__init__(blockID,nameSpace,sceneObject,42)
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes,sceneBlockBytes=super(CameraBlock, self).writeBinary(exportData)
        sceneBlockBytes+=struct.pack("< B",False)
        sceneBlockBytes+=struct.pack("< H",1)#length of lenses (for now always 1
        sceneBlockBytes+=struct.pack("< H",5001)
        lensBytes=str()
        lensBytes+=struct.pack("< H",101)
        lensBytes+=struct.pack("< I",4)
        lensBytes+=struct.pack("< f",self.lensFOV)
        sceneBlockBytes+=struct.pack("< I",len(lensBytes))+str(lensBytes)
        sceneBlockBytes+=struct.pack("< I",0)
        sceneBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(sceneBlockBytes))+sceneBlockBytes

class StandartMaterialBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,colorMat=False):
        super(StandartMaterialBlock, self ).__init__(blockID,nameSpace,81)
        self.lookUpName = None
        self.matType = 0
        self.numShadingMethods = 0
        self.materialProperties = None
        self.mat = None
        self.shaderMethods = []
        self.userAttributes = None
        self.colorMat = colorMat
        self.isCreated = False
        self.textureTags = []
        self.lightPicker = 0
        self.materialsList = []
        self.repeat = False

        self.name = ""
        self.saveMatType = 1
        self.saveShaders = []
        self.saveMatProps = []
        self.saveMatAtts = []
                
        self.colorTextureID = None
        self.normalTextureID = None
        self.matColor = []
        
        self.matColor = None#1
        self.saveColorTextureID = 0#2
        self.saveNormalTextureID = 0#3
        self.spezialID = None#4
        self.smooth = None#5
        self.mipmap = None#6
        self.bothSides = None#7
        self.permultiplied = None#8
        self.blendMode = None#9
        self.matAlpha = 1.0 #10
        self.alphaBlending = None #11
        self.binaryAlphaTresh = None #12
        self.repeat = None #13
        self.ambientLevel = None #15
        self.ambientColor = None #16
        self.saveAmbientTextureID = 0 #17
        self.specularLevel = None #18
        self.specularGloss = None #19
        self.specularColor = None # 20
        self.saveSpecTextureID = 0 #21
        self.lightPickerID = None
        #lightPickerID#[]###[]####

    def writeBinary(self,exportData):
        baseBlockBytes=super(StandartMaterialBlock, self).writeBinary(exportData)
        materialBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
        materialBlockBytes+=struct.pack("< B",self.saveMatType)
        materialBlockBytes+=struct.pack("< B",len(self.saveShaders))
        materialBAttributesBytes=str()
        if exportData.debug==True:
            #pass#print "Material Color = "+str(int(self.matColor[0]))+" / "+str(int(self.matColor[1]))+" / "+str(int(self.matColor[2]))+" / "+str(int(self.matColor[3]))
            print "Material matAlpha = "+str((self.matAlpha))
        for matProperty in self.saveMatProps:
            if matProperty==1:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[0]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[1]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[2]))
                materialBAttributesBytes+=struct.pack("< B",int(self.matColor[3]))
            if matProperty==2:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.saveColorTextureID))
            if matProperty==3:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.saveNormalTextureID))
            if matProperty==4:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.spezialID))
            if matProperty==5:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.smooth))
            if matProperty==6:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.mipmap))
            if matProperty==7:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.bothSides))
            if matProperty==8:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.permultiplied))
            if matProperty==9:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.blendMode))
            if matProperty==10:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",self.matAlpha)
            if matProperty==11:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",int(self.alphaBlending))
            if matProperty==12:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",float(self.binaryAlphaTresh))
            if matProperty==13:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",1)
                materialBAttributesBytes+=struct.pack("< B",float(self.repeat))
            #if matProperty==14: is not used atm
            if matProperty==15:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",float(self.ambientLevel))
            if matProperty==16:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< B",int(self.ambientColor[0]))
                materialBAttributesBytes+=struct.pack("< B",int(self.ambientColor[1]))
                materialBAttributesBytes+=struct.pack("< B",int(self.ambientColor[2]))
                materialBAttributesBytes+=struct.pack("< B",int(self.ambientColor[3]))
            if matProperty==17:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.saveAmbientTextureID))
            if matProperty==18:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",float(self.specularLevel))
            if matProperty==19:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< f",float(self.specularGloss))
            if matProperty==20:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< B",int(self.specularColor[0]))
                materialBAttributesBytes+=struct.pack("< B",int(self.specularColor[1]))
                materialBAttributesBytes+=struct.pack("< B",int(self.specularColor[2]))
                materialBAttributesBytes+=struct.pack("< B",int(self.specularColor[3]))
            if matProperty==21:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.saveSpecTextureID))
            if matProperty==22:
                materialBAttributesBytes+=struct.pack("< H",matProperty)
                materialBAttributesBytes+=struct.pack("< I",4)
                materialBAttributesBytes+=struct.pack("< I",int(self.lightPickerID))

        materialBlockBytes+=struct.pack("< I",len(materialBAttributesBytes))+str(materialBAttributesBytes)
        materialBlockBytes+=struct.pack("< I",len(self.saveMatAtts))
        return baseBlockBytes+struct.pack("< I",len(materialBlockBytes))+materialBlockBytes

class TextureBlock(BaseBlock):

    def __init__(self,blockID=None,nameSpace=None,c4dfilePath=None,saveIsEmbed=0,saveFileName=None):
        super(TextureBlock, self ).__init__(blockID,nameSpace,82)
        self.c4dfilePath = c4dfilePath
        if saveIsEmbed==0:
            self.saveIsEmbed = 1
        if saveIsEmbed==1:
            self.saveIsEmbed = 0        
        self.saveFileName = saveFileName
        self.saveTextureProps=[]
        self.saveTextureAtts=[]
        self.saveTextureData=None
        
    def writeBinary(self,exportData):
        baseBlockBytes=super(TextureBlock, self).writeBinary(exportData)
        textureBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
        textureBlockBytes+=struct.pack("< B",self.saveIsEmbed)
        if self.saveIsEmbed==0:
            textureData=str(self.saveFileName)
            textureBlockBytes+=struct.pack("< I",len(textureData))+textureData
        if self.saveIsEmbed==1 or self.saveIsEmbed==2:
            textureBlockBytes+=struct.pack("< I",len(self.saveTextureData))+self.saveTextureData
        textureBlockBytes+=struct.pack("< I",len(self.saveTextureProps))
        textureBlockBytes+=struct.pack("< I",len(self.saveTextureAtts))
        return baseBlockBytes+struct.pack("< I",int(len(textureBlockBytes)))+textureBlockBytes

class CubeTextureBlock(BaseBlock):
    def __init__(self):
        self.isSkinned=False
        self.polygonObject = None
        self.sceneObject = None
    def writeBinary(self,exportData):
        baseBlockBytes=super(CubeTextureBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)

class jointBlock(object):
    def __init__(self,jointID,parentID,jointObj):
        self.jointID=jointID
        self.parentID = parentID
        self.jointObj = jointObj
        self.transMatrix = c4d.Matrix()
        self.lookUpName = "None"

#VertexAnimation

class AnimatorBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,animSetBlock=None,targetMeshBlock=None,name=""):
        super(AnimatorBlock, self ).__init__(blockID,nameSpace,122)
        self.animSetBlock = animSetBlock
        self.targetMeshBlock = targetMeshBlock
        self.skeleton = None
        self.name=name
        self.savePoseBlockIDs=[]
        self.animatorTyp=2
        self.saveMeshID=0
        self.saveSkeletonID=None
        self.saveAnimSetID=0
        
    def writeBinary(self,exportData):
        baseBlockBytes=super(AnimatorBlock, self).writeBinary(exportData)
        animatorBlockBytes=struct.pack("< H",len(self.name))+str(self.name)
            
        animatorBlockBytes+=struct.pack("< H",self.animatorTyp)
        animatorBlockBlockAttributesBytes=str()  
        print "self.saveSkeletonID! = "+str(self.saveSkeletonID)
        if self.saveSkeletonID!=None:
            animatorBlockBlockAttributesBytes+=struct.pack("< H",1)
            animatorBlockBlockAttributesBytes+=struct.pack("< I",4)
            animatorBlockBlockAttributesBytes+=struct.pack("< I",self.saveSkeletonID)
        animatorBlockBytes+=struct.pack("< I",len(animatorBlockBlockAttributesBytes))+str(animatorBlockBlockAttributesBytes)
                     
        animatorBlockBytes+=struct.pack("< I",self.saveAnimSetID)# Active State as Index         
        animatorBlockBytes+=struct.pack("< H",1)# Active State as Index 
        animatorBlockBytes+=struct.pack("< I",self.saveMeshID)# Active State as Index 
        animatorBlockBytes+=struct.pack("< H",0)# Active State as Index 
        animatorBlockBytes+=struct.pack("< B",False)# Autoplay
        animatorBlockBytes+=struct.pack("< I",0)# attributes empty
        animatorBlockBytes+=struct.pack("< I",0)# attributes empty
        return baseBlockBytes+struct.pack("< I",len(animatorBlockBytes))+animatorBlockBytes
        
class AnimationSetBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,targetMeshBlock=None,name=None):
        super(AnimationSetBlock, self ).__init__(blockID,nameSpace,113)
        self.targetMesh = targetMeshBlock
        self.saveName = name
        self.poseBlockIDs=[]
        self.savePoseBlockIDs=[]
        self.jointsPerVert=4
        
    def writeBinary(self,exportData):
        baseBlockBytes=super(AnimationSetBlock, self).writeBinary(exportData)
        vertexAnimSetBlockBytes=struct.pack("< H",len(self.saveName))+str(self.saveName)
        print ("sdnksj = "+str(len(self.savePoseBlockIDs)))
        vertexAnimSetBlockBytes+=struct.pack("< H",len(self.savePoseBlockIDs))
        vertexAnimSetBlockAttributesBytes=str()   
        if self.jointsPerVert!=4:
            vertexAnimSetBlockAttributesBytes+=struct.pack("< H",1)
            vertexAnimSetBlockAttributesBytes+=struct.pack("< I",2)
            vertexAnimSetBlockAttributesBytes+=struct.pack("< H",self.jointsPerVert)
        vertexAnimSetBlockBytes+=struct.pack("< I",len(vertexAnimSetBlockAttributesBytes))+str(vertexAnimSetBlockAttributesBytes)
        print "AnimationNodes in Set = "+str(self.savePoseBlockIDs)             
        poseBlockCount=0     
        while poseBlockCount<len(self.savePoseBlockIDs):
            vertexAnimSetBlockBytes+=struct.pack("< I",self.savePoseBlockIDs[poseBlockCount])
            if exportData.debug==True:
                print "saved AnimationID in AnimationSET = "+str(self.savePoseBlockIDs[poseBlockCount])
            poseBlockCount+=1
        
        vertexAnimSetBlockBytes+=struct.pack("< I",0)# attributes empty
        return baseBlockBytes+struct.pack("< I",len(vertexAnimSetBlockBytes))+vertexAnimSetBlockBytes

class MeshPoseBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,meshPoseName=None):
        super(MeshPoseBlock, self ).__init__(blockID,nameSpace,111)
        self.meshPoseName = meshPoseName
        self.targetMesh = None
        self.subMeshStreams = []
        self.points=[]
        self.duration=[]
        self.streams=[] 
        self.savePoseProps=[]
        self.saveTargetMesh=None
        
    def writeBinary(self,exportData):
        baseBlockBytes=super(MeshPoseBlock, self).writeBinary(exportData)
        meshPoseBlockBytes=struct.pack("< H",len(self.meshPoseName))+str(self.meshPoseName)
        meshPoseBlockBytes+=struct.pack("< I",self.saveTargetMesh) # number of frames
        meshPoseBlockBytes+=struct.pack("< H",len(self.subMeshStreams))
        meshPoseBlockBytes+=struct.pack("< H",1) # number of streams
        meshPoseBlockBytes+=struct.pack("< H",1) # types of streams (can be a list later)
            
        meshPoseBlockAttributesBytes=str()
        for poseProperty in self.savePoseProps:
            if poseProperty==1:#a single meshpose needs no loop or stitchfinalframe
                pass
        meshPoseBlockBytes+=struct.pack("< I",len(meshPoseBlockAttributesBytes))+str(meshPoseBlockAttributesBytes)
            
        subMeshCount=0     
        while subMeshCount<len(self.subMeshStreams):    
            streamCnt=0     
            while streamCnt<len(self.subMeshStreams[subMeshCount]):   # this should be 1 iteration for now (only vertexPositionData)   
                streamDataBits=str()
                streamCounter=0
                while streamCounter< len(self.subMeshStreams[subMeshCount][streamCnt].streamData):
                    streamDataBits+=struct.pack(str("< "+str(self.subMeshStreams[subMeshCount][streamCnt].dataType)),self.subMeshStreams[subMeshCount][subMeshCount].streamData[streamCounter])
                    streamCounter+=1
                meshPoseBlockBytes+=struct.pack("< I",len(streamDataBits))+streamDataBits
                streamCnt+=1
            subMeshCount+=1     
        
        meshPoseBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(meshPoseBlockBytes))+meshPoseBlockBytes

class MeshPoseAnimationBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,vertexAnimationName=None,vertexAnimationframes=None):
        super(MeshPoseAnimationBlock, self ).__init__(blockID,nameSpace,112)
        self.vertexAnimationName = vertexAnimationName
        self.numFrames = vertexAnimationframes
        self.targetMesh = None
        self.saveTargetMesh=0
        self.name = 0
        self.framePoints=[]
        self.frameDurations=[]
        self.frameSubMeshStreams=[]
        self.saveFrameSubMeshStreams=[]
        self.savePoseProps=[]
        
    def writeBinary(self,exportData):
        baseBlockBytes=super(MeshPoseAnimationBlock, self).writeBinary(exportData)
        meshPoseAnimBlockBytes=struct.pack("< H",len(self.vertexAnimationName))+str(self.vertexAnimationName)
        if exportData.debug==True:
            print "self.saveTargetMesh = "+str(self.saveTargetMesh)
        meshPoseAnimBlockBytes+=struct.pack("< I",self.saveTargetMesh) # number of frames
        meshPoseAnimBlockBytes+=struct.pack("< H",len(self.frameDurations)) # number of frames
        meshPoseAnimBlockBytes+=struct.pack("< H",len(self.saveFrameSubMeshStreams[0]))# number of submeshes
        meshPoseAnimBlockBytes+=struct.pack("< H",1) # number of streams
        meshPoseAnimBlockBytes+=struct.pack("< H",1) # types of streams (can be a list later)
        meshPoseBlockAttributesBytes=str()
        for poseProperty in self.savePoseProps:
            if poseProperty==1:
                meshPoseBlockAttributesBytes+=struct.pack("< H",poseProperty)
                meshPoseBlockAttributesBytes+=struct.pack("< I",1)
                meshPoseBlockAttributesBytes+=struct.pack("< B",0)
            if poseProperty==2:
                meshPoseBlockAttributesBytes+=struct.pack("< H",poseProperty)
                meshPoseBlockAttributesBytes+=struct.pack("< I",1)
                meshPoseBlockAttributesBytes+=struct.pack("< B",1)
        meshPoseAnimBlockBytes+=struct.pack("< I",len(meshPoseBlockAttributesBytes))+str(meshPoseBlockAttributesBytes)
        
        frameCounter=0
        while frameCounter<len(self.saveFrameSubMeshStreams):
            meshPoseAnimBlockBytes+=struct.pack("< H",int((1000*self.frameDurations[frameCounter])))
            subMeshCount=0  
            while subMeshCount<len(self.saveFrameSubMeshStreams[frameCounter]):    
                streamCnt=0     
                while streamCnt<len(self.saveFrameSubMeshStreams[frameCounter][subMeshCount]):   # this hsould be 1 iteration for now (only vertexPositionData)   
                    streamDataBits=str()
                    streamCounter=0
                    while streamCounter< len(self.saveFrameSubMeshStreams[frameCounter][subMeshCount][streamCnt].streamData):
                        streamDataBits+=struct.pack(str("< "+str(self.saveFrameSubMeshStreams[frameCounter][subMeshCount][streamCnt].dataType)),self.saveFrameSubMeshStreams[frameCounter][subMeshCount][streamCnt].streamData[streamCounter])
                        streamCounter+=1
                    meshPoseAnimBlockBytes+=struct.pack("< I",len(streamDataBits))+streamDataBits
                    streamCnt+=1
                subMeshCount+=1     
            frameCounter+=1
            
        meshPoseAnimBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(meshPoseAnimBlockBytes))+meshPoseAnimBlockBytes


class SkeletonBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonName=None,skeletonRoot=None):
        super(SkeletonBlock, self ).__init__(blockID,nameSpace,101)
        self.skeletonName = skeletonName
        self.numJoints = 0
        self.skeletonRoot = skeletonRoot   
        self.jointList=[]   
        self.hasRetargetTag=None   
        self.tPoseObject=None   
        self.refObject=None   
        self.saveJointList=[]   
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonBlock, self).writeBinary(exportData)
        skeletonBlockBytes=struct.pack("< H",len(self.skeletonName))+str(self.skeletonName)
        skeletonBlockBytes+=struct.pack("< H",len(self.saveJointList))
        skeletonBlockBytes+=struct.pack("< I",0)
        for joint in self.saveJointList:
            skeletonBlockBytes+=struct.pack("< H",joint.jointID)
            skeletonBlockBytes+=struct.pack("< H",joint.parentID)
            skeletonBlockBytes+=struct.pack("< H",len(joint.lookUpName))+str(joint.lookUpName)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v1.x)+struct.pack("< f",joint.transMatrix.v1.y)+struct.pack("< f",joint.transMatrix.v1.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v2.x)+struct.pack("< f",joint.transMatrix.v2.y)+struct.pack("< f",joint.transMatrix.v2.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.v3.x)+struct.pack("< f",joint.transMatrix.v3.y)+struct.pack("< f",joint.transMatrix.v3.z)
            skeletonBlockBytes+=struct.pack("< f",joint.transMatrix.off.x*exportData.scale)+struct.pack("< f",joint.transMatrix.off.y*exportData.scale)+struct.pack("< f",joint.transMatrix.off.z*exportData.scale)
            skeletonBlockBytes+=struct.pack("< I",0)
            skeletonBlockBytes+=struct.pack("< I",0)
        skeletonBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonBlockBytes))+skeletonBlockBytes

class SkeletonPoseBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonPoseName=None):
        super(SkeletonPoseBlock, self ).__init__(blockID,nameSpace,102)
        self.skeletonPoseName = skeletonPoseName
        self.numJoints = 0
        self.transformations = []
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonPoseBlock, self).writeBinary(exportData)
        skeletonPoseBlockBytes=struct.pack("< H",len(self.skeletonPoseName))+str(self.skeletonPoseName)
        skeletonPoseBlockBytes+=struct.pack("< H",len(self.transformations))
        skeletonPoseBlockBytes+=struct.pack("< I",0)
        jointcounter=0
        while jointcounter<len(self.transformations):
            self.transformations[jointcounter].Normalize()
            skeletonPoseBlockBytes+=struct.pack("< B",1)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v1.x)+struct.pack("< f",self.transformations[jointcounter].v1.y)+struct.pack("< f",self.transformations[jointcounter].v1.z)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v2.x)+struct.pack("< f",self.transformations[jointcounter].v2.y)+struct.pack("< f",self.transformations[jointcounter].v2.z)
            skeletonPoseBlockBytes+=struct.pack("< f",self.transformations[jointcounter].v3.x)+struct.pack("< f",self.transformations[jointcounter].v3.y)+struct.pack("< f",self.transformations[jointcounter].v3.z)
            skeletonPoseBlockBytes+=struct.pack("< f",float(self.transformations[jointcounter].off.x))+struct.pack("< f",float(self.transformations[jointcounter].off.y))+struct.pack("< f",float(self.transformations[jointcounter].off.z))
            jointcounter+=1
        skeletonPoseBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonPoseBlockBytes))+skeletonPoseBlockBytes

class SkeletonAnimationBlock(BaseBlock):
    def __init__(self,blockID=None,nameSpace=None,skeletonAnimationName=None,skeletonAnimationframes=None):
        super(SkeletonAnimationBlock, self ).__init__(blockID,nameSpace,103)
        self.skeletonAnimationName = skeletonAnimationName
        self.numFrames = skeletonAnimationframes
        self.framesImported = 0
        self.targetSkeletonJointList = []  
        self.framesDurationsList = []  
        self.framesIDSList = []  
        self.framesIDSList2 = []  
    def writeBinary(self,exportData):
        baseBlockBytes=super(SkeletonAnimationBlock, self).writeBinary(exportData)
        skeletonAnimationBlockBytes=struct.pack("< H",len(self.skeletonAnimationName))+str(self.skeletonAnimationName)
        skeletonAnimationBlockBytes+=struct.pack("< H",len(self.framesIDSList2))
        skeletonAnimationBlockBytes+=struct.pack("< I",0)
        frameCounter=0
        while frameCounter<len(self.framesIDSList2):
            skeletonAnimationBlockBytes+=struct.pack("< I",int(self.framesIDSList2[frameCounter]))
            skeletonAnimationBlockBytes+=struct.pack("< H",int((1000*self.framesDurationsList[frameCounter])))
            frameCounter+=1
        skeletonAnimationBlockBytes+=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(skeletonAnimationBlockBytes))+skeletonAnimationBlockBytes

        
class UVAnimationBlock(BaseBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes=super(UVAnimationBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)


class NameSpaceBlock(BaseBlock):
    def __init__(self):
        self.name = "undefined"
    def writeBinary(self,exportData):
        baseBlockBytes=super(NameSpaceBlock, self).writeBinary(exportData)
        return baseBlockBytes+struct.pack("< I",0)

class MetaDataBlock(BaseBlock):
    def __init__(self,blockID=0,nameSpace=0):
        super(MetaDataBlock, self ).__init__(blockID,nameSpace,255)
    def writeBinary(self,exportData):
        baseBlockBytes=super(MetaDataBlock, self).writeBinary(exportData)
        metaDataBytes=struct.pack("< I",0)
        return baseBlockBytes+struct.pack("< I",len(metaDataBytes))+metaDataBytes
		
		
class BaseAttribute(object):
    def __init__(self):
        #tester=0
        #tesere=2
        #while tester<tesere:
            #print tester
        #    tester+=1
        self.attributeID = 0
        self.attributeValue = None

class awdGeometryStream(object):
    def __init__(self,streamType,streamData):
        self.streamType=streamType
        self.streamTypeName="None"
        self.streamData=streamData
        if streamType==1:#Vertex
            self.streamTypeName="Vertex"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==2:#Index
            self.streamTypeName="Index"
            self.dataType = "H"
            self.dataType2 = 2
        if streamType==3:#UV
            self.streamTypeName="UV"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==4:#VertexNormals
            self.streamTypeName="VertexNormals"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==5:#VertexTangents
            self.streamTypeName="VertexTangents"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==6:#JointIndex
            self.streamTypeName="JointIndex"
            self.dataType = "H"
            self.dataType2 = 2
        if streamType==7:#JointWeights
            self.streamTypeName="JointWeights"
            self.dataType = "f"
            self.dataType2 = 4
        if streamType==8:#quads - not used by official AWD
            self.streamTypeName="quads"
            self.dataType = "H"
            self.dataType2 = 2

class awdSubMesh(object):
    def __init__(self,materialName,selectionName,selectionIndexe, textureTag):
        self.materialName= materialName
        self.selectionName= selectionName
        self.selectionIndexe= selectionIndexe
        self.textureTag= textureTag

        self.objectSettings= 0
        self.saveSubMeshProps=0
        self.saveGeometryStreams = []
        self.saveUserAttributesList= 0

        self.weightsBuffer= []
        self.jointidxBuffer= []
        self.saveIndexBuffer= []
        self.saveWeightsBuffer= []

        self.vertexBuffer= []
        self.indexBuffer= []
        self.uvBuffer= []
        self.normalBuffer= []
        self.faceNormal= []
        self.quadBuffer= []

        self.uniquePoolDict= {}

    def writeBinary(self,exportData):
        outputBits=struct.pack("< I",self.saveSubMeshProps)
        subMeshCount=0
        outputString="Subemesh '"+str(self.selectionName)+"' streams = "
        while subMeshCount<len(self.saveGeometryStreams):
            if len(self.saveGeometryStreams[subMeshCount].streamData)>0:
            
                print "subGeoStream = "+str(self.saveGeometryStreams[subMeshCount].streamTypeName)
                outputBits+=struct.pack("< B",self.saveGeometryStreams[subMeshCount].streamType)
                outputBits+=struct.pack("< B",self.saveGeometryStreams[subMeshCount].dataType2)
                streamDataBits=str()
                streamCounter=0
                outputString+=str(self.saveGeometryStreams[subMeshCount].streamTypeName)+" = "+str(len(self.saveGeometryStreams[subMeshCount].streamData))+"  / "
                while streamCounter< len(self.saveGeometryStreams[subMeshCount].streamData):
                    streamDataBits+=struct.pack(str("< "+str(self.saveGeometryStreams[subMeshCount].dataType)),self.saveGeometryStreams[subMeshCount].streamData[streamCounter])
                    streamCounter+=1
                outputBits+=struct.pack("< I",len(streamDataBits))+streamDataBits

            subMeshCount+=1
        if exportData.debug==True:
            print outputString
        outputBits+=struct.pack("< I",self.saveUserAttributesList)
        return outputBits