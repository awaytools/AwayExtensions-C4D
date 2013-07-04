import c4d
import os

from awdimporter import ids
from awdimporter import importer
    

from xml.dom import minidom
import xml.dom.minidom as dom

MAINDIALOG_SCALE_DATA = 80000
MAINDIALOG_SCALE_JOINTS_DATA = 80015
CBOX_SKEL_ANIM_TRANSLATIONS_DATA = 80002
CBOX_SKEL_ANIM_SCALE_DATA = 80003
CBOX_SKEL_ROOT_ANIM_TRANSLATIONS_DATA = 80004
CBOX_SKEL_ROOT_ANIM_SCALE_DATA = 80005
CBOX_SKEL_TPOSERETARGET_DATA = 80006
CBOX_DEBUG_DATA = 80007
CBOX_CLOSEAFTER_DATA = 80008
COMBO_EXTERNTEXTURESPATH_DATA = 80009
COMBO_EMBEDTEXTRESPATH_DATA = 80010
LINK_EXTERNTEXTURESPATH_DATA = 80011
LINK_EMBEDTEXTRESPATH_DATA = 80012

class MainDialog(c4d.gui.GeDialog):
       
    doc = c4d.documents.GetActiveDocument()
	
    awdImporterData=None 
    scale = 1.0
    scaleJoints = 1.0
    skel_anim_translation = False
    skel_anim_scale = False
    skel_anim_translation_root = False
    skel_anim_scale_root = False
    skel_tposeretarget = False
    debug = False
    closeafter = False
    externtexPathmode = 0
    externtexPathmodeLink = ""
    embedtexPathmode = 0
    embedtexPathmodeLink = ""
	

	
        
    # called once when the dialog is initialized
    def __init__(self): 
        
        # kill the menu-bar
        pass#self.AddGadget(c4d.DIALOG_NOMENUBAR, ids.MAINDIALOG);
        
        
    # called when the dialog is opened - load or generate the GUI here
    def CreateLayout(self):  
        
        #create the menu
        self.MenuFlushAll()
        #about/branding menu
        self.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_PRESET))
        self.MenuAddString(ids.MENU_PRESET_LOAD, c4d.plugins.GeLoadString(ids.MENU_PRESET_LOAD))
        self.MenuAddString(ids.MENU_PRESET_SAVE, c4d.plugins.GeLoadString(ids.MENU_PRESET_SAVE))
        self.MenuSubEnd()
        self.MenuSubBegin(c4d.plugins.GeLoadString(ids.MENU_ABOUT))
        self.MenuAddString(ids.MENU_ABOUT_HELP, c4d.plugins.GeLoadString(ids.MENU_ABOUT_HELP))
        self.MenuAddString(ids.MENU_ABOUT_ABOUT, c4d.plugins.GeLoadString(ids.MENU_ABOUT_ABOUT))
        self.MenuSubEnd()
        self.MenuFinished()
        # load and parse the dialog layout from the resource file
        bc = c4d.BaseContainer()                            ######Create a new container to store the button image 
        bc.SetLong(c4d.BITMAPBUTTON_ICONID1, 1390383) #####Sets Button Icon
        bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        self.myBitButton=self.AddCustomGui(1390383, c4d.CUSTOMGUI_BITMAPBUTTON, "Bend", c4d.BFH_CENTER | c4d.BFV_CENTER, 32, 32, bc)
        self.myBitButton = c4d.gui.BitmapButtonCustomGui 
        dialogLoadet=self.LoadDialogResource(ids.MAINDIALOG, None, flags= c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT )     
        if dialogLoadet==True:

			self.InitValues()     
			return True
		 
    

    # called after 'CreateLayout()' - used to initialize the GUI elements 
    #and reset values
    def InitValues(self): 
        
        # Get saved value
		
        self.awdImporterData = c4d.plugins.GetWorldPluginData(ids.PLUGINID)
        if self.awdImporterData:
            if self.awdImporterData[MAINDIALOG_SCALE_DATA]:
				self.scale = self.awdImporterData[MAINDIALOG_SCALE_DATA]
				
            if self.awdImporterData[MAINDIALOG_SCALE_JOINTS_DATA]:
				self.scaleJoints = self.awdImporterData[MAINDIALOG_SCALE_JOINTS_DATA]
				
            if self.awdImporterData[CBOX_SKEL_ANIM_TRANSLATIONS_DATA]:
				self.skel_anim_translation = self.awdImporterData[CBOX_SKEL_ANIM_TRANSLATIONS_DATA]
				
            if self.awdImporterData[CBOX_SKEL_ANIM_SCALE_DATA]:
				self.skel_anim_scale = self.awdImporterData[CBOX_SKEL_ANIM_SCALE_DATA]
				
            if self.awdImporterData[CBOX_SKEL_ROOT_ANIM_TRANSLATIONS_DATA]:
				self.skel_anim_translation_root = self.awdImporterData[CBOX_SKEL_ROOT_ANIM_TRANSLATIONS_DATA]
				
            if self.awdImporterData[CBOX_SKEL_ROOT_ANIM_SCALE_DATA]:
				self.skel_anim_scale_root = self.awdImporterData[CBOX_SKEL_ROOT_ANIM_SCALE_DATA]

            if self.awdImporterData[CBOX_SKEL_TPOSERETARGET_DATA]:
				self.skel_tposeretarget = self.awdImporterData[CBOX_SKEL_TPOSERETARGET_DATA]
				
            if self.awdImporterData[CBOX_DEBUG_DATA]:
				self.debug = self.awdImporterData[CBOX_DEBUG_DATA]

            if self.awdImporterData[CBOX_CLOSEAFTER_DATA]:
				self.closeafter = self.awdImporterData[CBOX_CLOSEAFTER_DATA]
				
            if self.awdImporterData[COMBO_EXTERNTEXTURESPATH_DATA]:
				self.externtexPathmode = self.awdImporterData[COMBO_EXTERNTEXTURESPATH_DATA]
				
            if self.awdImporterData[COMBO_EMBEDTEXTRESPATH_DATA]:
				self.embedtexPathmode = self.awdImporterData[COMBO_EMBEDTEXTRESPATH_DATA]
				
            if self.awdImporterData[LINK_EXTERNTEXTURESPATH_DATA]:
				self.externtexPathmodeLink = self.awdImporterData[LINK_EXTERNTEXTURESPATH_DATA]
				
            if self.awdImporterData[LINK_EMBEDTEXTRESPATH_DATA]:
				self.embedtexPathmodeLink = self.awdImporterData[LINK_EMBEDTEXTRESPATH_DATA]
				
        else:
            self.awdImporterData = c4d.BaseContainer()
        # When the dialog opens, get the RSS feed
        self.setUI()
        self.setValues()     
        return True   
			

		
    def setUI(self):
        # init the sliders
        self.SetReal(ids.REAL_SCALE, self.scale, 0.001, 10000, 1.0, c4d.FORMAT_REAL)
        self.SetReal(ids.REAL_SCALE_JOINTS, self.scaleJoints, 0.001, 10000, 1.0, c4d.FORMAT_REAL)
		
        self.SetBool(ids.CBOX_SKEL_ANIM_TRANSLATIONS, self.skel_anim_translation)
        self.SetBool(ids.CBOX_SKEL_ANIM_SCALE, self.skel_anim_scale)
        self.SetBool(ids.CBOX_SKEL_ROOT_ANIM_TRANSLATIONS, self.skel_anim_translation_root)
        self.SetBool(ids.CBOX_SKEL_ROOT_ANIM_SCALE, self.skel_anim_scale_root)
        self.SetBool(ids.CBOX_SKEL_TPOSERETARGET, self.skel_tposeretarget)
        self.SetBool(ids.CBOX_DEBUG, self.debug)
        self.SetBool(ids.CBOX_CLOSEAFTER, self.closeafter)
		
        self.SetLong(ids.COMBO_EXTERNTEXTURESPATH, self.externtexPathmode)
        self.SetLong(ids.COMBO_EMBEDTEXTRESPATH, self.embedtexPathmode)
		
        self.SetString(ids.LINK_EXTERNTEXTURESPATH, self.externtexPathmodeLink)
        self.SetString(ids.LINK_EMBEDTEXTRESPATH, self.embedtexPathmodeLink)	
		
        return True

    def setValues(self):
        # Save the Values to the Container

        self.scale=self.GetReal(ids.REAL_SCALE)
        self.awdImporterData.SetReal(MAINDIALOG_SCALE_DATA, self.scale)
		
        self.scaleJoints=self.GetReal(ids.REAL_SCALE_JOINTS)
        self.awdImporterData.SetReal(MAINDIALOG_SCALE_JOINTS_DATA, self.scaleJoints)
		
        self.skel_anim_translation=self.GetBool(ids.CBOX_SKEL_ANIM_TRANSLATIONS)
        self.awdImporterData.SetBool(CBOX_SKEL_ANIM_TRANSLATIONS_DATA, self.skel_anim_translation)
		
        self.skel_anim_scale=self.GetBool(ids.CBOX_SKEL_ANIM_SCALE)
        self.awdImporterData.SetBool(CBOX_SKEL_ANIM_SCALE_DATA, self.skel_anim_scale)
		
        self.skel_anim_translation_root=self.GetBool(ids.CBOX_SKEL_ROOT_ANIM_TRANSLATIONS)
        self.awdImporterData.SetBool(CBOX_SKEL_ROOT_ANIM_TRANSLATIONS_DATA, self.skel_anim_translation_root)
		
        self.skel_anim_scale_root=self.GetBool(ids.CBOX_SKEL_ROOT_ANIM_SCALE)
        self.awdImporterData.SetBool(CBOX_SKEL_ROOT_ANIM_SCALE_DATA, self.skel_anim_scale_root)
		
        self.skel_tposeretarget=self.GetBool(ids.CBOX_SKEL_TPOSERETARGET)
        self.awdImporterData.SetBool(CBOX_SKEL_TPOSERETARGET_DATA, self.skel_tposeretarget)
		
        self.debug=self.GetBool(ids.CBOX_DEBUG)
        self.awdImporterData.SetBool(CBOX_DEBUG_DATA, self.debug)
		
        self.closeafter=self.GetBool(ids.CBOX_CLOSEAFTER)
        self.awdImporterData.SetBool(CBOX_CLOSEAFTER_DATA, self.closeafter)
		
        self.externtexPathmode=self.GetLong(ids.COMBO_EXTERNTEXTURESPATH)
        self.awdImporterData.SetLong(COMBO_EXTERNTEXTURESPATH_DATA, self.externtexPathmode)
		
        self.embedtexPathmode=self.GetLong(ids.COMBO_EMBEDTEXTRESPATH)
        self.awdImporterData.SetLong(COMBO_EMBEDTEXTRESPATH_DATA, self.embedtexPathmode)
		
        self.externtexPathmodeLink=self.GetString(ids.LINK_EXTERNTEXTURESPATH)
        self.awdImporterData.SetString(LINK_EXTERNTEXTURESPATH_DATA, self.externtexPathmodeLink)
		
        self.embedtexPathmodeLink=self.GetString(ids.LINK_EMBEDTEXTRESPATH)
        self.awdImporterData.SetString(LINK_EMBEDTEXTRESPATH_DATA, self.embedtexPathmodeLink)
		
        self.Enable(ids.LINK_EXTERNTEXTURESPATH,False)
        if self.GetLong(ids.COMBO_EXTERNTEXTURESPATH)==2:
			self.Enable(ids.LINK_EXTERNTEXTURESPATH,True)
			
        self.Enable(ids.LINK_EMBEDTEXTRESPATH,False)
        if self.GetLong(ids.COMBO_EMBEDTEXTRESPATH)==3:
			self.Enable(ids.LINK_EMBEDTEXTRESPATH,True)
		

        c4d.plugins.SetWorldPluginData(ids.PLUGINID, self.awdImporterData)  
		

		
		
    def savePreset(self):
        datei=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "save Preset", "dps")
        output_xml = dom.Document()#in here we save our output-xml data
        preset_xml=dom.Element("PresetForAWDImporter")
        preset_xml.setAttribute("scale",str(self.scale))
        preset_xml.setAttribute("scale",str(self.scaleJoints))
        preset_xml.setAttribute("skel_anim_translation",str(self.skel_anim_translation))
        preset_xml.setAttribute("skel_anim_scale",str(self.skel_anim_scale))
        preset_xml.setAttribute("skel_anim_translation_root",str(self.skel_anim_translation_root))
        preset_xml.setAttribute("skel_anim_scale_root",str(self.skel_anim_scale_root))
        preset_xml.setAttribute("skel_tposeretarget",str(self.skel_tposeretarget))
        preset_xml.setAttribute("debug",str(self.debug))
        preset_xml.setAttribute("closeafter",str(self.closeafter))
        preset_xml.setAttribute("externtexPathmode",str(self.externtexPathmode))
        preset_xml.setAttribute("externtexPathmodeLink",str(self.externtexPathmodeLink))
        preset_xml.setAttribute("embedtexPathmode",str(self.embedtexPathmode))
        preset_xml.setAttribute("embedtexPathmodeLink",str(self.embedtexPathmodeLink))
        output_xml.appendChild(preset_xml)
                
        if datei!=None:    
            str_object_xml=output_xml.toprettyxml()  
            f = open(datei, 'wb')
            f.write(str_object_xml)
            f.close()	
        return True
			
    def loadPreset(self):
		  
        datei=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "open Preset", c4d.FILESELECT_LOAD,"dps")  
        if datei!=None:                
         
            dom1 = dom.parse(datei) 
			
            self.scale=float(dom1.firstChild.getAttribute("scale"))
            self.scaleJoints=float(dom1.firstChild.getAttribute("scaleJoints"))
            self.skel_anim_translation=False
            if dom1.firstChild.getAttribute("skel_anim_translation")=="True":
				self.skel_anim_translation=True
            self.skel_anim_scale=False
            if dom1.firstChild.getAttribute("skel_anim_scale")=="True":
				self.skel_anim_scale=True
            self.skel_anim_translation_root=False
            if dom1.firstChild.getAttribute("skel_anim_translation_root")=="True":
				self.skel_anim_translation_root=True
            self.skel_anim_scale_root=False
            if dom1.firstChild.getAttribute("skel_anim_scale_root")=="True":
				self.skel_anim_scale_root=True
            self.skel_tposeretarget=False
            if dom1.firstChild.getAttribute("skel_tposeretarget")=="True":
				self.skel_tposeretarget=True
            self.debug=False
            if dom1.firstChild.getAttribute("debug")=="True":
				self.debug=True
            self.closeafter=False
            if dom1.firstChild.getAttribute("closeafter")=="True":
				self.closeafter=True
            self.externtexPathmode=int(dom1.firstChild.getAttribute("externtexPathmode"))
            self.embedtexPathmode=int(dom1.firstChild.getAttribute("embedtexPathmode"))
            self.externtexPathmodeLink=dom1.firstChild.getAttribute("externtexPathmodeLink")
            self.embedtexPathmodeLink=dom1.firstChild.getAttribute("embedtexPathmodeLink")
				
			
        self.setUI()
        return True

    # called on every GUI-interaction - check the 'id' against those of
    #your GUI elements
    def Command(self, id, msg):  
              			
        # "Ok"     
				
        if id == ids.MENU_PRESET_LOAD:   
            exportResult=self.loadPreset()  
        self.setValues()     
        if id == ids.MENU_PRESET_SAVE:   
            exportResult=self.savePreset() 
              
        if id == ids.BTN_IMPORT:
            importer.importAWD(self)
            if self.closeafter==True:
				self.Close()  
        return True  
    
    """
    # called on 'Close()'
    def AskClose(self):
        
        return not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_ASKCLOSE))
    """       