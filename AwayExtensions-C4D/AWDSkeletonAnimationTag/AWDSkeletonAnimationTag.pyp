#AWD Skeleton Animation Tag (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1028938    #ID for the tag

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

# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDSkeletonAnimationTagXpression(plugins.TagData):
    firstFrame=0
    lastFrame=50
    curRange=0
    def Init(self,node):
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(AWDSKELETON_EXPORT,True)
        bc.SetLong(COMBO_RANGE ,int(COMBO_RANGE_GLOBAL))
        node.SetData(bc)
        return True

    def Draw(self, tag, op, bd, bh): 
        if int( self.curRange)==COMBO_RANGE_CUSTOM:
            self.firstFram=tag.GetReal(REAL_FIRSTFRAME)
            self.lastFrame=tag.GetReal(REAL_LASTFRAME)
        return True
        
    # this function gets called for every Message the Tag recieves from C4D 
    def Message(self, node, type, data):
        if type==MSG_DESCRIPTION_CHECKUPDATE:
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
            else:
                if int( self.curRange)==COMBO_RANGE_CUSTOM:
                    self.firstFram=node.GetDataInstance().GetReal(REAL_FIRSTFRAME)
                    self.lastFrame=node.GetDataInstance().GetReal(REAL_LASTFRAME)
                
            print "Jes "+str(data)
            #print "Jes2 "+str(data["id"])
        #check if the Message was send from a Description-Dialog (such as this Tag)
        #print type
                    
        return True
        
        
    def GetDEnabling (self, node, id, t_data, flags, itemdesc):
        self.curRange=node.GetDataInstance().GetLong(COMBO_RANGE)
        curBool=True
        if int( self.curRange)==COMBO_RANGE_GLOBAL or int( self.curRange)==COMBO_RANGE_DOC or int( self.curRange)==COMBO_RANGE_PREVIEW:
            curBool=False
        testerString="("+str(REAL_FIRSTFRAME_STR)+", 12, 1028938)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_LASTFRAME_STR)+", 12, 1028938)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_FIRSTFRAME)+", 19, 1028938)"
        if str(id)==str(testerString):
            return curBool   
        testerString="("+str(REAL_LASTFRAME)+", 19, 1028938)"
        if str(id)==str(testerString):
            return curBool  
        #if the function has not returned False by now, the gui-element is set to be enabled by returning True
        return True
# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Skeleton Animation", g=AWDSkeletonAnimationTagXpression, description="AWDSkeletonAnimationTag", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)