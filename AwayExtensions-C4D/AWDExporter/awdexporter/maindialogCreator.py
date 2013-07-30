import c4d
import os
from awdexporter import ids
from awdexporter import classCanvas

        
def createLayout(mainDialog):         
    global exportData,workerThread,exchangeData
    mainDialog.SetTitle(c4d.plugins.GeLoadString(ids.STR_TITLE))
        
    mainDialog.MenuFlushAll()
    
    #mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_PRESET))
    #self.MenuAddString(ids.MENU_PRESET_LOAD, c4d.plugins.GeLoadString(ids.MENU_PRESET_LOAD))
    #self.MenuAddString(ids.MENU_PRESET_SAVE, c4d.plugins.GeLoadString(ids.MENU_PRESET_SAVE))
    #self.MenuSubEnd()
    mainDialog.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_ABOUT))
    mainDialog.MenuAddString(ids.MENU_ABOUT_HELP, c4d.plugins.GeLoadString(ids.MENU_ABOUT_HELP))
    mainDialog.MenuAddString(ids.MENU_CHECKFORUPDATE, c4d.plugins.GeLoadString(ids.MENU_CHECKFORUPDATE))
    mainDialog.MenuAddString(ids.MENU_ABOUT_ABOUT, c4d.plugins.GeLoadString(ids.MENU_ABOUT_ABOUT))
    mainDialog.MenuSubEnd()
    mainDialog.MenuFinished()

     
    #Group Level 1
    mainDialog.TabGroupBegin(ids.TABGRP_MAIN,c4d.BFH_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.TAB_TABS)    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_GENERAL,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,c4d.plugins.GeLoadString(ids.TABGRP_GENERAL))
    mainDialog.GroupSpace(5,15)  
    mainDialog.GroupBorderSpace(10, 5, 10, 5) 
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,"")
                #Group Level 4
    mainDialog.element = mainDialog.AddSeparatorH(300)
    mainDialog.GroupBegin(0,c4d.BFV_CENTER,2,1,"")
    mainDialog.GroupSpace(5,5)  
    mainDialog.element = mainDialog.AddStaticText(ids.REAL_SCALE_STR, flags=c4d.BFV_CENTER,initw=60,inith=12,name=c4d.plugins.GeLoadString(ids.REAL_SCALE_STR))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.REAL_SCALE, flags=c4d.BFV_CENTER,initw=100,inith=14) 
                #End Level 4
    mainDialog.GroupEnd()
                #Group Level 4
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,1,3,"")
    mainDialog.GroupSpace(5,10)  
    mainDialog.element = mainDialog.AddSeparatorH(300)
                    #Group Level 5
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,2,1,"")
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_STREAMING, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_STREAMING))
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_DEBUG, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_DEBUG))
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_COMPRESSED, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_COMPRESSED))
                    #End Level 5
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
                    #Group Level 5
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_OPENPREFAB, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_OPENPREFAB))
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_CLOSEAFTEREXPORT, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_CLOSEAFTEREXPORT))
                    #End Level 5
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
                    #Group Level 5
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,2,1,"")
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_EXPORTLIGHTXML, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_EXPORTLIGHTXML))
                    #End Level 5
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
                #End Level 4
    mainDialog.GroupEnd()
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_SAVEWITHASSETS, flags=c4d.BFH_CENTER,initw=300, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_SAVEWITHASSETS))
            #End Level 3
    mainDialog.element = mainDialog.AddSeparatorH(300)
    mainDialog.GroupEnd()
        #End Level 2
    mainDialog.GroupEnd()
    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_MATERIALS,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,c4d.plugins.GeLoadString(ids.TABGRP_MATERIALS))
    mainDialog.GroupSpace(5,15)  
    mainDialog.GroupBorderSpace(10, 5, 10, 5) 
            #Group Level 3
    mainDialog.element = mainDialog.AddSeparatorH(300)
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,1,2,"")
    mainDialog.GroupSpace(5,15)  
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_UNUSEDMATS, flags=c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_UNUSEDMATS))
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_LIGHTMATERIALS	, flags=c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_LIGHTMATERIALS	))
    mainDialog.element = mainDialog.AddSeparatorH(300)
                #Group Level 4
    mainDialog.GroupBegin(ids.GRP_TEXTURES, c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,1,2,c4d.plugins.GeLoadString(ids.GRP_TEXTURES))
    mainDialog.GroupBorder(c4d.BORDER_BLACK) 
    mainDialog.GroupBorderSpace(10, 15, 10, 15)
    mainDialog.GroupSpace(20,15)   
    mainDialog.element = mainDialog.AddComboBox(ids.COMBO_TEXTURESMODE,flags=c4d.BFH_SCALEFIT,initw=80, inith=0) 
    mainDialog.AddChild(ids.COMBO_TEXTURESMODE, 0, c4d.plugins.GeLoadString(ids.COMBOITEM_EMBED))
    mainDialog.AddChild(ids.COMBO_TEXTURESMODE, 1, c4d.plugins.GeLoadString(ids.COMBOITEM_EXTERNPATH))     
                #End Level 4
    #mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_UNSUPPORTETTEX, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=30, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_UNSUPPORTETTEX))
    mainDialog.GroupEnd()
    
    mainDialog.element = mainDialog.AddSeparatorH(300)
    #mainDialog.createButton = mainDialog.AddButton(ids.BTN_CHECKPOLY, flags=c4d.BFH_CENTER,initw=300, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CHECKPOLY))  
    #mainDialog.element = mainDialog.AddSeparatorH(300)
            #End Level 3
    mainDialog.GroupEnd()
        #End Level 2
    mainDialog.GroupEnd()
    
        #Group Level 2
    mainDialog.GroupBegin(ids.TABGRP_ANIMATIONS,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,2,c4d.plugins.GeLoadString(ids.TABGRP_ANIMATIONS))
    mainDialog.GroupSpace(5,10)  
    mainDialog.GroupBorderSpace(10, 5, 10, 5) 
    mainDialog.element = mainDialog.AddSeparatorH(300)
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_ANIMATION, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=300, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_ANIMATION))
    mainDialog.element = mainDialog.AddCheckbox(ids.CBOX_VANIMATION, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT, initw=300, inith=0, name=c4d.plugins.GeLoadString(ids.CBOX_VANIMATION))
    
            #End Level 3
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.element = mainDialog.AddStaticText(ids.COMBO_RANGE_STR, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=60,inith=0,name=c4d.plugins.GeLoadString(ids.COMBO_RANGE_STR))
    mainDialog.element = mainDialog.AddComboBox(ids.COMBO_RANGE,flags=c4d.BFH_SCALEFIT,initw=80, inith=0) 
    mainDialog.AddChild(ids.COMBO_RANGE, 0, c4d.plugins.GeLoadString(ids.COMBO_RANGE_DOC))
    mainDialog.AddChild(ids.COMBO_RANGE, 1, c4d.plugins.GeLoadString(ids.COMBO_RANGE_PREVIEW))
    mainDialog.AddChild(ids.COMBO_RANGE, 2, c4d.plugins.GeLoadString(ids.COMBO_RANGE_CUSTOM))
    mainDialog.element = mainDialog.AddStaticText(ids.REAL_FIRSTFRAME_STR, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=60,inith=0,name=c4d.plugins.GeLoadString(ids.REAL_FIRSTFRAME_STR))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.REAL_FIRSTFRAME, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=100,inith=14) 
    mainDialog.element = mainDialog.AddStaticText(ids.REAL_LASTFRAME_STR, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=60,inith=0,name=c4d.plugins.GeLoadString(ids.REAL_LASTFRAME_STR))
    mainDialog.element = mainDialog.AddEditNumberArrows(ids.REAL_LASTFRAME, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=100,inith=14) 
            #End Level 3
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
            #Group Level 3
    mainDialog.GroupBegin(0,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT,2,1,"")
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CHECKSKELETON, flags=c4d.BFH_CENTER,initw=250, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CHECKSKELETON))   
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CREATESKELETONANIMATION, flags=c4d.BFH_CENTER,initw=200, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CREATESKELETONANIMATION))    
            #End Level 3
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddSeparatorH(300)
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_RECORDVERTEXANIMATION, flags=c4d.BFH_CENTER,initw=500, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_RECORDVERTEXANIMATION))    
       #End Level 2
    mainDialog.GroupEnd()
    
    #End Level 1
    mainDialog.GroupEnd()
    #Group Level 1
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,1,2,"")
    mainDialog.GroupSpace(5,5)   
    mainDialog.AddUserArea(ids.MAINDIALOG_USERAREA, flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT|c4d.BFV_CENTER|c4d.BFH_CENTER,initw=500,inith=30)
    mainDialog.AttachUserArea(mainDialog.userarea,ids.MAINDIALOG_USERAREA,c4d.USERAREA_COREMESSAGE)
    #End Level 1
    mainDialog.GroupEnd()
    #Group Level 1
    mainDialog.GroupBegin(0,c4d.BFH_SCALEFIT,2,2,"")
    mainDialog.GroupSpace(5,5)  
    mainDialog.GroupBorderSpace(10, 5, 10, 5) 
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_EXPORT, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_EXPORT))
    mainDialog.createButton = mainDialog.AddButton(ids.BTN_CANCEL, flags=c4d.BFH_SCALEFIT,initw=40, inith=20,name=c4d.plugins.GeLoadString(ids.BTN_CANCEL))
    #End Level 1
    mainDialog.GroupEnd()
    mainDialog.element = mainDialog.AddStaticText(ids.STRING_80PRO, flags=c4d.BFH_CENTER,initw=350,inith=0,name=c4d.plugins.GeLoadString(ids.STRING_80PRO)) 
    mainDialog.element = mainDialog.AddStaticText(0, flags=c4d.BFH_CENTER|c4d.BFH_SCALEFIT,initw=500,inith=0,name="")   
    #End Level 0
    mainDialog.GroupEnd()    

       