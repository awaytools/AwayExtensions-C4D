import c4d
from c4d import documents
import struct
from awdimporter import awdBlocks



def parseProperties(body): 
    attributeList=[]
    listLength=struct.unpack('I', body.read(4))[0]
    #print "attributes found = "+str(listLength)
    attributesCounter=0
    while attributesCounter<listLength:
		newAttribute=awdBlocks.BaseAttribute()
		newAttribute.attributeID=struct.unpack('H', body.read(2))[0]
		valueLength=struct.unpack('I', body.read(4))[0]
		newAttribute.attributeValue=body.read(valueLength)
		attributesCounter+=6+valueLength
    return

def parseVarString(body):  
    length=struct.unpack('H', body.read(2))[0]
    return body.read(length)
	
def parseSceneHeader(body,scale):  
    parentID=struct.unpack('I', body.read(4))[0]
    newMatrix=parseMatrix(body,scale,True,1)
    name=parseVarString(body)
    return parentID,newMatrix,name	
	
def createJointListRekursive(object,sceneData):     
    sceneData.latestjointList.append(object)     
    childCount=  len(object.GetChildren())
    while childCount>0:
		childCount-=1
		createJointListRekursive(object.GetChildren()[childCount],sceneData)
	
def replaceObjects(object,joint):     
    newJoint=joint.GetClone()  
    c4d.documents.GetActiveDocument().InsertObject(newJoint,object.GetUp(),object)     
    joint.Remove()  
    object.Remove()  
    return True	
  
def moveJoints(object,joint):     
    newJoint=joint.GetClone()  
    c4d.documents.GetActiveDocument().InsertObject(newJoint,object.GetUp(),object)     
    joint.Remove()   
    return True	
    
def parseMatrix(body,scale,normalize,skaleMatrix):  		
    vector1=c4d.Vector(float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]))
    vector2=c4d.Vector(float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]))
    vector3=c4d.Vector(float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]),float(struct.unpack('f', body.read(4))[0]))
    vectorOff=c4d.Vector(float(struct.unpack('f', body.read(4))[0])*float(scale),float(struct.unpack('f', body.read(4))[0])*float(scale),float(struct.unpack('f', body.read(4))[0])*float(scale))
    newMatrix=c4d.Matrix(vectorOff,vector1,vector2,vector3)
    if normalize==True:
		newMatrix.Normalize()
    #
    newMatrix.Scale(c4d.Vector(skaleMatrix))
    return newMatrix