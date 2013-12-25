# some helper-functions for the part of the export process running in the c4d-mainthread

import c4d
import os
from awdexporter import ids
from awdexporter import classesHelper
from awdexporter import classesAWDBlocks

       
        
def createMaterial(newAWDBlock,exportData):
    
    material=newAWDBlock.mat
    newAWDBlock.tagForExport=True 
    if material[c4d.MATERIAL_USE_TRANSPARENCY]==True:
        newAWDBlock.matAlpha=1.0-material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS]
        newAWDBlock.saveMatProps.append(10)   
    if material[c4d.MATERIAL_USE_COLOR]==True:
        colorVec=material[c4d.MATERIAL_COLOR_COLOR]
        newAWDBlock.matColor=[colorVec.z*255,colorVec.y*255,colorVec.x*255,0]
        newAWDBlock.saveMatProps.append(1)             
        if(material[c4d.MATERIAL_COLOR_SHADER]):
            if material[c4d.MATERIAL_COLOR_SHADER].GetType() == c4d.Xbitmap:
                createSingleTextureBlock(exportData,str(material[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]))
                colorTexBlock=exportData.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_COLOR_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                if colorTexBlock is not None:
                    if colorTexBlock.isOK:
                        newAWDBlock.saveMatType=2
                        newAWDBlock.saveMatProps.append(2)
                        newAWDBlock.saveColorTextureID=colorTexBlock.blockID
            else:
                print "only supported shaders are bitmapshader!"
                #exportData.AWDwarningObjects.append("
    if(material[c4d.MATERIAL_USE_NORMAL]):            
        if(material[c4d.MATERIAL_NORMAL_SHADER]):
            if material[c4d.MATERIAL_NORMAL_SHADER].GetType() == c4d.Xbitmap:
                createSingleTextureBlock(exportData,str(material[c4d.MATERIAL_NORMAL_SHADER][c4d.BITMAPSHADER_FILENAME]))
                newTexBlock=exportData.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_NORMAL_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                if newTexBlock is not None:
                    if newTexBlock.isOK:
                        newTexBlock.tagForExport=True
                        newAWDBlock.saveMatProps.append(3)
                        newAWDBlock.saveNormalTextureID=newTexBlock.blockID      
            else:
                print "only supported shaders are bitmapshader!"    
    if(material[c4d.MATERIAL_USE_DIFFUSION]): # for now  use the diffuse tex as specularMap       
        if(material[c4d.MATERIAL_DIFFUSION_SHADER]):
            if material[c4d.MATERIAL_DIFFUSION_SHADER].GetType() == c4d.Xbitmap:
                createSingleTextureBlock(exportData,str(material[c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME]))
                newTexBlock=exportData.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_DIFFUSION_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                newTexBlock.tagForExport=True 
                if newTexBlock is not None:
                    if newTexBlock.isOK:
                        newTexBlock.tagForExport=True
                        newAWDBlock.saveMatProps.append(21)
                        newAWDBlock.saveSpecTextureID=newTexBlock.blockID  
            else:
                print "only supported shaders are bitmapshader!"
    if(material[c4d.MATERIAL_USE_SPECULARCOLOR]):            
        if(material[c4d.MATERIAL_SPECULAR_SHADER]):
            if material[c4d.MATERIAL_SPECULAR_SHADER].GetType() == c4d.Xbitmap:
                createSingleTextureBlock(exportData,str(material[c4d.MATERIAL_SPECULAR_SHADER][c4d.BITMAPSHADER_FILENAME]))
                newTexBlock=exportData.texturePathToAWDBlocksDic.get(str(material[c4d.MATERIAL_SPECULAR_SHADER][c4d.BITMAPSHADER_FILENAME]),None)
                newTexBlock.tagForExport=True
                if newTexBlock is not None:
                    if newTexBlock.isOK:
                        newTexBlock.tagForExport=True
                        newAWDBlock.saveMatProps.append(17)
                        newAWDBlock.saveAmbientTextureID=newTexBlock.blockID  
            else:
                print "only supported shaders are bitmapshader!"
                                
              
    if(material[c4d.MATERIAL_USE_FOG]):  
        pass# add fog-method
    if(material[c4d.MATERIAL_USE_SPECULAR]):  
        pass
    if(material[c4d.MATERIAL_USE_GLOW]):
        pass
        #print "material build: awdBlockid= "+str(material[c4d.MATERIAL_TRANSPARENCY_BRIGHTNESS])

def createSingleTextureBlock(exportData,texturePath):
    if texturePath is None or str(texturePath)=="":
        return
    isInList=exportData.texturePathToAWDBlocksDic.get(str(texturePath),None)
    if isInList is None:
        pathName=os.path.basename(texturePath)
        
        newAWDWrapperBlock=classesAWDBlocks.WrapperBlock(None,"",82)
        exportData.allAWDBlocks.append(newAWDWrapperBlock) 
        
        newAWDBlock=classesAWDBlocks.TextureBlock(exportData.idCounter,0,str(texturePath),exportData.embedTextures,pathName)
        
        exportData.texturePathToAWDBlocksDic[str(texturePath)]=newAWDBlock
        exportData.idCounter+=1
        extensionAr=pathName.split(".")
        extension=extensionAr[(len(extensionAr)-1)]
        filenamecount=0 
        newAWDBlock.saveLookUpName=""
        newAWDBlock.tagForExport=True
        newAWDBlock.isOK=False
        while filenamecount<(len(extensionAr)-1):
            newAWDBlock.saveLookUpName+=extensionAr[filenamecount]
            filenamecount+=1

        #if extension!="jpg" and extension!="jpeg" and extension!="JPG" and extension!="JPEG" and extension!="png" and extension!="PNG":
        #    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE3,texturePath))
        #    return
        inDocumentPath=texturePath
        try:
            with open(texturePath) as f: pass
        except IOError as e:
            try:
                inDocumentPath=os.path.join(c4d.documents.GetActiveDocument().GetDocumentPath(),texturePath)
                with open(inDocumentPath) as f: pass
            except IOError as e:
                try:
                    inDocumentPath=os.path.join(c4d.documents.GetActiveDocument().GetDocumentPath(),"tex",texturePath)
                    with open(inDocumentPath) as f: pass
                except IOError as e:
                    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE4,inDocumentPath))
                    return
                    
               
        curBmp = c4d.bitmaps.BaseBitmap()
        result, ismovie = curBmp.InitWith(str(inDocumentPath))
        if result==c4d.IMAGERESULT_NOTEXISTING:
            print "Image loade NOTEXISTING"
        if result==c4d.IMAGERESULT_WRONGTYPE:
            print "Image loade WRONGTYPE"
        if result==c4d.IMAGERESULT_OUTOFMEMORY:
            print "Image loade OUTOFMEMORY"
        if result==c4d.IMAGERESULT_FILEERROR:
            print "Image loade FILEERROR"
        if result==c4d.IMAGERESULT_FILESTRUCTURE:
            print "Image loade FILESTRUCTURE"
        if result==c4d.IMAGERESULT_MISC_ERROR:
            print "Image loade MISC_ERROR"
        if result==c4d.IMAGERESULT_PARAM_ERROR:
            print "Image loade PARAM_ERROR"
        if result==c4d.IMAGERESULT_OK: #int check
            #print "Image loadet OK"
            # picture loaded
            if ismovie==True: #bool check
                print "Texture is Movie...There is no movie suupport in AWD..."
            else:
                validWidth, validHeight=checkTextureForPowerOfTwo(curBmp)  #pass # file is a movie
                if validWidth!=True and validHeight!=True:
                    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE5,inDocumentPath))
                    return
                if validWidth!=True:
                    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE5,inDocumentPath))
                    return
                if validHeight!=True:
                    exportData.AWDerrorObjects.append(classesHelper.AWDerrorObject(ids.ERRORMESSAGE5,inDocumentPath))
                    return
                hasAlpha=curBmp.GetInternalChannel()
                fileType="jpg"
                fileFormat=c4d.FILTER_JPG
                if hasAlpha is not None:
                    fileType="png"
                    fileFormat=c4d.FILTER_PNG
                fileName=str(newAWDBlock.saveLookUpName)+"."+str(fileType)
                filePath=os.path.dirname(exportData.datei)
                inDocumentPath=os.path.join(filePath,fileName)  
                didExist=False
                try:
                    with open(inDocumentPath) as f: didExist=True
                except IOError as e:    
                    pass
                
                #f = open(inDocumentPath, 'wb')    
                saveResult=curBmp.Save(inDocumentPath,fileFormat,savebits=c4d.SAVEBIT_ALPHA)
                if saveResult==c4d.IMAGERESULT_OK:
                    #print "ImageSave OK"
                    if exportData.embedTextures==0:                     # if the texture should be embed in the awd file:
                        texturefile=open(str(inDocumentPath),"rb")          # if the function has not returned yet, the 'inDocumentPath' points to a valid file, so we open this file
                        newAWDBlock.saveTextureData=texturefile.read()      # we just read all the bits of the file into a the bytestring 'saveTextureData'    
                        texturefile.close()
                        if didExist!=True:
                            os.remove(str(inDocumentPath))
                    newAWDWrapperBlock.tagForExport=True
                    newAWDWrapperBlock.data=newAWDBlock
                    
                newAWDBlock.isOK=True
                if saveResult==c4d.IMAGERESULT_NOTEXISTING:
                    newAWDBlock.isOK=False
                    print "ImageSave NOTEXISTING"
                if saveResult==c4d.IMAGERESULT_WRONGTYPE:
                    newAWDBlock.isOK=False
                    print "ImageSave WRONGTYPE"
                if saveResult==c4d.IMAGERESULT_OUTOFMEMORY:
                    newAWDBlock.isOK=False
                    print "ImageSave OUTOFMEMORY"
                if saveResult==c4d.IMAGERESULT_FILEERROR:
                    newAWDBlock.isOK=False
                    print "ImageSave FILEERROR"
                if saveResult==c4d.IMAGERESULT_FILESTRUCTURE:
                    newAWDBlock.isOK=False
                    print "ImageSave FILESTRUCTURE"
                if saveResult==c4d.IMAGERESULT_MISC_ERROR:
                    newAWDBlock.isOK=False
                    print "ImageSave MISC_ERROR"
                if saveResult==c4d.IMAGERESULT_PARAM_ERROR:
                    newAWDBlock.isOK=False
                    print "ImageSave PARAM_ERROR"
                #f.close()

# checks if width and height of a texture is in 'power of two'
# returns two boolean values (width/height)
def checkTextureForPowerOfTwo(curBmp):
    w, h = curBmp.GetSize()
    returnerW = True
    returnerH = True
    if int(w)!=int(2) and int(w)!=int(4) and int(w)!=int(8) and int(w)!=int(16) and int(w)!=int(32) and int(w)!=int(64) and int(w)!=int(128) and int(w)!=int(256) and int(w)!=int(512) and int(w)!=int(1024) and int(w)!=int(2048):
        returnerW=False
    if int(h)!=int(2) and int(h)!=int(4) and int(h)!=int(8) and int(h)!=int(16) and int(h)!=int(32) and int(h)!=int(64) and int(h)!=int(128) and int(h)!=int(256) and int(h)!=int(512) and int(h)!=int(1024) and int(h)!=int(2048):
        returnerH=False
    return returnerW, returnerH
   