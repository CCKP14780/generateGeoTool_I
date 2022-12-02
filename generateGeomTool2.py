import maya.cmds as cmds
import random
import maya.mel as mel
import json

#-----------#
#    UI     #    
#-----------#

def generateGeomTool():
    if cmds.window('genGeomTool_window',q = True,ex=True):
        cmds.deleteUI('genGeomTool_window',window = True)
    cmds.window('genGeomTool_window',t='Export Alembic Tool')

#-----------#
#    OBJ    #    
#-----------#

    cmds.columnLayout(adj=True)
    cmds.frameLayout(label='Object')
    
    cmds.radioCollection('obj_radioCol')
    cmds.radioButton('sphere_radioBtn',label='Sphere',select=True)
    cmds.radioButton('cube_radioBtn',label='Cube')
    cmds.radioButton('cone_radioBtn',label='Cone')
    cmds.radioButton('random_radioBtn',label='Random')
    
#-----------#
# TRANSFORM #    
#-----------#    
    
    cmds.frameLayout(label='Transform')
    cmds.text(label='Rotate')
    cmds.floatSliderGrp('rotMin_floatSliderGrp',l='min',field=True,minValue=0,maxValue=360,value=0)
    cmds.floatSliderGrp('rotMax_floatSliderGrp',l='max',field=True,minValue=0,maxValue=360,value=360)
       
    cmds.text(label='Scale')
    cmds.floatSliderGrp('sclMin_floatSliderGrp',l='min',field=True,minValue=0.1,maxValue=2,value=0.2)
    cmds.floatSliderGrp('sclMax_floatSliderGrp',l='max',field=True,minValue=0.1,maxValue=2,value=1.2)
   
#-----------#
#   BUTTON  #    
#-----------#

    cmds.button('create_btn',label='Create',h=30,c=createObject)       

#-----------#
#   EXPORT  #    
#-----------#

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2)
    cmds.radioCollection('obj_radioCol2')
    cmds.radioButton('abc_radioBtn',label='abc',select=True)
    cmds.radioButton('json_radioBtn',label='json')
    cmds.setParent('..')
    cmds.button(l='Export',c=exportData)

    cmds.showWindow('genGeomTool_window')
    cmds.window('genGeomTool_window',e = True,wh=[600,380]) 

#-----------#
#  CONNECT1 #    
#-----------#

def createObject(*args):
    primSel = cmds.radioCollection('obj_radioCol',q=True,select=True)
    
    if primSel == 'cube_radioBtn':
        prim = 'cube'
    if primSel == 'cone_radioBtn':
        prim = 'cone'
    if primSel == 'sphere_radioBtn':
        prim = 'sphere'
    elif primSel == 'random_radioBtn':
        prims = ['cube','sphere','cone']
        prim = random.choice(prims)
        
    roMin = cmds.floatSliderGrp('rotMin_floatSliderGrp',q=True,value=True)
    roMax = cmds.floatSliderGrp('rotMax_floatSliderGrp',q=True,value=True)
    sclMin = cmds.floatSliderGrp('sclMin_floatSliderGrp',q=True,value=True)
    sclMax = cmds.floatSliderGrp('sclMax_floatSliderGrp',q=True,value=True)
    
    generateGeo(prim=prim,rotate=[roMin,roMax],scale=[sclMin,sclMax])

#-----------#
#  CONNECT2 #    
#-----------#

def exportData(*args):
    exportOption = cmds.radioCollection('obj_radioCol2',q=True,select=True)
    if exportOption == 'abc_radioBtn':
        opt = 'abc'
    elif exportOption == 'json_radioBtn':
        opt = 'json'
        
    exportFunciton(opt)
        
#-----------#
#   FUNCT   #    
#-----------#

def generateGeo(num=5,amp=2,prim='cube',rotate=[0,360],scale=[1,1]):
    objs = []
    
    offset = (((num-1)*amp)/2)*(-1)#offset value
    for x in range(num):
        for z in range(num):
            for y in range(num):
                obj = ''
                if prim == 'cube':
                    obj = cmds.polyCube(ch=False)[0]#construction history
                elif prim == 'cone':
                    obj = cmds.polyCone(ch=False)[0]
                elif prim == 'sphere':
                    obj = cmds.polySphere(ch=False)[0]
                
                cmds.xform(obj,t=[(x*amp+offset),(y*amp),(z*amp+offset)],
                               ro=[random.uniform(rotate[0],rotate[1]),
                                   random.uniform(rotate[0],rotate[1]),
                                   random.uniform(rotate[0],rotate[1])
                               ],
                               s=[random.uniform(scale[0],scale[1]),
                                 random.uniform(scale[0],scale[1]),
                                 random.uniform(scale[0],scale[1])]
                )
                
                objs.append(obj)
    
    cmds.group(objs,n='prim_Grp')

def exportFunciton(exp=''):
    if exp == 'abc':
   
        sels = cmds.ls(sl=True, l=True)
    
        if sels:
            cmd='AbcExport -j '
            cmd+='"-frameRange 1 120 ' 
            cmd+='-dataFormat ogawa '
            cmd+='-root |prim_Grp '
            cmd+='-file D:/Geom.abc";'#the question does not provide the textfield to put the filepath that users wants to export their data, so i assume it is exported to drive D
    
            mel.eval(cmd)
            
    elif exp == 'json':
        
        data = []
        sels = cmds.ls(sl=True)
        filepath = 'D:/Data.json'
        
        if sels:
            for sel in sels:
                objInfo = {}
                
                pos = cmds.xform(sel,q=True,t=True,os=True)
                rot = cmds.xform(sel,q=True,ro=True,os=True)
                size = cmds.xform(sel,q=True,s=True,os=True)
                vis = cmds.getAttr(f'{sel}.visibility')
        
                objInfo[sel] = {
                    "translate": pos,
                    "rotate": rot,
                    "scale": size,
                    "visibility": vis,
                }
                data.append(objInfo)
        
                with open(filepath,'w') as f:
                    json.dump(data,f,indent = 4)
  
generateGeomTool()
