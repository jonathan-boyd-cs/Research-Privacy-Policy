#!/usr/bin/env python3


"""

    Class serves to ensure file paths exist and
        to relocate files as necessary.
    

"""

import sys
sys.path.append('../')
import subprocess
import os
from ErrorHandleModule.general import time_stamped_msg, maybe_print


class FileManager:
    """
        Helper class used throughout codebase to ensure file paths exist and
        to relocate files.
    
    """
    def __init__(self, name, errLogDirectory, verbose=True):
        self.__name = name
        self.__verbose = verbose
        m = time_stamped_msg("policy-analysis-suite-{}".format(name))
        self.__errLogDirectory = errLogDirectory
    
    def __post_init__(self):
        self.assure_directory(self.__errLogDirectory)


    def assure_directory(self,relative_path_string):
        """
            Ensure a directory exists, creating it if it does not.
        
        """
        try:
            idx = [i for i,x in enumerate(relative_path_string) if x=='/']    
            for i in idx:
                dir = relative_path_string[0:i+1]
                if not os.path.exists(dir):
                    self.dir_creator(dir)
        except Exception as e:
            
            raise(e)
        
    def dir_creator(self, directory):
        try:
            if not os.path.exists(directory):
                subprocess.run(["mkdir", directory  ])
                maybe_print(self.__verbose,"(FileManager-{}) created {}...".format(
                self.__name,directory
            ))
        except Exception as e:
           
            raise(e)

    def copy_rename(self, path, new_path):
        try:
            self.assure_directory(new_path)
            subprocess.run(['cp',path,new_path])
            maybe_print(self.__verbose,"(FileManager-{}) copied {} as {}...".format(
                self.__name,path,new_path
            ))
        except Exception as e:
            
            raise(e)

        
    def move_rename(self, path, new_path):
        try:
            self.assure_directory(new_path)
            subprocess.run(['mv',path,new_path])
            maybe_print(self.__verbose,"(FileManager-{}) moved {} to {}...".format(
                self.__name,path,new_path
            ))
        except Exception as e:
            
            raise(e)

        
  