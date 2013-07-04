import c4d
from c4d import documents

	
class mainScene(object):
    def __init__(self, scale=None,scaleJoints=None, fps=None):
        self.path = ""
        self.scale = scale
        self.scaleJoints = scaleJoints
        self.fps = fps
        self.objectsIDsDic = {}
        self.skeletonIDsDic = {}
        self.meshIDsDic = {}
        self.lightsIDsDic = {}
        self.materialsIDsDic = {}
        self.cameraIDsDic = {}
        self.texturesIDsDic = {}   
        self.latestSkinnedMesh = None
        self.latestSkinnedMeshUsed = False
        self.lastSkeleton = None
        self.latestjointList = []
        self.latestSkeletonAnimation = None
        self.skeletonPoses=[]
        self.rootObjects=[]
		
        self.unusedIDsDic = {}   
        self.blockDic = {}    
        self.geoDic = {}    
        self.texDic = {}    
        self.materialsDic = {}  
		
        self.skeletonTrannslations = False 
        self.skeletonTrannslationsRoot = False 
        self.skeletonScales = False 
        self.skeletonScalesRoot = False  
        self.skeletonQuaternions = False  
        self.skeletonTPoseRetarget = False  
		
        self.debug = False  
		
        self.texturesExternPathMode = 0  
        self.texturesExternPath = None  
        self.texturesEmbedPathMode = 0  
        self.texturesEmbedPath = None  

        self.magicString = ""
        self.versionNumberMajor = 0
        self.versionNumberMinor = 0
        self.flags = 00
        self.compression=0
        self.bodyLength=0
		
		
        self.parsingOK=False
        self.errorMessages=[0]