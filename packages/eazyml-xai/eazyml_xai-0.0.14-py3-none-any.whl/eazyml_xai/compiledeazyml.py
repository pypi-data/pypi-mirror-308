import sys
import importlib
from importlib import abc

class CythonPackageMetaPathFinder(importlib.abc.MetaPathFinder):
    def __init__(self, name_filter):
        super(CythonPackageMetaPathFinder, self).__init__()
        self.name_filter = name_filter
    
    def find_module(self, fullname, path):
        if fullname.startswith(self.name_filter):
           return importlib.machinery.ExtensionFileLoader(fullname, __file__)

def libeazymlxaipython_cython_submodule():
    sys.meta_path.append(CythonPackageMetaPathFinder("eazyml_xai."))
    sys.meta_path.append(CythonPackageMetaPathFinder("eazyml_xai.xai."))
