import c4d
import os
from awdexporter import ids
from awdexporter import workerExporter
from awdexporter import mainHelpers   
from awdexporter import classCanvas
from awdexporter import mainExporter

from awdexporter import maindialogHelpers
from awdexporter import mainSkeletonHelper
from awdexporter import maindialogCreator

workerThread=None
exportData=None
enableObjects=[]
enableStates=[]
class AboutDialog(c4d.gui.GeDialog):
    BUTTON_ID = 1001
    def CreateLayout(self):
        self.TabGroupBegin(1003,c4d.BFH_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.TAB_TABS)    
        #Group Level 2
        self.GroupBegin(1003,c4d.BFH_CENTER|c4d.BFV_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,1,1,"About")#c4d.plugins.GeLoadString(ids.TABGRP_GENERAL))
        view=self.AddCustomGui(1001, c4d.CUSTOMGUI_HTMLVIEWER, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 400, 400, c4d.BaseContainer())
        view.SetUrl(os.path.join(os.path.dirname(__file__), "res",  "123456"), c4d.URL_ENCODING_UTF16)
        self.GroupEnd()
        self.GroupEnd()
        return True        
    def Command(self, id, msg):
        #self.Close()
        return True
class HelpDialog(c4d.gui.GeDialog):
    BUTTON_ID = 1001
    def CreateLayout(self):
        self.TabGroupBegin(1003,c4d.BFH_CENTER|c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,c4d.TAB_TABS)   
        view=self.AddCustomGui(1001, c4d.CUSTOMGUI_HTMLVIEWER, "", c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 400, 400, c4d.BaseContainer())
        view.SetUrl(os.path.join(os.path.dirname(__file__), "res",  "123456"), c4d.URL_ENCODING_UTF16)
        self.GroupEnd()
        return True        
    def Command(self, id, msg):
        #self.Close()
        return True

# this class is C4DThread Class, and will be executed to have calculated the mesh-converting in other thread than the c4d main thread
class WorkerThread(c4d.threading.C4DThread):    
    def Main(self):
        global exportData
        doc=c4d.documents.GetActiveDocument()
        if doc is not None:
            workerExporter.startWorkerExport(exportData,self)                
            c4d.StatusClear()



# the main Dialog class. this class contains the functions to create and handle the dialog.
class MainDialog(c4d.gui.GeDialog):
       

    workerAction=None
    userarea = None
    awdExporterData=None 
    sliderEditor = 1.0
    sliderRender = 1.0
    sliderEditorBool = False
    sliderRenderBool = False

    scale = 1.0
    unusedMats = False
    selectedOnly = False
    streaming = False
    compressData = False
    debug = False
    closeAfter = False
    
    docName=None
    
    firstFrame=0
    lastFrame=0
    firstFrameUser=0
    lastFrameUser=0
    textures=0
    copyTextures=False
    texturesURL=""
    animationBool = False
    vanimationBool = False
    animationRange = int(0)
    openInPreFab = False
    exportSceneLights = False
    exportExtraMats = False
    exportUnsupportedTex = False
        
    def __init__(self): 
        doc=c4d.documents.GetActiveDocument()
        if doc:
            if self.docName!=doc.GetDocumentPath():
                self.docName=doc.GetDocumentPath()
                self.firstFrame = doc.GetMinTime().GetFrame(doc.GetFps())
                self.lastFrame = doc.GetMaxTime().GetFrame(doc.GetFps())
        self.userarea = classCanvas.Canvas()
        
    def CreateLayout(self):      
        #icon2 = c4d.bitmaps.BaseBitmap()
        #icon2.InitWith(os.path.join(os.path.dirname(__file__), "res", "pic.jpg"))    
        #bc = c4d.BaseContainer()                         
        #bc.SetLong(c4d.BITMAPBUTTON_ICONID1, 1390382) 
        #bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        #self.myBitButton = self.AddCustomGui(1390382, c4d.CUSTOMGUI_BITMAPBUTTON, "Bend", c4d.BFH_CENTER | c4d.BFV_CENTER, 32, 32, bc)
        #self.myBitButton = c4d.gui.BitmapButtonCustomGui 
        maindialogCreator.createLayout(self)
        #dialogLoadet=self.LoadDialogResource(ids.MAINDIALOG, None, flags= c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT )  
        mainHelpers.updateCanvas(self,exportData)
        maindialogHelpers.InitValues(self)     
        return True

                
    def CoreMessage(self, msg, result):
        #if msg==c4d.EVMSG_BROWSERCHANGE:
            #print "JA"
        mainHelpers.updateCanvas(self,exportData)#update the status-canvas
        doc=c4d.documents.GetActiveDocument()
        if doc:
            isDirty=False
            if self.GetLong(ids.COMBO_RANGE)==0:
                if self.firstFrame != doc.GetMinTime().GetFrame(doc.GetFps()):
                    isDirty=True
                if self.lastFrame != doc.GetMaxTime().GetFrame(doc.GetFps()):
                    isDirty=True
            if self.GetLong(ids.COMBO_RANGE)==1:
                if self.firstFrame != doc.GetLoopMinTime().GetFrame(doc.GetFps()):
                    isDirty=True
                if self.lastFrame != doc.GetLoopMaxTime().GetFrame(doc.GetFps()):
                    isDirty=True
            if self.docName!=doc.GetDocumentPath():
                self.docName=doc.GetDocumentPath()
                isDirty=True                   
            if isDirty==True:
                maindialogHelpers.setUI(self)
        return True
      
    # this function will be executed every 20ms as long as a Background-thread is active
    def Timer(self, msg):
        global exportData   # we need this to be global, so we can destroy it if needed
        if self.workerAction is None:
            self.SetTimer(0)
            
        if self.workerAction == "exporting":
            if workerThread is None:                                                        #this should never happen, but if it happens,
                exportData=None                                                                 # we destroy the exportData-Object.
                mainHelpers.updateCanvas(self,exportData)                                       # update the status-canvas
                print "unexpected Error: Workerthread not found by mainDialog.Timer function"   # and print out a error
            if workerThread is not None:
                if workerThread.IsRunning():                                                # while the background-thread is working, 
                    mainHelpers.updateCanvas(self,exportData)                                   # we update the status-canvas
                if not workerThread.IsRunning():                                            # if the background-thread is not working 
                    mainExporter.endExport(self,exportData)                                     # we call the function to end the export-processing                      
                    exportData=None                                                             # destroy the exportData-object
                    mainHelpers.updateCanvas(self,exportData)                                   # and update the status-canvas
        if self.workerAction == "meshChecking":
            pass#print "worker2"


    # this function will be executed every time a GUI-Element is changed by the user
    # using the global-IDs of the GUI-Elements, we can check which Element was changed, and react...
    def Command(self, id, msg):  
        global workerThread,exportData             
        mainHelpers.updateCanvas(self,exportData)       
        
        if id == ids.BTN_RECORDVERTEXANIMATION:        # Save with assets was hit: 
            doc=c4d.documents.GetActiveDocument()
            mainHelpers.bakeVertexAnimation(doc)
            
        if id == ids.BTN_CHECKSKELETON:                 # check Skeleton was hit:                
            op=mainHelpers.checkforValidSelectedSkeleton()
            if op is not None:  
                doc=c4d.documents.GetActiveDocument()
                doc.StartUndo()                     # Start undo support
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, op) # Support redo the insert operation
                checkSkeleton=mainSkeletonHelper.SkeletonHelper(op) # we create a SkeletonHelper-Object to check if the selected object is a valid skeleton
                doc.EndUndo()                       # Do not forget to close the undo support 
                return True
            c4d.gui.MessageDialog("To use this function, you need to select one Object that has Child-Objects\n,or one SkeletonTag,or one SkeletonAnimationTag")   
        if id == ids.BTN_CREATESKELETONANIMATION:                 # check Skeleton was hit:                
            op=mainHelpers.checkforValidSelectedSkeleton()
            if op is not None:        
                mainHelpers.copySkeletonAndApplySkeletonAnimation(op) # we create a SkeletonHelper-Object to check if the selected object is a valid skeleton
                return True
            c4d.gui.MessageDialog("To use this function, you need to select one SkeletonTag, or one Object that has a SkeletonTag applied!")  
                
        if id == ids.BTN_SAVEWITHASSETS:        # Save with assets was hit: 
            c4d.CallCommand(12255)                  # we just call the command "Save C4D-Scene with Assets"           
                    
        if id == ids.BTN_CANCEL:                # cancel Button was hit: cancel export process:   
            print "User cancelled the export-process"
            self.SetTimer(0)
            self.workerAction=None
            if workerThread is not None:
                if workerThread.IsRunning()==True:
                    workerThread.End()
            exportData=None
            mainHelpers.updateCanvas(self,exportData)
            maindialogHelpers.enableAll(self,True)
            return True            
       
        if id == ids.BTN_EXPORT:             # export button was hit: start export process:
            #check if a valid C4D scene is active, if not we return with error-message
            doc=c4d.documents.GetActiveDocument()
            self.workerAction="exporting"
            if doc==None:
                newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
                c4d.gui.MessageDialog(newMessage)
                return True
            if doc.GetDocumentPath()==None or doc.GetDocumentPath()=="":
                newMessage=c4d.plugins.GeLoadString(ids.STATUSMESSAGE1)
                c4d.gui.MessageDialog(newMessage)
                return True
            
            exportData=mainExporter.startExport(self,doc)       # start the export-process thats done in the c4d-main-Thread                     
            if exportData is not None:                            # if the exportData object is still alive, no error has occured
                mainHelpers.printErrors(self,exportData)                              # if any errors occured, print them out and delete the "exportData"-object
                workerThread  = WorkerThread()                  # recreated the workerThread (open a new c4d-thread for the heavy mesh-processing)
                workerThread.Start()                            # start the workerThread
                self.SetTimer(20)                               # start the timer-function to monitor the workerThread
            if exportData is None:                            # if the export data is not alive, a error has occured
                self.SetTimer(0)                                # stop the timer-function
              
        if id == ids.CBOX_ANIMATION: 
            self.animationBool=self.GetBool(ids.CBOX_ANIMATION)
            maindialogHelpers.setUI(self)  
        if id == ids.CBOX_VANIMATION: 
            self.vanimationBool=self.GetBool(ids.CBOX_VANIMATION)
            maindialogHelpers.setUI(self) 
        if id == ids.CBOX_CLOSEAFTEREXPORT: 
            self.closeAfter=self.GetBool(ids.CBOX_CLOSEAFTEREXPORT)
        if id == ids.CBOX_UNUSEDMATS: 
            self.unusedMats=self.GetBool(ids.CBOX_UNUSEDMATS)
            
        if id == ids.CBOX_STREAMING: 
            self.streaming=self.GetBool(ids.CBOX_STREAMING)
            if self.streaming==True:
                self.SetBool(ids.CBOX_COMPRESSED,False)
                self.compressData=False
            maindialogHelpers.setUI(self)  
                
        if id == ids.CBOX_COMPRESSED: 
            self.compressData=self.GetBool(ids.CBOX_COMPRESSED)
            if self.compressData==True:
                self.SetBool(ids.CBOX_STREAMING,False)
                self.streaming=False
            maindialogHelpers.setUI(self)  
            
        if id == ids.CBOX_DEBUG:  
            self.debug=self.GetBool(ids.CBOX_DEBUG)
            
        if id == ids.CBOX_OPENPREFAB:  
            self.openInPreFab=self.GetBool(ids.CBOX_OPENPREFAB)
            
        if id == ids.COMBO_RANGE: 
            self.animationRange=self.GetLong(ids.COMBO_RANGE)
            maindialogHelpers.setUI(self)
            
        if id == ids.COMBO_TEXTURESMODE: 
            maindialogHelpers.setValues(self)   
            maindialogHelpers.setUI(self)
           
        if id == ids.MENU_ABOUT_ABOUT: 

            pass#dlg = AboutDialog()
            #DLG_TYPE_MODAL = > synchronous dialog
            #DLG_TYPE_ASYNC = > asynchronous dialogs
            #dlg.Open(dlgtype=c4d.DLG_TYPE_MODAL, defaultw=300, defaulth=300)
            
        if id == ids.MENU_ABOUT_HELP: 
            realPath= os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
            helpPath=os.path.join(realPath, "res",  "Help","index.html")
            c4d.storage.GeExecuteFile(helpPath)
            print helpPath
            #pass#dlg = HelpDialog()
            #DLG_TYPE_MODAL = > synchronous dialog
            #DLG_TYPE_ASYNC = > asynchronous dialogs
            #dlg.Open(dlgtype=c4d.DLG_TYPE_ASYNC, defaultw=400, defaulth=400)
            
        if id == ids.MENU_CHECKFORUPDATE: 
            realPath= os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
            helpPath=os.path.join(realPath, "res",  "awdtoolsc4dversion.xml")
            versionThis=maindialogHelpers.loadVersionFile(helpPath)
            versionWeb=maindialogHelpers.loadVersionFilefromNet()
            if versionThis=="" or versionWeb=="":
                return
            if versionThis!=versionWeb:
                message="Your Version is not up to date\n"
                message+="Go to \nhttps://github.com/awaytools/awd-tools-c4d\n and get the new version"
                message+="Your version = "+str(versionThis)+"\n"
                message+="Latest version = "+str(versionWeb)+"\n"
            if versionThis==versionWeb:
                message="Your Version is up to date\n"
            c4d.gui.MessageDialog(message)
            
        maindialogHelpers.setValues(self)   
        return True  
    
    """
    # called on 'Close()'
    def AskClose(self):
        
        return not c4d.gui.QuestionDialog(c4d.plugins.GeLoadString(ids.STR_ASKCLOSE))
    """       