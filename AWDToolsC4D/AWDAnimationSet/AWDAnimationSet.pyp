#AWD Skeleton Animation Tag (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1030508    #ID for the tag

AWDSKELETON_EXPORT        = 1010
AWDSKELETON_NAME          = 1011
COMBO_RANGE_GLOBAL        = 1021
COMBO_RANGE_DOC         = 1012
COMBO_RANGE_PREVIEW     = 1013
COMBO_RANGE_CUSTOM      = 1014
COMBO_RANGE             = 1015
COMBO_RANGE_STR         = 1016
REAL_FIRSTFRAME_STR     = 1017
REAL_FIRSTFRAME         = 1018
REAL_LASTFRAME_STR      = 1019
REAL_LASTFRAME          = 1020
LINK_TARGETOBJ          = 1050
CBX_CAPTUREDEFORMER     = 1051
STRING_KEYFRAMER        = 1052
CBOX_LOOP               = 1053
COMBO_ALLFRAMES         = 1054
COMBO_ALLFRAMES_ALL         = 1055
COMBO_ALLFRAMES_OBJECTKEYS   = 1056
COMBO_ALLFRAMES_TAGKEYS      = 1057
COMBO_ALLFRAMES_KEYNUM      = 1058
COMBO_ALLFRAMES_STR         = 1078
CBOX_STITCH             =1059
REAL_KEYFRAME_STR    = 1060
REAL_KEYFRAME         = 1061

# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDAnimationSetXpression(plugins.TagData):
    firstFrame=0
    lastFrame=50
    curRange=0
    curMode=1054
    def Init(self,node):
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(AWDSKELETON_EXPORT,True)
        bc.SetLong(COMBO_RANGE ,int(COMBO_RANGE_GLOBAL))
        bc.SetLong(COMBO_ALLFRAMES ,int(COMBO_ALLFRAMES_ALL))
        node.SetData(bc)
        return True

    def Draw(self, tag, op, bd, bh): 
        if int( self.curRange)==COMBO_RANGE_CUSTOM:
            pass#self.firstFrame=tag.GetReal(REAL_FIRSTFRAME)
            #self.lastFrame=tag.GetReal(REAL_LASTFRAME)
        return True
        
    # this function gets called for every Message the Tag recieves from C4D 
    def Message(self, node, type, data):
        if type==MSG_DESCRIPTION_CHECKUPDATE:
            bc=node.GetDataInstance()
            if bc.GetLink(LINK_TARGETOBJ) is not None:
                errorString=""
                if bc.GetLink(LINK_TARGETOBJ).GetType()!=c4d.Opolygon:
                    newObject=node.GetObject().GetClone()
                    doc=c4d.documents.GetActiveDocument()
                    doc.InsertObject(newObject)
                    bc.SetLink(LINK_TARGETOBJ,newObject)
                    newObject.Remove()
                    errorString="VertexAnimation can only target PolygonObjects!"
                if bc.GetLink(LINK_TARGETOBJ)==node.GetObject():
                    newObject=node.GetObject().GetClone()
                    doc=c4d.documents.GetActiveDocument()
                    doc.InsertObject(newObject)
                    bc.SetLink(LINK_TARGETOBJ,newObject)
                    newObject.Remove()
                    errorString="VertexAnimation cannot target itself!"
                if errorString!="":
                    c4d.gui.MessageDialog(errorString)
        
            if self.curMode!=node.GetDataInstance().GetLong(COMBO_ALLFRAMES):
                self.curMode=node.GetDataInstance().GetLong(COMBO_ALLFRAMES);
            if self.curRange==node.GetDataInstance().GetLong(COMBO_RANGE):
                if int( self.curRange)==COMBO_RANGE_CUSTOM:
                    self.firstFram=node.GetDataInstance().GetReal(REAL_FIRSTFRAME)
                    self.lastFrame=node.GetDataInstance().GetReal(REAL_LASTFRAME)
                    return True
            if self.curRange!=node.GetDataInstance().GetLong(COMBO_RANGE):
                bc=node.GetDataInstance()
                self.curRange=bc.GetLong(COMBO_RANGE) 
                   
                if int( self.curRange)==COMBO_RANGE_GLOBAL:
                    bc.SetReal(REAL_FIRSTFRAME ,int(0))
                    bc.SetReal(REAL_LASTFRAME ,int(0))
                        
                if int( self.curRange)==COMBO_RANGE_DOC:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                            
                        bc.SetReal(REAL_FIRSTFRAME ,int(doc.GetMinTime().GetFrame(doc.GetFps())))
                        bc.SetReal(REAL_LASTFRAME ,int(doc.GetMaxTime().GetFrame(doc.GetFps())))
                    if doc is None:
                        bc.SetReal(REAL_FIRSTFRAME ,int(0))
                        bc.SetReal(REAL_LASTFRAME ,int(0))
                            
                if int( self.curRange)==COMBO_RANGE_PREVIEW:
                    doc=c4d.documents.GetActiveDocument()
                    if doc is not None:
                        bc.SetReal(REAL_FIRSTFRAME ,int(doc.GetLoopMinTime().GetFrame(doc.GetFps())))
                        bc.SetReal(REAL_LASTFRAME ,int(doc.GetLoopMaxTime().GetFrame(doc.GetFps())))
                    if doc is None:
                        bc.SetReal(REAL_FIRSTFRAME ,int(0))
                        bc.SetReal(REAL_LASTFRAME ,int(0))
                            
                if int( self.curRange)==COMBO_RANGE_CUSTOM:
                    bc.SetReal(REAL_FIRSTFRAME ,int(self.firstFrame))
                    bc.SetReal(REAL_LASTFRAME ,int(self.lastFrame))
                    
                node.SetData(bc) 
                    
                
            #print "Jes2 "+str(data["id"])
        #check if the Message was send from a Description-Dialog (such as this Tag)
        #print type
                    
        return True
        
        
    def GetDEnabling (self, node, id, t_data, flags, itemdesc):
        testerString="("+str(CBOX_STITCH)+", 400006001, 1030484)"
        if str(id)==str(testerString):
            return False   
        testerString="("+str(CBOX_LOOP)+", 400006001, 1030484)"
        if str(id)==str(testerString):
            return False   
            
            
        self.curRange=node.GetDataInstance().GetLong(COMBO_RANGE)
        curBool=True
        if int( self.curRange)==COMBO_RANGE_GLOBAL or int( self.curRange)==COMBO_RANGE_DOC or int( self.curRange)==COMBO_RANGE_PREVIEW:
            curBool=False
        testerString="("+str(REAL_FIRSTFRAME_STR)+", 12, 1030484)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_LASTFRAME_STR)+", 12, 1030484)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_FIRSTFRAME)+", 19, 1030484)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_LASTFRAME)+", 19, 1030484)"
        if str(id)==str(testerString):
            return curBool 
            
        self.curMode=node.GetDataInstance().GetLong(COMBO_ALLFRAMES) 
        curBool2=True
        if self.curMode!=COMBO_ALLFRAMES_KEYNUM:
            curBool2=False
        testerString="("+str(REAL_KEYFRAME_STR)+", 12, 1030484)"
        if str(id)==str(testerString):
            return curBool2 
        testerString="("+str(REAL_KEYFRAME)+", 19, 1030484)"
        if str(id)==str(testerString):
            return curBool2 
        curBool3=True
        if int( self.curMode)!=COMBO_ALLFRAMES_TAGKEYS:
            curBool3=False
        testerString="("+str(STRING_KEYFRAMER)+", 130, 1030484)"
        if str(id)==str(testerString):
            return curBool3  
        #if the function has not returned False by now, the gui-element is set to be enabled by returning True
        return True
# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD AnimationSet", g=AWDAnimationSetXpression, description="AWDAnimationSet", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)