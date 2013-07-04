
import c4d
import os
import math
import time
import struct
import zlib
import sys
from c4d import bitmaps, gui, plugins, utils, modules, documents

from xml.dom import minidom

import xml.dom.minidom as dom

from c4d.modules import character


from awdimporter import ids
from awdimporter import helpers
from awdimporter import parseObjects
from awdimporter import classesMain
from awdimporter import awdParser


sceneData=None
 
def importAWD(mainDialog):        
    global sceneData
    sceneData=classesMain.mainScene(mainDialog.GetReal(ids.REAL_SCALE),mainDialog.GetReal(ids.REAL_SCALE_JOINTS),0)
    sceneData.debug=mainDialog.GetBool(ids.CBOX_DEBUG)
    sceneData.skeletonTrannslations=mainDialog.GetBool(ids.CBOX_SKEL_ANIM_TRANSLATIONS)
    sceneData.skeletonTrannslationsRoot=mainDialog.GetBool(ids.CBOX_SKEL_ROOT_ANIM_TRANSLATIONS)
    sceneData.skeletonScales=mainDialog.GetBool(ids.CBOX_SKEL_ANIM_SCALE)
    sceneData.skeletonScalesRoot=mainDialog.GetBool(ids.CBOX_SKEL_ROOT_ANIM_SCALE)
    sceneData.skeletonTPoseRetarget=mainDialog.GetBool(ids.CBOX_SKEL_TPOSERETARGET)
    sceneData.texturesExternPathMode=mainDialog.GetLong(ids.COMBO_EXTERNTEXTURESPATH)
    sceneData.texturesEmbedPathMode=mainDialog.GetLong(ids.COMBO_EMBEDTEXTRESPATH)
    if sceneData.texturesExternPathMode==1 and c4d.documents.GetActiveDocument().GetDocumentPath()=="":
		print "Please save your c4d project before you use the document path = "+str(c4d.documents.GetActiveDocument().GetDocumentPath())
		return
    if sceneData.texturesExternPathMode==2 and mainDialog.GetString(ids.LINK_EXTERNTEXTURESPATH)=="" :
		print "Please choose a folder for external textures"
		return
    if (sceneData.texturesEmbedPathMode==1 or sceneData.texturesEmbedPathMode==2) and c4d.documents.GetActiveDocument().GetDocumentPath()=="":
		print "Please save your c4d project before you use the document path"
		return
    if sceneData.texturesEmbedPathMode==3 and mainDialog.GetString(ids.LINK_EMBEDTEXTRESPATH)=="" :
		print "Please choose a folder for embed textures"
		return
    objFile=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open *.AWD", c4d.FILESELECT_LOAD,"AWD")
    if sceneData.debug==True:
		print "File opened = "+str(objFile)
    if objFile==None:
		sceneData.errorMessages.append("No valid File selected")
		return
    if objFile!=None:
		f = open(objFile, 'rb')
		sceneData.path=os.path.dirname(objFile)
		if sceneData.texturesExternPathMode==0:
			sceneData.texturesExternPath=sceneData.path
		if sceneData.texturesExternPathMode==1:
			sceneData.texturesExternPath=c4d.documents.GetActiveDocument().GetDocumentPath()
		if sceneData.texturesExternPathMode==2:
			sceneData.texturesExternPath=mainDialog.GetString(ids.LINK_EXTERNTEXTURESPATH)
		if sceneData.texturesEmbedPathMode==0:
			sceneData.texturesEmbedPath=sceneData.path
		if sceneData.texturesEmbedPathMode==1:
			sceneData.texturesEmbedPath=c4d.documents.GetActiveDocument().GetDocumentPath()
		if sceneData.texturesEmbedPathMode==2:
			sceneData.texturesEmbedPath=os.path.join(c4d.documents.GetActiveDocument().GetDocumentPath(),"tex")
		if sceneData.texturesEmbedPathMode==3:
			sceneData.texturesEmbedPath=mainDialog.GetString(ids.LINK_EMBEDTEXTRESPATH)
		sceneData.magicString=f.read(3)

		if sceneData.magicString!="AWD":
			sceneData.errorMessages.append("The Magicstring is not 'AWD'!")
			return sceneData
		if sceneData.magicString=="AWD":
			sceneData.versionNumberMajor = struct.unpack('B', f.read(1))[0]
			sceneData.versionNumberMinor = struct.unpack('B', f.read(1))[0]
			sceneData.flags = struct.unpack('H', f.read(2))[0]
			sceneData.compression = struct.unpack('B', f.read(1))[0]
			sceneData.bodyLength = struct.unpack('I', f.read(4))[0]
			newBody =f
			if sceneData.compression ==1:
				#print "Compressed"
				d = zlib.decompressobj() 
				body=d.decompress(f.read(sceneData.bodyLength))+d.flush()
				newBody=open("test.dat","wb")
				newBody.write(body)
				newBody.close()
				newBody=open("test.dat","rb")
				newBody.seek(0)
			if sceneData.compression ==2:
				sceneData.errorMessages.append("LZMA Compression is not supported by this Importer!")
				return
				
			byteCounter=0
			newBody.seek(0, 2)
			newBodyLength=newBody.tell()
			newBody.seek(0, 0)
			if sceneData.compression ==0:
				byteCounter+=12
				newBody.seek(12)
			while byteCounter<newBodyLength:
				byteCounter+=awdParser.parseBlock(newBody,sceneData)
				byteCounter+=11
				if byteCounter>=newBodyLength:
					print "parsing done "+str(byteCounter)+" / "+str(newBodyLength)
		rootOBJCounter=0
		for rootOBJ in sceneData.rootObjects:
			if rootOBJCounter==0:
				c4d.documents.GetActiveDocument().SetActiveObject(rootOBJ,c4d.SELECTION_NEW)	
			if rootOBJCounter>0:
				c4d.documents.GetActiveDocument().SetActiveObject(rootOBJ,c4d.SELECTION_ADD)	
			rootOBJCounter+=1
		#print "Objects Importet = "+str(len(sceneData.blockDic))


    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.DrawViews( c4d.DA_ONLY_ACTIVE_VIEW|c4d.DA_NO_THREAD|c4d.DA_NO_REDUCTION|c4d.DA_STATICBREAK )
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED)
    c4d.EventAdd(c4d.EVENT_ANIMATE)
    return
	
