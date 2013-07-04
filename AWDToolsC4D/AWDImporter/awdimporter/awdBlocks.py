import c4d
from c4d import documents
class BaseBlock(object):
    def __init__(self,blockID=0,nameSpace=0,blockType=0,blockFlags=None,blockSize=0):
        self.blockID = blockID
        self.nameSpace = nameSpace
        self.blockType = blockType
        self.blockFlags= blockFlags
        self.blockSize= blockSize
        self.blockDataObject = None
        self.sceneObject=None

class BaseAttribute(object):
    def __init__(self):
        self.attributeID = 0
        self.attributeValue = None

class TriangleGeometrieBlock(object):
    def __init__(self):
        self.isSkinned=False
        self.polygonObject = None
        self.allJointIndexe = []
        self.allJointWeights = []
        self.numJoints = []
        self.indexDics = []
        self.maxJointIndex = []
        self.minJointIndex = []
        self.SubmeshPointCount = []
        self.SubmeshTrisCount = []

class PrimitiveGeometrieBlock(object):
    def __init__(self):
        self.name = "undefined"

class SceneBlock(object):
    def __init__(self):
        self.name = "undefined"

class ContainerBlock(object):
    def __init__(self):
        self.sceneObject = None

class MeshInstanceBlock(object):
    def __init__(self):
        self.isSkinned=False
        self.sceneObject = None

class LightBlock(object):
    def __init__(self):
        self.name = "undefined"

class CameraBlock(object):
    def __init__(self):
        self.name = "undefined"

class StandartMaterialBlock(object):
    def __init__(self):
        self.name = "undefined"

class TextureBlock(object):
    def __init__(self):
        self.name = None
        self.isEmbed = None
        self.dataSize = None
        self.filePath = None
		
class CubeTextureBlock(object):
    def __init__(self):
        self.isSkinned=False
        self.polygonObject = None
        self.sceneObject = None
		

class SkeletonBlock(object):
    def __init__(self):
        self.name = "undefined"
        self.numJoints = 0
        self.rootJoint = None   
        self.jointList=[]   
        self.hasRetargetTag=None   
        self.tPoseObject=None   
        self.refObject=None   

class SkeletonPoseBlock(object):
    def __init__(self):
        self.name = "undefined"
        self.numJoints = 0
        self.transformations = []
		
class SkeletonAnimationBlock(object):
    def __init__(self):
        self.name = "undefined"
        self.numFrames = 0
        self.framesImported = 0
        self.targetSkeletonJointList = []  
        self.framesDurationsList = []  
        self.framesIDSList = []  
	
class UVAnimationBlock(object):
    def __init__(self):
        self.name = "undefined"
		
class NameSpaceBlock(object):
    def __init__(self):
        self.name = "undefined"
		
class MetaDataBlock(object):
    def __init__(self):
        self.numAttributes = 0
        self.Attributes = []