# functions that will run inside the background-worker-thread

import c4d
import copy
import struct
import os
import zlib
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import workerReorderBlocks
from awdexporter import classesAWDBlocks
from awdexporter import mainMaterials
from awdexporter import mainLightRouting

# called by "WorkerExporter.py"
def getAllObjectData(exportData):
    for awdSceneBlock in exportData.allSceneObjects:
        dataMatrix=awdSceneBlock.data.sceneObject.GetMl()
        if awdSceneBlock.data.isSkinned==True:
            pass#dataMatrix=c4d.Matrix()
        awdSceneBlock.data.dataMatrix=dataMatrix
		
# called by "WorkerExporter.py"
# creates the final binary string and saves it to harddisc
def exportAllData(exportData):        
    outputBits=struct.pack('< 3s',exportData.headerMagicString)
    outputBits+=struct.pack('< B',exportData.headerVersionNumberMajor)
    outputBits+=struct.pack('< B',exportData.headerVersionNumberMinor)
    outputBits+=struct.pack('< H',exportData.headerFlagBits)
    outputBits+=struct.pack('< B',exportData.headerCompressionType)
    outputBlocks=str()
    blocksparsed=0
    while blocksparsed<len(exportData.allSaveAWDBlocks):
        outputBlocks+=exportData.allSaveAWDBlocks[blocksparsed].writeBinary(exportData)
        blocksparsed+=1
    if exportData.headerCompressionType==1:
        outputBody = zlib.compress(outputBlocks, 9)
    if exportData.headerCompressionType==0:
        outputBody = outputBlocks
    outputBits+=struct.pack('< I',len(outputBody))
    outputBits+=outputBody
    f = open(exportData.datei, 'wb')
    f.write(outputBits)
    f.close()
    if exportData.openPrefab==True:
        c4d.storage.GeExecuteFile(exportData.datei)
    return
  
def applymaterialsToPrimitives(exportData): 
    for primitiveBlock in exportData.primitives:    
        primitiveBlock.data.lightPickerIdx=mainLightRouting.getObjectLights(primitiveBlock.targetObject,exportData)# get the LightPicker for this sceneObject (if the lightpicker does not allready exists, it will be created)
        materials=getMaterials(primitiveBlock.targetObject,[],True,exportData) 
        thisMat=None
        geoBlock=exportData.allAWDBlocks[int(primitiveBlock.data.geoBlockID)]
        geoBlock.data.hasMats=False
        if len(materials)>0:
            geoBlock.data.hasMats=True
            thisMat=materials[len(materials)-1]
        materials2=getObjectColorMode(primitiveBlock.targetObject,thisMat,exportData)
        exportData.allAWDBlocks[int(materials2[1][0])].tagForExport=True
        geoBlock.data.colorStyle=materials2[0]
        #if materials2[0]==True:
        geoBlock.data.baseMat=materials2[1][0]
        repeat=False
        if len(exportData.allAWDBlocks[int(materials2[1][0])].data.materialsList)==0:
            exportData.allAWDBlocks[int(materials2[1][0])].data.materialsList.append(materials2[1][0])
            exportData.allAWDBlocks[int(materials2[1][0])].data.lightPicker=primitiveBlock.data.lightPickerIdx
            exportData.allAWDBlocks[int(materials2[1][0])].data.repeat=False
            foundMat=materials2[1][0]
        else:
            foundMat=-1
            for matID in exportData.allAWDBlocks[int(materials2[1][0])].data.materialsList:
                if exportData.allAWDBlocks[int(matID)].data.lightPicker==primitiveBlock.data.lightPickerIdx:
                    if exportData.allAWDBlocks[int(matID)].data.repeat==repeat:
                        foundMat=matID
            if foundMat==-1:
                foundMat=copyAsNewMaterialBlock(exportData,exportData.allAWDBlocks[int(materials2[1][0])],primitiveBlock.data.lightPickerIdx,repeat)
                print "CREATE NEW MATERIAL"
        primitiveBlock.data.saveMaterials.append(foundMat)  
    
def copyAsNewMaterialBlock(exportData, matBlock, lightPicker, repeat):
      # create a AWD-Material-Block for the C4D-Default-Color, in case some Objects have no Materials/ObjectColors Applied
    newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(matBlock.targetObject,matBlock.name,81)
    newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,matBlock.data.colorMat)
    newAWDBlock.mat=matBlock.data.mat
    newAWDBlock.saveLookUpName=matBlock.name
    newAWDBlock.name=matBlock.data.name
    newAWDBlock.lightPicker=lightPicker
    newAWDBlock.repeat=repeat
    newAWDWrapperBlock.data=newAWDBlock
    newAWDWrapperBlock.tagForExport=True 
    exportData.allAWDBlocks.append(newAWDWrapperBlock)  
    returner=exportData.idCounter
    exportData.idCounter+=1
    return returner
    

def reorderAllBlocks(exportData):
    for awdBlock in exportData.allSceneObjects:
        workerReorderBlocks.addToExportList(exportData,awdBlock)
    for awdBlock in exportData.allAWDBlocks:
        workerReorderBlocks.addToExportList(exportData,awdBlock)

def connectInstances(exportData):
    for instanceBlock in exportData.unconnectedInstances:
        isPoly=False
        if instanceBlock.data.sceneObject[c4d.INSTANCEOBJECT_LINK].GetType()==c4d.Opolygon:
            isPoly=True
        geoInstanceID=instanceBlock.data.sceneObject[c4d.INSTANCEOBJECT_LINK].GetName()
        instanceGeoBlock=exportData.allAWDBlocks[int(geoInstanceID)]   
        if instanceGeoBlock is not None:
            geoBlockID=instanceGeoBlock.data.geoBlockID
            geoBlock=exportData.allAWDBlocks[int(geoBlockID)]    
            if geoBlock is not None: 
                instanceBlock.data.geoBlockID=geoBlockID
                geoBlock.data.sceneBlocks.append(instanceBlock)
                if isPoly==False:
                    instanceBlock.data.lightPickerIdx=mainLightRouting.getObjectLights(instanceBlock.targetObject,exportData)# get the LightPicker for this sceneObject (if the lightpicker does not allready exists, it will be created)
                    if str(geoBlock.blockType)==str(11):
                        if instanceBlock.data.isRenderInstance==True:
                            if geoBlock.data.colorStyle==False:
                                instanceBlock.data.saveMaterials=[geoBlock.data.baseMat]
                            if geoBlock.data.colorStyle==True:
                                if geoBlock.data.hasMats==True:
                                    instanceBlock.data.saveMaterials=[geoBlock.data.baseMat]
                                if geoBlock.data.hasMats==False:
                                    materials=getMaterials(instanceBlock.data.sceneObject,[],True,exportData) 
                                    if len(materials)>0:
                                        instanceBlock.data.saveMaterials=[materials[len(materials)-1]]
                                    else:
                                        instanceBlock.data.saveMaterials=[-1]
                        if instanceBlock.data.isRenderInstance==False:
                            materials=getMaterials(instanceBlock.data.sceneObject,[],True,exportData) 
                            thisMaterial=None
                            if len(materials)>0:
                                thisMaterial=materials[len(materials)-1]                    
                            if geoBlock.data.hasMats==True:
                                thisMaterial=geoBlock.data.baseMat
                            returnList = getObjectColorMode(instanceBlock.data.sceneObject,thisMaterial,exportData)
                            instanceBlock.data.saveMaterials=[returnList[1][0]]
                        for mat in instanceBlock.data.saveMaterials:
                            matAwdBlock=exportData.allAWDBlocks[int(mat)]
                            if matAwdBlock is not None:
                                if matAwdBlock.data.isCreated==False and matAwdBlock.data.colorMat==False:
                                    matAwdBlock.data.isCreated=True                
                                    mainMaterials.createMaterial(matAwdBlock.data,exportData)
                                #if instanceBlock.lightPickerIdx>0:
                                    #matAwdBlock.lightPickerID=instanceBlock.lightPickerIdx
                                if matAwdBlock.tagForExport==False:
                                    matAwdBlock.tagForExport=True               
                    
        instanceBlock.geoBlockID=geoBlockID
        
	
				
def getObjectColorMatBlock(exportData,colorVector):
    newColorVecString="#"+str(colorVector)
    colorMat=exportData.colorMaterials.get(newColorVecString,None)  
    #print str(newColorVecString) + "  /  "+str() 
    if colorMat is not None:
        return colorMat
    
    newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(None,"",11)
    newAWDBlock=classesAWDBlocks.StandartMaterialBlock(exportData.idCounter,0,True)
    newAWDBlock.name="Material"
    newAWDBlock.matColor=[colorVector.z*255,colorVector.y*255,colorVector.x*255,0]
    newAWDBlock.saveMatProps.append(1)
    newAWDBlock.isCreated=True
    newAWDWrapperBlock.tagForExport=False 
    newAWDWrapperBlock.data=newAWDBlock
    exportData.idCounter+=1
    exportData.allAWDBlocks.append(newAWDWrapperBlock) 
    exportData.colorMaterials[newColorVecString]=newAWDWrapperBlock
    #exportData.MaterialsToAWDBlocksDic[str(defaultMaterial)]=newAWDBlock 
    return newAWDWrapperBlock
       

    
# this is the function that gets called from the "mainExporter"
def createAnimatorBlocks(objList,exportData):
    for object in objList:                                      # for every object do:
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
            tag=object.GetTag(1030509)
            if tag is not None:
                if tag[1010] == True: 
                    if tag[1012] is None: 
                        print "ERROR = No Animator-Target Set"
                    if tag[1012] is not None: 
                        animSetBlock=exportData.allAWDBlocks[int(tag[1012].GetName())]  
                        print "animationSet = "+str(animSetBlock)+ "    animationSet = "+str(int(tag[1012].GetName()))
                        targetMeshBlock=exportData.allAWDBlocks[int(object.GetName())]
                        newAWDBlockAnimator=classesAWDBlocks.AnimatorBlock(int(tag.GetName()),0,animSetBlock,targetMeshBlock,tag[1011])
                        newAWDBlockAnimator.animatorTyp=2 # this is a vertexAnimation
                        if tag[1018] is not None: # if a skeleton is set, 
                            newAWDBlockAnimator.animatorTyp=1 # this is a  skeletionANmiation
                            
                            newAWDBlockAnimator.skeleton=exportData.allAWDBlocks[int(tag[1018].GetName())]
                            print "newAWDBlockAnimator.skeleton = "+str(newAWDBlockAnimator.skeleton)
                            
                        exportData.allAWDBlocks[int(tag.GetName())].data=newAWDBlockAnimator
                        exportData.allAWDBlocks[int(tag.GetName())].blockType=122
                        exportData.allAWDBlocks[int(tag.GetName())].tagForExport=True
        if exportThisObjChild==True:     
            if len(object.GetChildren())>0:                             # if the object has any Children:
                createAnimatorBlocks(object.GetChildren(),exportData)# execute this function again, passing the children as objList


    
               
                
def getAllPolySelections(curObj,exportData):
    allSelections=[]                                                                                                                            # we create "allSelections" as new empty List
    for selectionTag in curObj.GetTags():                                                                                                           # do for each tag on the Object:          
        if selectionTag.GetType()==c4d.Tpolygonselection:                                                                                           # if the tag is a Polygon-SelectionTag:
            allSelections.append(classesHelper.PolySelection(exportData.allAWDBlocks[int(selectionTag.GetName())].name,selectionTag.GetBaseSelect().GetAll(len(curObj.GetAllPolygons())))) # store a new instance of HelperClass "PolySelection" in  "allSelections"                       
    return allSelections
   
# returns a list of materials (if inherite==True, the list will inculde materials that are applied to the 
def getMaterials(curObj,allSelections,inherite,exportData):
    returnMats=[]
    for tag in curObj.GetTags():                                        # do for each tag on the Object:  
        if tag.GetType()==c4d.Ttexture:                                     # if the tag is a texture tag:
            foundTexturetag=True                                                # set "foundTexturetag" to True 
            curSelection=tag[c4d.TEXTURETAG_RESTRICTION]                        # get the name of the Polygon-Selection that restricts the Material or None or ""     
            print "found a texturetag = "+str(tag[c4d.TEXTURETAG_RESTRICTION]) 
            if curSelection is not None and str(curSelection)!=str(""):         # if the name of the Polygon-Selection is not None and not "", the material is restricted by a Selection:
                for selection in allSelections:                                         # for each selection do:
                    print "selection = "+str(selection.name)+" / "+str(tag[c4d.TEXTURETAG_RESTRICTION])
                    if str(tag[c4d.TEXTURETAG_RESTRICTION])==selection.name:                # if this is the selection that is restricting the textureTag: 
                        if tag.GetMaterial() is not None:                                      
                            if len(returnMats)==0:                                                  
                                newMaterialList=[]
                                newMaterialList.append(str(1))                      
                                newMaterialList.append(classesHelper.PolySelection("Base",[]))
                                newMaterialList.append(None)  
                                returnMats.append(newMaterialList)
                            if str(tag.GetMaterial().GetTypeName())!="Mat":                         # if this Materials-type is not a C4d-DefaultMaterial:
                                newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName())  # create a Warning Object
                                exportData.AWDwarningObjects.append(newWarning)                             
                                newMaterialList=[]
                                newMaterialList.append(str(1))                      
                                newMaterialList.append(selection)
                                newMaterialList.append(None)  
                                returnMats.append(newMaterialList)
                            if str(tag.GetMaterial().GetTypeName())=="Mat":                         
                                newMaterialList=[]
                                newMaterialList.append(tag.GetMaterial().GetName())             
                                newMaterialList.append(selection)
                                exportData.allAWDBlocks[int(tag.GetMaterial().GetName())].data.textureTags.append(tag)
                                newMaterialList.append(tag)  
                                returnMats.append(newMaterialList)
                        break
                                                
            if curSelection is None or str(curSelection)==str(""):              # if the name of the Restriction is None or "", the material is not restricted by any selection:
                if tag.GetMaterial() is not None:                                  
                    if str(tag.GetMaterial().GetTypeName())!="Mat":                     # if this Materials-type is not a C4d-DefaultMaterial: 
                        newWarning=AWDerrorObject(ids.WARNINGMESSAGE1,tag.GetMaterial().GetName()) # create a Warning Object
                        exportData.AWDwarningObjects.append(newWarning)                     
                        newMaterialList=[]
                        newMaterialList.append(str(1))                      
                        newMaterialList.append(classesHelper.PolySelection("Base",[]))
                        newMaterialList.append(None)  
                        returnMats.append(newMaterialList)
                    if str(tag.GetMaterial().GetTypeName())=="Mat":                     # if this Materials-type is a C4d-DefaultMaterial: 
                        newMaterialList=[]
                        newMaterialList.append(tag.GetMaterial().GetName())                      
                        newMaterialList.append(classesHelper.PolySelection("Base",[]))
                        exportData.allAWDBlocks[int(tag.GetMaterial().GetName())].data.textureTags.append(tag)
                        newMaterialList.append(tag)  
                        returnMats=[newMaterialList]
    if inherite==True and len(returnMats)==0:
        parentObj=curObj.GetUp()
        if parentObj is not None:
            returnMats=getMaterials(parentObj,allSelections,True,exportData)
            
    return returnMats
           

# get the materials applied to a mesh. if the mesh has no texture applied, the function will be executed for its Parent-Object, so we can read out the c4d-materials inheritage			
def getObjectColorMode(curObj,textureBaseMaterial,exportData):
    
    objColorMode=curObj[c4d.ID_BASEOBJECT_USECOLOR]   

    if int(objColorMode)==int(0): # ColorMode = OFF                                                   
        newMaterialList=[]
        newMaterialList.append(str(1))    
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                      
        newMaterialList.append(None)                                                                        
        if textureBaseMaterial is not None:
            newMaterialList=textureBaseMaterial
        return True, newMaterialList                                                                                 
        
    if int(objColorMode)==int(1): # ColorMode = AUTOMATIC      
        newMaterialList=[]
        newMaterialList.append(str(getObjectColorMatBlock(exportData,curObj[c4d.ID_BASEOBJECT_COLOR]).data.blockID))    
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                        
        newMaterialList.append(None)                                                                           
        if textureBaseMaterial is not None:
            newMaterialList=textureBaseMaterial
        return True, newMaterialList    
        
    if int(objColorMode)==int(2): # ColorMode = ON                                               
        newMaterialList=[]                                        
        newMaterialList.append(str(getObjectColorMatBlock(exportData,curObj[c4d.ID_BASEOBJECT_COLOR]).data.blockID))     
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                       
        newMaterialList.append(None)
        return False, newMaterialList                                                                                  
        
    if int(objColorMode)==int(3): # ColorMode = LAYER                                                                         
        newMaterialList=[]
        objLayerData=curObj.GetLayerData(exportData.doc)
        if objLayerData is not None:
            newMaterialList.append(str(getObjectColorMatBlock(exportData,objLayerData["color"]).data.blockID))   
        if objLayerData is None:
            newMaterialList.append(str(1))   
        newMaterialList.append(classesHelper.PolySelection("Base",[]))                                       
        newMaterialList.append(None)           
        return False, newMaterialList                                                                                    
