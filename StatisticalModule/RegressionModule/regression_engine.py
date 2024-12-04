import sys
sys.path.append('../../')
from FileManager.file_manager import FileManager
from DataStorageModule.GraphicalStorageModule.dataframe_store import CSVToDataFrameStore
from StatisticalModule.DataPreprocessorModule.preprocessor import DataPreprocessor
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print



class RegressionCreator:

    def __init__(self, outputDirectory):
        self.__outputDirectory = outputDirectory



    def regression_model(self, X_train, X_test, y_train, y_test, xlabel,ylabel, title):
        regressor = LinearRegression()
        X_train = X_train.reshape(-1,1)
        regressor.fit(
            X_train, y_train
        )
        #y_predictions = regressor.predict(X_test)
        self.__visualization(regressor, X_train, X_test, y_train, y_test,xlabel,ylabel, title)

    def __visualization(self,regressor,  X_train, X_test, y_train, y_test, xlabel,ylabel,title):
        # TRAIN
        plt.clf()
        plt.scatter(x=X_train, y=y_train,
                    color = 'red')
        plt.plot(X_train, regressor.predict(X_train),
                 color = 'blue')
        plt.title('Training Set-{}'.format(title))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        self.__save_pdf('train-regression-model-{}'.format(title))

        

        # TEST
        plt.clf()
        plt.scatter(X_test, y_test,
                    color = 'red')
        plt.plot(X_train, regressor.predict(X_train),
                 color = 'blue')
        plt.title('Test Set-{}'.format(title))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
       
        self.__save_pdf('test-regression-model-{}'.format(title))



    def __save_pdf(self,tag):
        m = time_stamped_msg(tag)
        plt.savefig(
            fname="{}{}-{}.pdf".format(self.__outputDirectory,'regression',m),
            orientation='landscape',
            format='pdf',
            bbox_inches='tight'
        )

class RegressionEngine(RegressionCreator):
    def __init__(self, name, outputDirectory, errLogDirectory, verbose):
        super().__init__(outputDirectory)
        self.__name = name
        self.__outputDirectory = outputDirectory
        self.__file_manager = FileManager(name, errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg("{}-regression-engine".format(name))
        self.__err_database = ErrorDatabase(m)
        
    def set_output_directory(self, directory):
        self.__file_manager.assure_directory(directory)
        self.__outputDirectory = directory
    
    def regression(self, X_train, X_test, y_train, y_test, xlabel,ylabel, title):
        self.regression_model(X_train, X_test, y_train, y_test, xlabel,ylabel, title)