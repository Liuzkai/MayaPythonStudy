import maya.cmds as cmds
from functools import partial

# Interface
window_name = 'Rig_Tool2'
window_title = "Simple Rig"
window_w = 200
window_h = 180

def create_window():
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)
    
    cmds.window(window_name)
    cmds.window(window_name, edit=True, w=window_w, h=window_h, title=window_title)
    cmds.columnLayout("main_column", w=window_w, h=window_h)
    create_customUI()
    cmds.text("version_txt", label="ver.0.01")
    cmds.showWindow(window_name)

def create_customUI():
    cmds.button("rig_button", label="Rigging", w=window_w, h=40, command = create_rigging)  
    cmds.frameLayout("control_scale_frame", label="Control Scale", w=window_w, parent="main_column", bgc=(0.50,0.50,0.5))
    cmds.rowLayout("control_scale_row", nc=3, w=window_w)
    
    cmds.floatField("scale_float_field",precision=2, value=0.25, w=window_w/3)
    cmds.button("small_button", label="Small",w=window_w/3, c="scale_controlers('small')")
    cmds.button("big_button", label="Big",w=window_w/3, c=partial(scale_controlers,'big'))
    
    cmds.frameLayout("control_color_frame", label="Control Color", w=window_w, parent="main_column", bgc=(0.50,0.50,0.5))
    cmds.colorIndexSliderGrp("contorl_color_slider", max = 32)
    cmds.button("set_color_button", label="Set Color", h=30, c=set_controlers_color)


def create_rigging(*args):
    selected = cmds.ls(selection=True)
    if len(selected)==0:
        cmds.warning("No joint selected!!!")
    elif len(selected) > 2:
        cmds.warning("you can select a joint only,or select a joint and a control curve!")
    else:
        if cmds.objectType(selected[0]) != "joint":
            cmds.warning("Joint must be selected first !!!")
        else:
            cmds.select(selected[0], hierarchy = True)
            all_joints = cmds.ls(selection=True)
            joint_num = len(all_joints)
            
            previous_control = None
            new_contorl = None
            for i in range(joint_num):
                if len(selected) == 1:
                    new_control = cmds.circle(name=all_joints[i]+"_ctrl")[0]
                    cmds.rotate(0,90,0, new_control)
                else:
                    new_control = cmds.duplicate(selected[1], name=all_joints[i]+"_ctrl")[0]

                # frezze the attribute and delete history
                cmds.makeIdentity(apply=True)
                cmds.DeleteHistory()
                
                offset_group = cmds.group(name= new_control+"_offset", empty=True)
                cmds.parent(new_control,offset_group)
                
                joint_tr = cmds.xform(all_joints[i], query=True, translation=True, worldSpace=True)
                cmds.xform(offset_group, translation=joint_tr)
                
                orient_cons = cmds.orientConstraint(all_joints[i],offset_group)
                cmds.delete(orient_cons)
                
                cmds.parentConstraint(new_control, all_joints[i])
                
                if previous_control:
                    cmds.parent(offset_group, previous_control)
                    previous_control = new_control
                else:
                    previous_control = new_control


def scale_controlers(mode, *arg):
    sls = cmds.ls(sl=True)
    s = cmds.floatField("scale_float_field", query=True, value=True)
    if mode == "small":
        s *= -1;
    for sl in sls:
        cmds.scale(1+s,1+s,1+s,sl+'.cv[0:]')
       

def set_controlers_color(*arg):
    sls = cmds.ls(sl=True)
    col = cmds.colorIndexSliderGrp("contorl_color_slider", query=True, value=True)
    for sl in sls:
        shape = cmds.listRelatives(sl, children=True)[0]
        cmds.setAttr(shape + '.overrideEnabled', 1)
        cmds.setAttr(shape + '.overrideColor', col-1)
        print(col-1)
       
create_window()

    
    
