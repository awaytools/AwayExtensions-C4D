# the main Scene containing all the data and parameters needed for export
# One Instance of this class is create at the beginning of the export process in the "mainExporter.py" 
# this instance is stored in the variable "exportData" and gets modified withhin the export-process


import c4d


from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainHelpers 
from awdexporter import classesHelper 

class mainScene(object):
    def __init__(self, doc,mainDialog):
    
        self.skeleton=None
        self.idCounter = 0  # will count the ids of the awdBlocks.
        self.doc = doc 
        self.name = doc.GetDocumentName()
        self.fps = doc.GetFps()
        self.animationCounter=0
        self.allStatusLength = 0
        self.allStatus = 0
        self.subStatus = 0
        self.status = 0
        self.useInsteadSubMeshDic = {}# used to translate between 
        self.scale = mainDialog.GetReal(ids.REAL_SCALE)
        self.firstFrame=mainDialog.GetReal(ids.REAL_FIRSTFRAME)
        self.lastFrame=mainDialog.GetReal(ids.REAL_LASTFRAME)
        self.unusedMats=mainDialog.GetReal(ids.CBOX_UNUSEDMATS) 
        self.debug=mainDialog.GetBool(ids.CBOX_DEBUG)        
        self.embedTextures=mainDialog.GetLong(ids.COMBO_TEXTURESMODE)        
        self.openPrefab=mainDialog.GetBool(ids.CBOX_OPENPREFAB)
        self.exportLightXML=mainDialog.GetBool(ids.CBOX_EXPORTLIGHTXML)
        self.exportExtraMats=mainDialog.GetBool(ids.CBOX_LIGHTMATERIALS)
        self.exportUnsupportedTextures=mainDialog.GetBool(ids.CBOX_UNSUPPORTETTEX)
        self.primitives=[]
        
        # store the current selected objects/tags/materials, so we can restore the selection after export
        self.originalActiveObjects = doc.GetActiveObjects(True)
        self.originalActiveTags = doc.GetActiveTags()
        self.originalActiveMaterials = doc.GetActiveMaterials()
        
        self.originalTime=doc.GetTime()#store the original play position
        self.storeEditMode=doc.GetMode()#store the current EditMode
        self.allc4dMaterials = doc.GetMaterials() # get all Materials found in the document        
        
        self.datei="" # the path to the output-file. will be set at beginning of export by Saveas-Dialog, so we have the Output-Path to export lightXML and textures to
        	
        # define the some infos needed for the AWD-File-Header     
        self.headerMagicString = "AWD"
        self.headerVersionNumberMajor = 2
        self.headerVersionNumberMinor = 1           
        self.headerFlagBits=0x0
        if mainDialog.GetBool(ids.CBOX_STREAMING)==True:
            self.headerFlagBits=0x1			
        self.headerCompressionType=0
        if mainDialog.GetBool(ids.CBOX_COMPRESSED)==True:
            self.headerCompressionType=1
        self.allObjects=[]
        self.AWDerrorObjects = [] # if a error occurs, a error-object will be added to this list, and the export-process will be ended. on end of export, this errors will be printed out
        self.AWDwarningObjects = [] # if a warning occurs, a warning-object will be added to this list. on end of export, this warning will be printed out
        
        self.allSaveAWDBlocks = [] # this wll contain all awdBlocks in the correct order, ready for export
        self.allAWDBlocks = [] # this wll contain all awdBlocks, even the ones that will not be exported
        self.allPlaceHolder = [] # this wll contain all awdBlocks, even the ones that will not be exported
        
        self.unconnectedInstances = [] # a list of all meshinstancesBlocks, so we can loop trough them and connect them to the correct geometryBlock, after all awdBlocks have been created
        
        self.jointIDstoJointBlocks = {} # dictionary to find a JointBlock using a joints ID
        self.jointIDstoSkeletonBlocks = {} # dictionary to find a SkeletonBlock using a joints ID
        self.allSkeletonBlocks = []   # a list of all skeletionBlocks that should be exported  
        self.allSkeletonAnimations = []  # a list of all allSkeletonAnimations that should be exported
        self.allVertexAnimations=[]
        self.lightPickerDic = {}  # dictionary to makes shure only one LightPicker is created for each combination of Lights 
        self.lightPickerList = [] # will contain all LightPickers - LightPicker are no AWDBlocks, but simple classes containing a name and a list of light-indicies (allAWDBlocks[lightIndex]=lightBlock)
        self.lightPickerCounter=0
        self.allLights = []   # a list of all lights, used by mainLightRouting
        
        self.defaultObjectSettings = 0    
        
        self.unsupportedTextures=[] # will contain a list of exported but unsupported textures, for every texture it should contain the infos about channel and material too
        self.texturePathToAWDBlocksDic = {}  # dictionary to translate a filePath to a AWDTextureBlock, to make shure we only save one TextureBlock for each Texture-Path
   
        self.colorMaterials = {} # dictionary to make shure for each object-color exists onyl one material 
        self.allMatBlocks = [] # not really needed?
        self.IDsToAWDBlocksDic = {} # not really needed?
        self.allMeshObjects = []
        self.allSceneObjects = []
        self.allLightBlocks = [] 
        self.allPrimitives= [] 
        
  
            

                                