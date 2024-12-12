#!/usr/bin/env python3



import matplotlib.pyplot as plt
from ErrorHandleModule.general import time_stamped_msg
from FileManager.file_manager import FileManager
import random

class PDFGenerator:
    """
        Class utilized to generate matplotlib.pyplot pdf output.
    """
    def __init__(self, outputDirectory, errLogDirectory, verbose):
        m = time_stamped_msg('pdf_generator-{}'.format(random.randint(2,200)))
        self.__file_manager = FileManager(m,errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        self.__outputDirectory = outputDirectory
        
    def save_pdf(self,tag : str,title : str):
        m = time_stamped_msg('{}-{}'.format(tag,title))
        plt.savefig(
            fname="{}{}.pdf".format(self.__outputDirectory,m),
            orientation='landscape',
            format='pdf',
            bbox_inches='tight'
        )
