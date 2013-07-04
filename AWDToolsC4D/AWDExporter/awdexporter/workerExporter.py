# functions that will run inside the background-worker-thread
# main function of the worker-thread. 
# all other functions running in the worker-thread are called from here.

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import workerMeshReader
from awdexporter import workerHelpers
from awdexporter import mainLightRouting
from awdexporter import mainMaterials

	
# called after all functions running in the c4d-main-thread have been successfully executed, 
# and the exportdata object has been created and prepared.
# basically it converts the c4d-meshdata to away3d-meshdata, 
# restructures the previos created AWDBlocks
# parses the AWDBlocks into Binary exportAllData
# wirtes the file to harddisc
def startWorkerExport(exportData,workerthreat):
  
    workerHelpers.connectInstances(exportData)
    
    if workerthreat.TestBreak():
        return      
        
    #for oneObj in exportData.doc.GetObjects():
    #    mainLightRouting.readAllLightRouting(oneObj,exportData)   
        
    workerHelpers.getAllObjectData(exportData)
    
    if workerthreat.TestBreak():
        return    
    workerHelpers.createAnimatorBlocks(exportData.objList,exportData) 
    
    workerMeshReader.convertMeshes(exportData.allMeshObjects,exportData,workerthreat)   
    
    if exportData.unusedMats==True:
        for awdBlock in exportData.allAWDBlocks:
            if awdBlock.blockType==81:
                if awdBlock.data.isCreated==False and awdBlock.data.colorMat==False:
                    awdBlock.data.isCreated=True                
                    mainMaterials.createMaterial(awdBlock,exportData)
                
    if workerthreat.TestBreak():
        return          
    if exportData.exportLightXML==True:
        mainLightRouting.saveLightXML(exportData)
    exportData.status=3    
    
    
    
    workerHelpers.reorderAllBlocks(exportData)
    
    if workerthreat.TestBreak():
        return       
        
    workerHelpers.exportAllData(exportData)
    
    if workerthreat.TestBreak():
        return  
        
    exportData.allStatus+=1
	
    for block in exportData.allAWDBlocks: 
        if block.targetObject is not None:
            block.targetObject.SetName(str(block.name))
    
    for block in exportData.allSceneObjects:
        if block.data.sceneObject is not None:
            block.data.sceneObject.SetName(str(block.name))
        
		
    #print "export = "+str(exportData.allMeshObjects)
    #c4d.gui.MessageDialog("jnJK")

    #self.parse_mats(mats_xml,self.GetBool(CBOX_UNUSEDMATS["id"]),used_mat_names)#loop trough all matrials and creates xml
    #self.read_morphtags(copied_op)#loops trough all objects, sets all  morphtags keyvalues to 0          
    #object_eintrag = self.read_selected_object(copied_op,objSettings,lights_Dic)#loop through all objects, creating xml 
    #self.read_hirarchy_morphs(copied_op,object_eintrag)#loop through all objects again, creaing morphstates for children of hirarchy-morphs
    #self.export_meshes(copied_op,object_eintrag,allPointAndUvMorpTag)#parsing the meshes

            #self.export_to_XMLfile(output_xml)
            #doc.SetActiveObject(op)#make the original object activ again
        
        #op.SetEditorMode(c4d.MODE_UNDEF)#make original object visible again
        # if no object is selected we open a c4d.MessageDialog for ErrorNotification:
    #if not(op):    
        #print "No Object selected!\n"
        
      #copied_op.Remove()#remove cloned object  

            
      

 