import c4d
from c4d import documents
import struct

import zlib


import c4d
from c4d import documents
import struct
from awdimporter import awdBlocks
from awdimporter import parseObjects



def parseBlock(body,sceneData): 
    newBlock=awdBlocks.BaseBlock(struct.unpack('I', body.read(4))[0],struct.unpack('B', body.read(1))[0],struct.unpack('B', body.read(1))[0],struct.unpack('B', body.read(1))[0],struct.unpack('I', body.read(4))[0])
    sceneData.blockDic[str(newBlock.blockID)]=newBlock
    if sceneData.debug==True:
        print " "
        print "blockID= "+str(newBlock.blockID)
        print "nameSpace= "+str(newBlock.nameSpace)
        print "blockType= "+str(newBlock.blockType)
        print "blockFlags= "+str(newBlock.blockFlags)
        print "blockSize= "+str(newBlock.blockSize)
    
    if newBlock.nameSpace==0:
        newBlock.blockDataObject=parseAWDBlock(newBlock,body, sceneData)
        #print "sceneDate.Geodict = "+str(len(sceneData.geoDic))
    if newBlock.nameSpace!=0:
        if sceneData.debug==True:
            print "found a block with other namespace than awd"
        body.read(newBlock.blockSize)
    return (newBlock.blockSize)


def parseAWDBlock(newBlock,body,sceneData):
    isParsed=False
    returnBlock=None

    if newBlock.blockType==1:
        isParsed=True
        returnBlock=parseObjects.parseTriangleGeometryBlock(body, newBlock,sceneData)
    if newBlock.blockType==11:
        isParsed=True
        returnBlock=parseObjects.parsePrimitiveGeometryBlock(body, newBlock,sceneData)
    if newBlock.blockType==21:
        isParsed=True
        returnBlock=parseObjects.parseSceneBlock(body, newBlock,sceneData)
    if newBlock.blockType==22:
        isParsed=True
        returnBlock=parseObjects.parseContainerBlock(body, newBlock,sceneData)
    if newBlock.blockType==23:
        isParsed=True
        returnBlock=parseObjects.parseMeshInstanceBlock(body, newBlock,sceneData)
    if newBlock.blockType==41:
        isParsed=True
        returnBlock=parseObjects.parseLightBlock(body, newBlock,sceneData)
    if newBlock.blockType==42:
        isParsed=True
        returnBlock=parseObjects.parseCameraBlock(body, newBlock,sceneData)
    if newBlock.blockType==81:
        isParsed=True
        returnBlock=parseObjects.parseStandartMaterialBlock(body, newBlock,sceneData)
    if newBlock.blockType==82:
        isParsed=True
        returnBlock=parseObjects.parseTextureBlock(body, newBlock,sceneData)
    if newBlock.blockType==83:
        isParsed=True
        returnBlock=parseObjects.parseCubeTextureBlock(body, newBlock,sceneData)
    if newBlock.blockType==101:
        isParsed=True
        returnBlock=parseObjects.parseSkeletonBlock(body, newBlock,sceneData)
    if newBlock.blockType==102:
        isParsed=True
        returnBlock=parseObjects.parseSkeletonPoseBlock(body, newBlock,sceneData)
    if newBlock.blockType==103:
        isParsed=True
        returnBlock=parseObjects.parseSkeletonAnimationBlock(body, newBlock,sceneData)
    if newBlock.blockType==121:
        isParsed=True
        returnBlock=parseObjects.parseUVAnimationBlock(body, newBlock,sceneData)
    if newBlock.blockType==254:
        isParsed=True
        returnBlock=parseObjects.parseNameSpaceBlock(body, newBlock,sceneData)
    if newBlock.blockType==255:
        isParsed=True
        returnBlock=parseObjects.parseMetaDataBlock(body, newBlock,sceneData)
    if isParsed==False:
        if sceneData.debug==True:
            print "AWD Block could not be parsed"
        returnBlock=body.read(newBlock.blockSize)
    return returnBlock
