# runs in the c4d main thread

# some functions and one class to read out the c4d-light-routing (which object/material is lit by which lights)
# the awd2 file-format is not yet ready to transport this information, but it might by in the future. (and we are ready for that).

from xml.dom import minidom
import xml.dom.minidom as dom
import os
import c4d
from c4d import documents
from xml.sax.saxutils import unescape
from awdexporter import ids
from awdexporter import classesAWDBlocks



def saveLightXML(exportData):
    if len(exportData.allLightBlocks)==0:
        return
    if len(exportData.lightPickerList)==0:
        return
    openLightDatStr="<lightsdata>\n"
    closeLightDataStr="</lightsdata>\n"
    openLightsStr="    <lights>\n"
    closeLightsStr="    </lights>\n"
    openLightStr="        <light>\n"
    closeLightStr="        </light>\n"
    
    outputStr="<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    outputStr+="<!-- SceneLightDescription C4D to Prefab3D v2, C4D-Exporter = Robin Lockhart (80prozent@ifferentdesign.de) // Prefab = Fabrice closier, 2013, www.closier.nl/prefab -->\n"
    outputStr+=openLightDatStr
    outputStr+=openLightsStr
    for lightBlock in exportData.allLightBlocks:
        outputStr+=openLightStr
        outputStr+="            <id><![CDATA["+str(lightBlock.name)+"_"+str(lightBlock.sceneObject.GetName())+"]]></id>\n"  
        
        colorVec=lightBlock.sceneObject[c4d.LIGHT_COLOR]
        outputStr+="            <color>"+str(int(255*colorVec.x))+","+str(int(255*colorVec.y))+","+str(int(255*colorVec.z))+"</color>\n"
        outputStr+="            <ambientColor>"+str(int(255*colorVec.x))+","+str(int(255*colorVec.y))+","+str(int(255*colorVec.z))+"</ambientColor>\n"
        
        lightStrength=lightBlock.sceneObject[c4d.LIGHT_BRIGHTNESS]
        mainBool=lightBlock.sceneObject[c4d.LIGHT_NOLIGHTRADIATION]
        if str(mainBool)==str(1):
            lightStrength=0
            
        diffuseValue=0
        diffuseBool=lightBlock.sceneObject[c4d.LIGHT_DETAILS_DIFFUSE]
        if str(diffuseBool)==str(1):
            diffuseValue=lightStrength
            
        outputStr+="            <diffuse>"+str(diffuseValue)+"</diffuse>\n"
        specularBool=lightBlock.sceneObject[c4d.LIGHT_DETAILS_SPECULAR]
        specularValue=0
        if str(specularBool)==str(1):
            specularValue=lightStrength
        outputStr+="            <specular>"+str(specularValue)+"</specular>\n"
        ambientBool=lightBlock.sceneObject[c4d.LIGHT_DETAILS_AMBIENT]
        ambientValue=0
        if str(ambientBool)==str(1):
            ambientValue=lightStrength
        outputStr+="            <ambient>"+str(ambientValue)+"</ambient>\n"
        
        lightType="pointlight"
        positionVec=lightBlock.sceneObject.GetMg().off
        directionVec=c4d.Vector(1,0,0)
        if lightBlock.lightType==1:
            lightType="directionallight"            
            directionVec=lightBlock.sceneObject.GetAbsRot()
            directionVec.x*=-1
            directionVec.Normalize()    
        
        
        outputStr+="            <type><![CDATA["+str(lightType)+"]]></type>\n"
        outputStr+="            <max>true</max>\n"
        
        outputStr+="            <x>"+str(positionVec.x)+"</x>\n"
        outputStr+="            <y>"+str(positionVec.y)+"</y>\n"
        outputStr+="            <z>"+str(positionVec.z)+"</z>\n"
        outputStr+="            <radius>"+str(lightBlock.sceneObject[c4d.LIGHT_DETAILS_INNERDISTANCE])+"</radius>\n"
        falloff=str(lightBlock.sceneObject[c4d.LIGHT_DETAILS_OUTERDISTANCE])
        if lightBlock.sceneObject[c4d.LIGHT_DETAILS_FALLOFF]==0:
            falloff=999999
        outputStr+="            <fallOff>"+str(falloff)+"</fallOff>\n"
        outputStr+="            <direction>"+str(directionVec.x)+","+str(directionVec.y)+","+str(directionVec.z)+"</direction>\n"
        outputStr+=closeLightStr
        
    outputStr+=closeLightsStr
    outputStr+="\n"
    openlightPickersStr="    <lightPickers>\n"
    closelightPickersStr="    </lightPickers>\n"
    openStaticLightPickerStr="        <StaticLightPicker>\n"
    closeStaticLightPickerStr="        </StaticLightPicker>\n"
    outputStr+=openlightPickersStr
    outputStr+=openStaticLightPickerStr
    lightPickerCnt=1
    while lightPickerCnt<len(exportData.lightPickerList):        
        outputStr+="            <name><![CDATA[lightPicker0]]></name>\n"
        nameListStr=""
        #print "lights to export = "+str(exportData.lightPickerList[lightPickerCnt].lights)
        nameCnt=0
        for name in exportData.lightPickerList[lightPickerCnt].lightList:
            getAwdBlock=exportData.allAWDBlocks[int(name)]
            if nameCnt>0:
                nameListStr+=","
            nameListStr+=str(getAwdBlock.name)+"_"+str(getAwdBlock.sceneObject.GetName())
            nameCnt+=1
            
        outputStr+="            <lightIds><![CDATA["+str(nameListStr)+"]]></lightIds>\n"
        lightPickerCnt+=1
        
    outputStr+=closeStaticLightPickerStr
    outputStr+=closelightPickersStr
    
    outputStr+=closeLightDataStr
            
    filePath=os.path.dirname(exportData.datei)
    fileNameOriginal=os.path.basename(exportData.datei)
    fileName1=fileNameOriginal.split(".")
    fileName=""
    fileNameCnt=0
    while fileNameCnt<len(fileName1)-1:
        fileName+=fileName1[fileNameCnt]
        fileNameCnt+=1
        
        
        
    testString="<!>"
    fileName+="_sceneLight.xml"
    datei=os.path.join(filePath,fileName)  
    #unescape(str_object_xml)
    f = open(datei, 'wb')
    
    f.write(outputStr)
    f.close()	
    return True

class LightRouter(object):
    def __init__(self):
        self.name = "NoLights"
        self.lights = []
        
def getObjectLights(curObj,exportData):
    objLightsList=[]
    curName=curObj.GetName()
    for lightObj in exportData.allLights:
        inorExluded=lightObj[2].get(str(curObj.GetName()),None)
        if inorExluded is not None:
            if inorExluded==True:
                objLightsList.append(lightObj[0])
    newLightsList=[]
    lightPickerString=""
    while len(objLightsList)>0:
        findSmallestName=1000000
        findSmallestNameIdx=-1
        nameIdx=0
        for curName in objLightsList:
            if int(curName)<int(findSmallestName):
                findSmallestName=int(curName)
                findSmallestNameIdx=nameIdx
            nameIdx+=1
        if findSmallestNameIdx!=-1:            
            newLightsList.append(findSmallestName)
            objLightsList.pop(findSmallestNameIdx)
            lightPickerString+=str(findSmallestName)+"#"
        if findSmallestNameIdx==-1:  
            print "Error in Lightrouting"
            objLightsList=[]
            newLightsList=[]
            lightPickerString=""
    returnIdx=0
    if len(exportData.lightPickerDic)==0:
        newAWDBlock=classesAWDBlocks.LightPickerBlock(exportData.idCounter,0,[])
        exportData.allAWDBlocks.append(newAWDBlock)
        exportData.idCounter+=1
        exportData.lightPickerDic[str("")]=0
        exportData.lightPickerList.append(newAWDBlock)
    if lightPickerString!="":
        getLightPicker=exportData.lightPickerDic.get(str(lightPickerString),None)
        if getLightPicker is not None:
            returnIdx=getLightPicker
        if getLightPicker is None:
            newAWDBlock=classesAWDBlocks.LightPickerBlock(exportData.idCounter,0,newLightsList)
            newAWDBlock.name="LightPicker "+str(len(exportData.lightPickerList))
            exportData.allAWDBlocks.append(newAWDBlock)
            exportData.idCounter+=1
            exportData.lightPickerList.append(newAWDBlock)
            exportData.lightPickerDic[str(lightPickerString)]=len(exportData.lightPickerList)
            returnIdx=len(exportData.lightPickerList)
            
        
    return returnIdx
    
        
def addAllObjectsToLightList(curObjList,lightList,exOrInclude):
    #print curObjList
    if curObjList is not None:
        for curObj in curObjList:
            lightList[str(curObj.GetName())]=exOrInclude
            addAllObjectsToLightList(curObj.GetChildren(),lightList,exOrInclude)
        
        
def readAllLightRouting(curObj,exportData):
    
    if curObj.GetType() == c4d.Olight:
        read_light_routing(curObj,exportData)
        if len(curObj.GetChildren())==0:
            return False, False
    for child in curObj.GetChildren():
        readAllLightRouting(child,exportData)

def read_light_routing(curObj,exportData):
    lightType="unsupported"
    if curObj[c4d.LIGHT_TYPE]==0:
        lightType="Point"
    if curObj[c4d.LIGHT_TYPE]==3:
        lightType="Directional"
    if lightType!="unsupported":
        objCount=0
        lightObjectDic={}
        exOrIncluded=True
        exOrIncludedOpposite=False
        if curObj[c4d.LIGHT_EXCLUSION_MODE]==1:
            #print "mode = exlude"
            exOrIncluded=False
            exOrIncludedOpposite=True
            
        addAllObjectsToLightList(exportData.doc.GetObjects(),lightObjectDic,exOrIncludedOpposite)    
            
        while objCount < curObj[c4d.LIGHT_EXCLUSION_LIST].GetObjectCount():
            thisObj=curObj[c4d.LIGHT_EXCLUSION_LIST].ObjectFromIndex(exportData.doc,objCount)
            if thisObj is not None :
                lightObjectDic[str(thisObj.GetName())]=exOrIncluded
                if curObj[c4d.LIGHT_EXCLUSION_LIST].GetFlags(objCount)>7:
                    for child1 in thisObj.GetChildren():
                        self.read_light_routing_recursiv(child1,lightObjectDic,exOrIncluded)
            objCount+=1
        newlightObject=[]
        newlightObject.append(curObj.GetName())
        newlightObject.append(exOrIncluded)
        newlightObject.append(lightObjectDic)
        exportData.allLights.append(newlightObject)
    
def read_light_routing_recursiv(self,curObj,lightObjectDic,exOrIncluded):
    lightObjectDic[str(curObj.GetName())]=exOrIncluded
    for child in curObj.GetChildren():
        self.read_light_routing_recursiv(child,lightObjectDic,exOrIncluded)   