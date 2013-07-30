# functions that will run inside the background-worker-thread


import c4d
import copy
import struct
import os
import zlib
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import mainMaterials

                        
def addToExportList(exportData,awdBlock):
    if awdBlock.isReordered==True:
        return awdBlock.saveBlockID
    if awdBlock.isReordered==False:
        if awdBlock.tagForExport==True:
            if awdBlock.blockType==254:#NameSpace
                pass#doThis=True
            if awdBlock.blockType==255:#metadata
                pass#doThis=True    
            if awdBlock.blockType==1:
                pass#triangel
            if awdBlock.blockType==11:
                pass#primitive
            if awdBlock.blockType==21:
                pass#scene       
            if awdBlock.blockType==22:#container
                parentBlock=exportData.allAWDBlocks[int(awdBlock.data.dataParentBlockID)]
                if parentBlock is not None:
                    awdBlock.data.dataParentBlockID=addToExportList(exportData,parentBlock)
                    
            if awdBlock.blockType==23:#meshinstance
                parentBlock=exportData.allAWDBlocks[int(awdBlock.data.dataParentBlockID)]
                if parentBlock is not None:
                    awdBlock.data.dataParentBlockID=addToExportList(exportData,parentBlock)
                geoBlock=exportData.allAWDBlocks[int(awdBlock.data.geoBlockID)]
                if geoBlock is not None:
                    awdBlock.data.saveGeoBlockID=addToExportList(exportData,geoBlock)           
                awdBlock.data.saveMaterials2=[]
                print str((awdBlock.data.saveGeoBlockID))+"   geoBlock.saveSubMeshes"
                for mat in awdBlock.data.saveMaterials:
                    matBlockID=addToExportList(exportData,exportData.allAWDBlocks[int(mat)])
                    awdBlock.data.saveMaterials2.append(matBlockID)
                    #print "awdBlock.saveMaterials2 = "+str(awdBlock.saveMaterials2)
                      
            if awdBlock.blockType==41:#light
                parentBlock=exportData.allAWDBlocks[int(awdBlock.data.dataParentBlockID)]
                if parentBlock is not None:
                    awdBlock.data.dataParentBlockID=addToExportList(exportData,parentBlock)
                    
            if awdBlock.blockType==42:#camera
                parentBlock=exportData.allAWDBlocks[int(awdBlock.data.dataParentBlockID)]
                
            if awdBlock.blockType==51:#lightPicker
                exportData.lightPickerCounter+=1
                awdBlock.data.name+=str(exportData.lightPickerCounter)
                for light in awdBlock.data.lightList:
                    lightID=addToExportList(exportData,exportData.allAWDBlocks[int(light)])
                    awdBlock.data.saveLightList.append(lightID)
                
            if awdBlock.blockType==81:#material
                
                lightPickerBlock=exportData.allAWDBlocks[int(awdBlock.data.lightPicker)]
                if lightPickerBlock is not None:
                    awdBlock.data.saveMatProps.append(22)
                    awdBlock.data.lightPickerID=addToExportList(exportData,lightPickerBlock)
                if awdBlock.data.isCreated==False and awdBlock.data.colorMat==False:
                    awdBlock.data.isCreated=True                
                    mainMaterials.createMaterial(awdBlock.data,exportData)
                if awdBlock.data.saveMatType==2:
                    textureBlock=exportData.allAWDBlocks[int(awdBlock.data.saveColorTextureID)]
                    if textureBlock is not None:
                        awdBlock.data.saveColorTextureID=addToExportList(exportData,textureBlock)
                    normalTextureBlock=exportData.allAWDBlocks[int(awdBlock.data.saveNormalTextureID)]
                    if normalTextureBlock is not None:
                        awdBlock.data.saveNormalTextureID=addToExportList(exportData,normalTextureBlock)
                    ambientTextureBlock=exportData.allAWDBlocks[int(awdBlock.data.saveAmbientTextureID)]
                    if ambientTextureBlock is not None:
                        awdBlock.data.saveAmbientTextureID=addToExportList(exportData,ambientTextureBlock)
                    specTextureBlock=exportData.allAWDBlocks[int(awdBlock.data.saveSpecTextureID)]
                    if specTextureBlock is not None:
                        awdBlock.data.saveSpecTextureID=addToExportList(exportData,specTextureBlock)
                
            if awdBlock.blockType==82:#texture
                pass
            if awdBlock.blockType==83:#cubetexture
                pass#      awdBlock.dataParentBlockID=addToExportList(exportData,parentBlock)                    
            if awdBlock.blockType==101:#skeleton
                pass
            if awdBlock.blockType==102:#skeletonpose
                pass
            if awdBlock.blockType==103:#skeletonanimation
                for pose in awdBlock.data.framesIDSList:
                    awdBlock.data.framesIDSList2.append(addToExportList(exportData,pose))
            if awdBlock.blockType==121:#uvanimation
                pass
            if awdBlock.blockType==111:#VertexState
                targetMesh=exportData.allAWDBlocks[int(awdBlock.data.targetMesh)]
                if targetMesh is not None:
                    awdBlock.data.saveTargetMesh=addToExportList(exportData,targetMesh)

            if awdBlock.blockType==112:#VertexAnimation
                targetMesh=exportData.allAWDBlocks[int(awdBlock.data.targetMesh)]
                if targetMesh is not None:
                    awdBlock.data.saveTargetMesh=addToExportList(exportData,targetMesh)
                    
            if awdBlock.blockType==113:#AnimationSet
                awdBlock.data.saveTargetMesh=addToExportList(exportData,awdBlock.data.targetMesh)
                geoBlock=exportData.allAWDBlocks[int(awdBlock.data.targetMesh.data.geoBlockID)]
                if len(geoBlock.data.saveSubMeshes[0].weightsBuffer)>0:
                    awdBlock.data.jointsPerVert=len(geoBlock.data.saveSubMeshes[0].weightsBuffer)/(len(geoBlock.data.saveSubMeshes[0].vertexBuffer)/3)
                print "AnimationNodes in Set = "+str(len(geoBlock.data.saveSubMeshes[0].weightsBuffer))
                print "AnimationNodes in Set = "+str(len(geoBlock.data.saveSubMeshes[0].vertexBuffer))
                print "AnimationNodes in Set = "+str(awdBlock.data.jointsPerVert)
                for anim in awdBlock.data.poseBlockIDs:
                    awdBlock.data.savePoseBlockIDs.append(addToExportList(exportData,anim))
             
            if awdBlock.blockType==122:#Animator
                awdBlock.data.saveMeshID=addToExportList(exportData,awdBlock.data.targetMeshBlock)
                awdBlock.data.saveAnimSetID=addToExportList(exportData,awdBlock.data.animSetBlock)
                print "awdBlock.data.skeleton "+str(awdBlock.data.skeleton)
                if awdBlock.data.skeleton is not None:
                    print "awdBlock.data.skeleton "+str(awdBlock.data.skeleton)
                    awdBlock.data.saveSkeletonID=addToExportList(exportData,awdBlock.data.skeleton)
                print "awdBlock.data.saveSkeletonID "+str(awdBlock.data.saveSkeletonID)
                #awdBlock.saveSkeletonID=addToExportList(exportData,exportData.skeleton)
                        
            print "Reordered Block type = "+str(awdBlock.blockType)+"  /  "+  str(awdBlock.data) 
            awdBlock.saveBlockID=int(len(exportData.allSaveAWDBlocks))
            awdBlock.isReordered=True
            awdBlock.data.saveBlockID=awdBlock.saveBlockID
            exportData.allSaveAWDBlocks.append(awdBlock.data)
            return awdBlock.saveBlockID