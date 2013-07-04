# functions running in c4d-main-thread
import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import mainMaterials
from awdexporter import workerHelpers

# create a AWDBlock fior each Object and each tag, gather all in a List, and rename the c4d-objects/tags using their list index, so
def createAllAWDBlocks(exportData,objList):
    for object in objList:
        createBaseBlock(exportData,object)
        for tag in object.GetTags():
            createBaseBlock(exportData,tag)
        createAllAWDBlocks(exportData,object.GetChildren())
            

def createBaseBlock(exportData,object):
    newAWDBlock=classesAWDBlocks.WrapperBlock(object,object.GetName(),0)
    exportData.allAWDBlocks.append(newAWDBlock)  
    object.SetName(str(exportData.idCounter))
    exportData.idCounter+=1
        
def createAllSceneBlocks(exportData,objList,parentExportSettings=None,tagForExport=True,returner=True):
    for object in objList:
        exporterSettingsTag=object.GetTag(1028905)
        thisExporterSettings=parentExportSettings
        exportThisObj=True
        returnerAR=[False,False]
        vertexAnimationSet=object.GetTag(1030508)
        if vertexAnimationSet is None:
            vertexAnimation=object.GetTag(1030484)
            if vertexAnimation is None:
                if exporterSettingsTag is None:
                    returnerAR=createSceneBlock(exportData,object,tagForExport,returner,False)
                    
                if exporterSettingsTag is not None:
                    if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== True:
                        pass
                    if exporterSettingsTag[1014]==True and exporterSettingsTag[1016]== True:
                        returnerAR=createSceneBlock(exportData,object,tagForExport,returner,False)
                    if exporterSettingsTag[1014]==True and exporterSettingsTag[1016]== False:
                        returnerAR=createSceneBlock(exportData,object,tagForExport,returner,False)
                    if exporterSettingsTag[1014]==False and exporterSettingsTag[1016]== False:
                        returnerAR=createSceneBlock(exportData,object,tagForExport,returner,True)
                if returnerAR[0]==True:
                    createAllSceneBlocks(exportData,object.GetChildren(),thisExporterSettings,returnerAR[1],returnerAR[0])
#function check the object-type of a c4d-object and creates a corresponding AWDBlock (see classesAWDBlocks) 
def createSceneBlock(exportData,curObj,tagForExport,returner=True,onlyNullObject=False):  
  
    if onlyNullObject==False:     
        if curObj.GetType() == c4d.Oextrude:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ospline:
            if len(curObj.GetChildren())==0:
                return False, False
        
    
    #####	Primitives
        isPrimitv=False
        if curObj.GetType() == c4d.Oplane:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)
            newAWDBlockGEO.primType=1
            if curObj[c4d.PRIM_PLANE_WIDTH]!=100:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_PLANE_WIDTH])
            if curObj[c4d.PRIM_PLANE_HEIGHT]!=100:
                newAWDBlockGEO.primitiveProps.append(102)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_PLANE_HEIGHT])
            if curObj[c4d.PRIM_PLANE_SUBW]!=1:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_PLANE_SUBW])
            if curObj[c4d.PRIM_PLANE_SUBH]!=1:
                newAWDBlockGEO.primitiveProps.append(302)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_PLANE_SUBH])
            # to do: add yaxis up curObj[c4d.PRIM_AXIS]
        
        if curObj.GetType() == c4d.Ocube:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)
            newAWDBlockGEO.primType=2
            if curObj[c4d.PRIM_CUBE_LEN].x!=100:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_LEN].x)
            if curObj[c4d.PRIM_CUBE_LEN].y!=100:
                newAWDBlockGEO.primitiveProps.append(102)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_LEN].y)
            if curObj[c4d.PRIM_CUBE_LEN].z!=100:
                newAWDBlockGEO.primitiveProps.append(103)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_LEN].z)
            if curObj[c4d.PRIM_CUBE_SUBX]!=1:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.depth=curObj[c4d.PRIM_CUBE_SUBX]
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_SUBX])
            if curObj[c4d.PRIM_CUBE_SUBY]!=1:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.depth=curObj[c4d.PRIM_CUBE_SUBY]
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_SUBY])
            if curObj[c4d.PRIM_CUBE_SUBZ]!=1:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.depth=curObj[c4d.PRIM_CUBE_SUBZ]
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CUBE_SUBZ])
            # for a cube exportet from c4d cube.tile6 will allways be false
        
        if curObj.GetType() == c4d.Osphere:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj) 
            newAWDBlockGEO.primType=3
            if curObj[c4d.PRIM_SPHERE_RAD]!=50:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_SPHERE_RAD])
            if curObj[c4d.PRIM_SPHERE_SUB]!=16:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_SPHERE_SUB])
            # to do: sphere has two segments properties in away but only 1 in c4d
            #Sphere[c4d.PRIM_SPHERE_TYPE]
            #Sphere[c4d.PRIM_SPHERE_PERFECT]
            
        if curObj.GetType() == c4d.Ocylinder:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)    
            newAWDBlockGEO.primType=4
            if curObj[c4d.PRIM_CYLINDER_RADIUS]!=50:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CYLINDER_RADIUS])
            if curObj[c4d.PRIM_CYLINDER_HEIGHT]!=100:
                newAWDBlockGEO.primitiveProps.append(103)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CYLINDER_HEIGHT])
            if curObj[c4d.PRIM_CYLINDER_SEG]!=16:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CYLINDER_SEG])
            if curObj[c4d.PRIM_CYLINDER_HSUB]!=1:
                newAWDBlockGEO.primitiveProps.append(302)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CYLINDER_HSUB])
            #Cylinder[c4d.PRIM_AXIS]
            
        if curObj.GetType() == c4d.Ocone:   
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)
            if curObj[c4d.PRIM_CONE_TRAD]==0:
                newAWDBlockGEO.primType=5
            if curObj[c4d.PRIM_CONE_TRAD]>0: 
                newAWDBlockGEO.primType=4
                if curObj[c4d.PRIM_CONE_TRAD]!=50:   
                    newAWDBlockGEO.primitiveProps.append(101)
                    newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CONE_TRAD])
            if curObj[c4d.PRIM_CONE_BRAD]!=50:
                if curObj[c4d.PRIM_CONE_TRAD]>0: 
                    newAWDBlockGEO.primitiveProps.append(102)
                if curObj[c4d.PRIM_CONE_TRAD]==0: 
                    newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CONE_BRAD])
            if curObj[c4d.PRIM_CONE_HEIGHT]!=100:
                if curObj[c4d.PRIM_CONE_TRAD]>0: 
                    newAWDBlockGEO.primitiveProps.append(103)
                if curObj[c4d.PRIM_CONE_TRAD]==0: 
                    newAWDBlockGEO.primitiveProps.append(102)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CONE_HEIGHT])
            if curObj[c4d.PRIM_CONE_SEG]!=16:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CONE_SEG])
            if curObj[c4d.PRIM_CONE_HSUB]!=1:
                newAWDBlockGEO.primitiveProps.append(302)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CONE_HSUB])
            #Cone[c4d.PRIM_AXIS]
         
        if curObj.GetType() == c4d.Ocapsule:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)      
            newAWDBlockGEO.primType=6 
            if curObj[c4d.PRIM_CAPSULE_RADIUS]!=50:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CAPSULE_RADIUS])
            if curObj[c4d.PRIM_CAPSULE_HEIGHT]!=100:
                newAWDBlockGEO.primitiveProps.append(102)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CAPSULE_HEIGHT])
            if curObj[c4d.PRIM_CAPSULE_SEG]!=16:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_CAPSULE_SEG])
            #allHeightSegments=curObj[c4d.PRIM_CAPSULE_HSUB]+(curObj[c4d.PRIM_CAPSULE_FSUB]*2)
            #if allHeightSegments!=15:
            #    checkHeight=float(allHeightSegments/2);
            #    if float(math.round(checkHeight))!=float(checkHeight):
            #        allHeightSegments+=1
            #    newAWDBlockGEO.primitiveProps.append(302)
            #    newAWDBlockGEO.primitiveValues.append(allHeightSegments)
            #Cone[c4d.PRIM_AXIS]
            
        if curObj.GetType() == c4d.Otorus:
            isPrimitv=True
            newAWDBlockGEO=classesAWDBlocks.PrimitiveGeometrieBlock(exportData.idCounter,0,curObj)      
            newAWDBlockGEO.primType=7 
            if curObj[c4d.PRIM_TORUS_OUTERRAD]!=50:
                newAWDBlockGEO.primitiveProps.append(101)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_TORUS_OUTERRAD])
            if curObj[c4d.PRIM_TORUS_INNERRAD]!=50:
                newAWDBlockGEO.primitiveProps.append(102)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_TORUS_INNERRAD])
            if curObj[c4d.PRIM_TORUS_SEG]!=16:
                newAWDBlockGEO.primitiveProps.append(301)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_TORUS_SEG])
            if curObj[c4d.PRIM_TORUS_CSUB]!=8:
                newAWDBlockGEO.primitiveProps.append(302)
                newAWDBlockGEO.primitiveValues.append(curObj[c4d.PRIM_TORUS_CSUB])
            #Torus[c4d.PRIM_AXIS]   
        
        if isPrimitv == True:
            newAWDBlockGEO.saveLookUpName="Geo_"+str(exportData.allAWDBlocks[int(curObj.GetName())].name)
            
            newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(curObj,str(curObj.GetName())+"_geom",11)
            newAWDWrapperBlock.tagForExport=tagForExport
            exportData.idCounter+=1
            newAWDWrapperBlock.data=newAWDBlockGEO
            exportData.allAWDBlocks.append(newAWDWrapperBlock) 
    
            newAWDBlock=classesAWDBlocks.MeshInstanceBlock(exportData.idCounter,0,exportData.idCounter-1,curObj)
            newAWDBlock.dataParentBlockID=0
            if curObj.GetTag(1019365):
                newAWDBlock.isSkinned=True
            if curObj.GetUp():
                parentID=exportData.allAWDBlocks[int(curObj.GetUp().GetName())]
                if parentID!=None:
                    newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())                
                    
            materials=workerHelpers.getMaterials(curObj,[],True) 
            thisMat=None
            newAWDBlockGEO.hasMats=False
            if len(materials)>0:
                newAWDBlockGEO.hasMats=True
                thisMat=materials[len(materials)-1]
            materials2=workerHelpers.getObjectColorMode(curObj,thisMat,exportData)
            exportData.allAWDBlocks[int(materials2[1][0])].tagForExport=True
            newAWDBlockGEO.colorStyle=materials2[0]
            if materials2[0]==True:
                newAWDBlockGEO.baseMat=materials2[1][0]
            newAWDBlock.saveMaterials.append(materials2[1][0])    
        
            exportData.allAWDBlocks[int(curObj.GetName())].data=newAWDBlock
            exportData.allAWDBlocks[int(curObj.GetName())].blockType=23
            exportData.allAWDBlocks[int(curObj.GetName())].tagForExport=tagForExport
            newAWDBlockGEO.sceneBlocks.append(exportData.allAWDBlocks[int(curObj.GetName())])
            exportData.allSceneObjects.append(exportData.allAWDBlocks[int(curObj.GetName())])
            
            return True, True
        
    
        if curObj.GetType() == c4d.Oinstance:
            allowedInstynceTypes=[c4d.Opolygon,c4d.Ocube,c4d.Osphere,c4d.Oplane,c4d.Ocylinder,c4d.Ocone,c4d.Ocapsule,c4d.Otorus]
            for allowedtype in allowedInstynceTypes:
                if curObj[c4d.INSTANCEOBJECT_LINK].GetType()==allowedtype:
                    newAWDBlock=classesAWDBlocks.MeshInstanceBlock(int(curObj.GetName()),0,None,curObj)
                    newAWDBlock.geoObj=curObj[c4d.INSTANCEOBJECT_LINK]
                    if curObj[c4d.INSTANCEOBJECT_RENDERINSTANCE]==True:
                        newAWDBlock.isRenderInstance=True    
        
                    newAWDBlock.dataParentBlockID=0
                    parentObj=curObj.GetUp()
                    if parentObj is not None:
                        parentID=exportData.allAWDBlocks[int(curObj.GetUp().GetName())]
                        if parentID!=None:
                            newAWDBlock.dataParentBlockID=int(parentObj.GetName())
                    exportData.allAWDBlocks[int(curObj.GetName())].data=newAWDBlock
                    exportData.allAWDBlocks[int(curObj.GetName())].blockType=23
                    exportData.allAWDBlocks[int(curObj.GetName())].tagForExport=tagForExport
                    exportData.allSceneObjects.append(exportData.allAWDBlocks[int(curObj.GetName())])
                    exportData.unconnectedInstances.append(exportData.allAWDBlocks[int(curObj.GetName())])
                    return True, True   
            
            #print "Instance objects are only allowed to point to Mesh objects"
            if len(curObj.GetChildren())==0:
                return False, False        
            
    
        if curObj.GetType() == c4d.Opolygon:
            
            meshInstanceID=int(curObj.GetName())
            newAWDBlockGEO=classesAWDBlocks.TriangleGeometrieBlock(exportData.idCounter,0,curObj)
            
            newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(curObj,str(exportData.allAWDBlocks[int(curObj.GetName())].name)+"_geom",11)
            newAWDWrapperBlock.tagForExport=tagForExport
            newAWDBlockGEO.saveLookUpName=newAWDWrapperBlock.name
            newAWDWrapperBlock.data=newAWDBlockGEO
            exportData.allAWDBlocks.append(newAWDWrapperBlock) 
            exportData.allMeshObjects.append(newAWDWrapperBlock)
            exportData.idCounter+=1
    
            newAWDBlock=classesAWDBlocks.MeshInstanceBlock(meshInstanceID,0,exportData.idCounter-1,curObj)
            newAWDBlock.dataParentBlockID=0
            if curObj.GetTag(1019365):
                newAWDBlock.isSkinned=True
            if curObj.GetUp():
                parentID=exportData.allAWDBlocks[int(curObj.GetUp().GetName())]
                if parentID!=None:
                    newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
                   
            exportData.allAWDBlocks[meshInstanceID].data=newAWDBlock
            exportData.allAWDBlocks[meshInstanceID].blockType=23
            exportData.allAWDBlocks[meshInstanceID].tagForExport=tagForExport
            exportData.allSceneObjects.append(exportData.allAWDBlocks[meshInstanceID])
            newAWDBlockGEO.sceneBlocks.append(exportData.allAWDBlocks[meshInstanceID])
            return True, True
        
        if curObj.GetType() == c4d.Oskin:
            if len(curObj.GetChildren())==0:
                return False, False
        
        if curObj.GetType() == c4d.Ojoint:
            if curObj.GetTag(1028937):
                skeletonTag=curObj.GetTag(1028937)
                if skeletonTag[1014]==False or skeletonTag[1010]==False :
                    #print "Do not export Skeleton as SceneObjects"
                    tagForExport=False
                    returner= True
    
                return False, False
    
    
        if curObj.GetType() == c4d.Olight:
            lightType=None
            if curObj[c4d.LIGHT_TYPE]==0:
                lightType=0
            if curObj[c4d.LIGHT_TYPE]==3:
                lightType=1
            if lightType is not None:
                newAWDBlock=classesAWDBlocks.LightBlock(int(curObj.GetName()),0,curObj,lightType)
                if exportData.unusedMats==True:
                    newAWDBlock.tagForExport=True
                if curObj.GetUp():
                    parentID=exportData.allAWDBlocks[int(curObj.GetUp().GetName())]
                    if parentID!=None:
                        newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
                exportData.allAWDBlocks[int(curObj.GetName())].data=newAWDBlock
                exportData.allAWDBlocks[int(curObj.GetName())].blockType=41
                exportData.allAWDBlocks[int(curObj.GetName())].tagForExport=tagForExport
                exportData.allSceneObjects.append(exportData.allAWDBlocks[int(curObj.GetName())])
                exportData.allLightBlocks.append(exportData.allAWDBlocks[int(curObj.GetName())])
                return True, True
        
        if curObj.GetType() == c4d.Ocamera:
            if len(curObj.GetChildren())==0:
                return False, False

    newAWDBlock=classesAWDBlocks.ContainerBlock(exportData.idCounter,0,curObj)        
    newAWDBlock.dataParentBlockID=0
    if curObj.GetUp():
        parentID=exportData.allAWDBlocks[int(curObj.GetUp().GetName())]
        if parentID!=None:
            newAWDBlock.dataParentBlockID=int(curObj.GetUp().GetName())
    exportData.allAWDBlocks[int(curObj.GetName())].data=newAWDBlock
    exportData.allAWDBlocks[int(curObj.GetName())].blockType=22
    exportData.allAWDBlocks[int(curObj.GetName())].tagForExport=tagForExport
    exportData.allSceneObjects.append(exportData.allAWDBlocks[int(curObj.GetName())])
    
    return returner,tagForExport