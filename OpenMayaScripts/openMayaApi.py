import maya.OpenMaya as om

# 选择列表 DAG MObject MSelectionList
def selectionlist_test():
    print("selectionlist_test is running!")

    # 如果有重名，需要写出父级，直到可以区分彼此
    mSelectionList = om.MSelectionList()
    mSelectionList.add("pSphere4|pSphere6")

    mDagPath = om.MDagPath()
    mSelectionList.getDagPath(0, mDagPath)
    print("fullPathName:" + mDagPath.fullPathName())

    # DependNode 依赖节点
    mObj = om.MObject()
    mSelectionList.getDependNode(0, mObj)
    print("apiType:" + mObj.apiTypeStr())

# 修改参数
def modified_attribute_test():
    print("modified_attribute_test is running!")
