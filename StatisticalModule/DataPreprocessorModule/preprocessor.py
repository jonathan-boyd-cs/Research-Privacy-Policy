import sys
sys.path.append('../../')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

class DataLoader:    
    def load_dataset(self, file_path,type):
        dataset = None
        if type == "json":
            dataset = pd.read_json(file_path)
        if type == "csv":
            dataset = pd.read_csv(file_path)
        return dataset

class DataCleaner:
    def clean_null_data(self, dataset, numerical_start_idx, mean_flag=True):
        if mean_flag:
            imputer = SimpleImputer(missing_values=np.nan, strategy= 'mean' )
        else :
            imputer = SimpleImputer(missing_values=np.nan, strategy= 'median' )

        imputer.fit(dataset.iloc[:,numerical_start_idx:])
        dataset = imputer.transform(dataset.iloc[:,numerical_start_idx:])
        return dataset


class DataEncoder:
    def data_encoder_categorical(self, dataset,at):
        ct = ColumnTransformer(
            transformers = [('encoder',OneHotEncoder(), at )], 
            remainder = 'passthrough'
            )
        dataset = ct.fit_transform(dataset)
        return dataset
        
    def data_encoder_binary(self, dataset,at):
        le = LabelEncoder()
        dataset.iloc[:,at] = le.fit_transform(dataset.iloc[:,at])   
        return dataset

class DataSegregator:
    def variable_split_dataset(self, dataset):
        X = dataset.iloc[:, :-1].values
        y = dataset.iloc[:,-1].values
        return X,y

    def ml_data_segregation(self, dataset_X, dataset_y, test_percentage):
        X_train, X_test, y_train, y_test = train_test_split(
            dataset_X,
            dataset_y,
            test_size=(test_percentage),
        )
        return X_train, X_test, y_train, y_test


class DataFeatureScaler:
    def ml_feature_scale(self, dataset_train,dataset_test):
        sc = StandardScaler()
        dataset_train= sc.fit_transform(dataset_train)
        dataset_test= sc.transform(dataset_test)
        return dataset_train, dataset_test



class DataPreprocessor:
    def __init__(self):
        self.__dl = DataLoader()
        self.__de = DataEncoder()
        self.__ds = DataSegregator()
        self.__df = DataFeatureScaler()
        self.__dc = DataCleaner()


    def load(self, file,type):
        data = self.__dl.load_dataset(file,type)
        return data
        
    
    def get_X_y(self, dataset):
        X,y = self.__ds.variable_split_dataset(dataset)
        return X,y
    
    def get_train_test_sets(self,X,y,test_percentage):
        return self.__ds.ml_data_segregation(
            X,y,test_percentage
        )
    
    def encode_categorical(self,dataset, column_s_idx):
        return self.__de.data_encoder_categorical(dataset,column_s_idx)
        
    def encode_binary(self, dataset, column_idx):
        return self.__de.data_encoder_binary(dataset,column_idx)
        
    def feature_scale(self, data_train, data_test):
        return self.__df.ml_feature_scale(
            data_train,
            data_test
        
        )
    def clean_nulls(self,  dataset, numerical_start_idx, mean_flag):
        return self.__dc.clean_null_data( dataset, numerical_start_idx, mean_flag)