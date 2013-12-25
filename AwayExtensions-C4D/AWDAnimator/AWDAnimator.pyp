#AWDAnimator (c) 2013 80prozent[a]differentdesign.de

from c4d import gui, bitmaps

import c4d
import c4d.documents
from c4d import *
from c4d import plugins, bitmaps, utils
import os, math

PLUGIN_ID = 1030509    #ID for the tag


ANIMATOR_EXPORT= 1010
ANIMATOR_NAME = 1011
LINK_TARGETOBJ= 1012
LINK_TARGETSTATE= 1013
LINK_SKELETON= 1018
CBOX_AUTOPLAY= 1014
REAL_STARTTIME= 1015
REAL_STARTTIME_STR= 1016
BTN_SETSTARTTIME= 1017

# +++++++++++++++ The plugin tag ++++++++++++++++++++++++++++++

class AWDAnimatorXpression(plugins.TagData):
    firstFrame=0
    lastFrame=50
    curRange=0
    curMode=1054
    def Init(self,node):
        bc = node.GetDataInstance()# Reads the tag's container and opens a copy.
        bc.SetBool(ANIMATOR_EXPORT,True)
        node.SetData(bc)
        return True

    def Draw(self, tag, op, bd, bh): 
        return True
        
    # this function gets called for every Message the Tag recieves from C4D 
    def Message(self, node, type, data):
        if type==MSG_DESCRIPTION_CHECKUPDATE:
            bc=node.GetDataInstance()
            if bc.GetLink(LINK_TARGETOBJ) is not None:
                errorString=""
                if bc.GetLink(LINK_TARGETOBJ).GetType()!=1030508:
                    newObject=node.GetObject().GetClone()
                    doc=c4d.documents.GetActiveDocument()
                    doc.InsertObject(newObject)
                    bc.SetLink(LINK_TARGETOBJ,newObject)
                    newObject.Remove()
                    errorString="Animator can only target AnimationSet!"
                if errorString!="":
                    c4d.gui.MessageDialog(errorString)
            if bc.GetLink(LINK_TARGETSTATE) is not None:
                errorString=""
                if bc.GetLink(LINK_TARGETSTATE).GetType()!=1028938 and bc.GetLink(LINK_TARGETSTATE).GetType()!=1030484:
                    newObject=node.GetObject().GetClone()
                    doc=c4d.documents.GetActiveDocument()
                    doc.InsertObject(newObject)
                    bc.SetLink(LINK_TARGETSTATE,newObject)
                    newObject.Remove()
                    errorString="TargetState must be a SkeletonAnimationTag or a VertexAnimationTag!"
                if errorString!="":
                    c4d.gui.MessageDialog(errorString)
            if bc.GetLink(LINK_SKELETON) is not None:
                errorString=""
                if bc.GetLink(LINK_SKELETON).GetType()!=1028937:
                    newObject=node.GetObject().GetClone()
                    doc=c4d.documents.GetActiveDocument()
                    doc.InsertObject(newObject)
                    bc.SetLink(LINK_SKELETON,newObject)
                    newObject.Remove()
                    errorString="TargetSkeleton must be a SkeletonTag (this must only be set for VertexAnimations)!"
                if errorString!="":
                    c4d.gui.MessageDialog(errorString)
                    
                
        #check if the Message was send from a Description-Dialog (such as this Tag)
        #print type
                    
        return True
        
        
    def GetDEnabling (self, node, id, t_data, flags, itemdesc):
                        
        #if the function has not returned False by now, the gui-element is set to be enabled by returning True
        return True
# ++++++++++++++++ The Main function. Loads icons, registeres plugins on startup etc. ++++++++++++++++++
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "res", "icon.tif"))
    plugins.RegisterTagPlugin(id=PLUGIN_ID, str="AWD Animator", g=AWDAnimatorXpression, description="AWDAnimator", icon=bmp, info=c4d.TAG_MULTIPLE|c4d.TAG_VISIBLE)