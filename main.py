import sys
sys.path.append("E:/Git/MayaPythonStudy") # 将python目录加入系统路径

import importlib
from OpenMayaScripts import openMayaApi as omapi
importlib.reload(omapi) # 重载模块来维持我们的更新

if __name__ == "__main__":
    omapi.selectionlist_test()
    print("main finished !")
