# functions that will run inside the background-worker-thread
# main-functions for mesh-converting

import c4d
from c4d import documents

from awdexporter import ids
from awdexporter import classesAWDBlocks
from awdexporter import workerSubMeshReader
from awdexporter import workerHelpers

# convert all the geometry-blocks from c4d-polygon-object to away3d mesh
def convertMeshes(meshBlockList,exportData,workerthreat):
    for meshBlock in meshBlockList:                     # we check if the user cancelled the process
        if workerthreat.TestBreak():                        # if user cancelled 
            return                                              # and return if he has   
        convertMesh(meshBlock,exportData,workerthreat)      # convert the geometry-block into away3d-mesh-data

def convertMesh(meshBlock,exportData,workerthreat):
    exportData.doc.SetActiveObject(meshBlock.copiedMesh)
    if not meshBlock.copiedMesh.GetTag(5604): 
        return    
    if not meshBlock.copiedMesh.GetTag(5600):
        return  
    materials=workerHelpers.getObjectsMaterials(meshBlock.copiedMesh)
    matCounter=0   
    while matCounter<len(materials):
        meshBlock.saveSubMeshes.append(classesAWDBlocks.awdSubMesh(materials[matCounter][0],materials[matCounter][1].name,materials[matCounter][1].selectionIndexe,materials[matCounter][2]))
        matCounter+=1
         
    if workerthreat.TestBreak():
        return        
            
    workerSubMeshReader.prepareSubmeshIndexe(meshBlock)       
 
    if workerthreat.TestBreak():
        return

    # if the meshBlock has a WeightTag-applied, we create a "jointTranslater"-list, so when parsing the weight-data later, we know which joint-indicies to set.
    if meshBlock.copiedMesh.GetTag(c4d.Tweights)!=None:
        firstSkeleton=exportData.jointIDstoSkeletonBlocks.get(str(meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(0,exportData.doc).GetName()),None)        
        noValidSkeleton=False
        if firstSkeleton!=None:
            firstSkeletonName=exportData.jointIDstoSkeletonBlocks[str(meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(0,exportData.doc).GetName())].name
            jointcounter=0 
            meshBlock.jointTranslater=[]
            while jointcounter<meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJointCount():
                curJoint=meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJoint(jointcounter,exportData.doc)
                if curJoint is not None:
                    if exportData.jointIDstoSkeletonBlocks.get(str(curJoint.GetName()),None) is None:
                        noValidSkeleton=True
                        break
                    if exportData.jointIDstoSkeletonBlocks.get(str(curJoint.GetName()),None) is not None:
                        if firstSkeletonName!=exportData.jointIDstoSkeletonBlocks[str(curJoint.GetName())].name:
                            noValidSkeleton=True
                            break
                    meshBlock.jointTranslater.append(exportData.jointIDstoJointBlocks[str(curJoint.GetName())].jointID-1)
                jointcounter+=1
            if noValidSkeleton==False:
                pass#print "Skeleton Found: "+str(firstSkeletonName)
        if firstSkeleton==None or noValidSkeleton==True:
            jointcounter=0
            meshBlock.jointTranslater=[]
            while jointcounter<meshBlock.copiedMesh.GetTag(c4d.Tweights).GetJointCount():
                meshBlock.jointTranslater.append(jointcounter)
                jointcounter+=1
    if workerthreat.TestBreak():
        return
        
    #morphs=[]    
    #for morphState in allPointAndUvMorpTag:
        #if morphState.morphedObject==cur_mesh:
            #morphs.append(morphState)   
    #for submesh in new_submeshes:
        #for morphState in morphs:
            #submorphVerts=[]
            #submorphUVs=[]
            #submorphActiv=False
            #submorphdata=[submorphVerts,submorphUVs,submorphActiv,morphState.morphName,morphState.tagName,morphState.tagObject]
            #submesh.morphs.append(submorphdata)                
                
    workerSubMeshReader.collectSubmeshData(meshBlock,exportData,workerthreat)   # parse this object into a awd2-geometry-block
    if workerthreat.TestBreak():                                                # when the user has cancelled the process: 
        return                                                                      # we stop executing and return 
    for subMesh in meshBlock.saveSubMeshes:                                     # for every SubMeshBlock that has been created:
        if workerthreat.TestBreak():                                                # we check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.transformUVS(subMesh)                                   # transform the uvs if needed (to allow for tilling etc)
        if workerthreat.TestBreak():                                                # check if the user cancelled the process
            return                                                                      # and return if he has
        workerSubMeshReader.buildGeometryStreams(subMesh,exportData.scale)          # build the AWD-geometry-streams for all submeshes



          
  
