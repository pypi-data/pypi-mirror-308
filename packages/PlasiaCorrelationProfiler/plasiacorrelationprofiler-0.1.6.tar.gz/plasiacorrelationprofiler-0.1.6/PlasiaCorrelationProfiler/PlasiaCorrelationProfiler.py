# Author: Pravallika Govada

# Contact: pravallika2606g@gmail.com

import os
import warnings
import random
import pandas as pd
import numpy as np
import copy
from copy import deepcopy
import itertools
import csv
from pathlib import Path
import time

import scipy.stats as stats
import scipy
import math

import importlib.resources as ExRes

def Normal_path():
    Barretts_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Barretts.csv'
    Normal_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Normal.csv'
    StageI_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'StageI.csv'
    StageII_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'StageII.csv'
    StageIII_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'StageIII.csv'
    return str(Barretts_file_path), str(Normal_file_path), str(StageI_file_path), str(StageII_file_path), str(StageIII_file_path)

def Synthetic_path():
    NBarretts_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Normal_Barretts.csv'
    NStageI_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Normal_StageI.csv'
    NStageII_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Normal_StageII.csv'
    NStageIII_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'Normal_StageIII.csv'
    Pseudo_Normal_file_path = ExRes.files('PlasiaCorrelationProfiler.data') / 'Synthetic Benchmark Dataset GSE13898' / 'P_Normal_StageIII.csv'
    return str(NBarretts_file_path), str(NStageI_file_path), str(NStageII_file_path), str(NStageIII_file_path), str(Pseudo_Normal_file_path)

def fisher_z_transform(r):
    '''Returns Fisher Z-transformed values
    Args:
        r: Numerical value
    Returns:
        Fisher Z-transformed values of r
    '''
    return 0.5 * np.log((1 + r) / (1 - r))

def upper(df):
    '''Returns the upper triangle of a correlation matrix.
    Args:
        df: correlation matrix
    Returns:
        list of values from upper triangle
    '''
    df = df.values
    mask = np.triu_indices(df.shape[0], k=1)
    return df[mask]

def Global_Profiler(User_List, Random_Seed, Number_of_iterations, **kwargs):
    '''Identifies percentage similarity between global profile of gene correlations between two conditions
       Args:
           User_List: A list of paths or variables with individual paths. The files contain gene expression of 'm' genes 
                       for 'n' samples as column data
           Random_Seed: A numerical value to intialize pseudorandom number generator
           Number_of_iterations: Number of iterations to perform matrix permutations
        Returns:
           Percentage Similarity
    '''
    List_of_Tuples, rhos, Matrix_Names, Correlation_Matrix_List=[], [], [], []
    FC = kwargs.get('FC', None)
    SC = kwargs.get('SC', None)    
    def Correlation_Matrix(DFs):
        '''Generates a dictionary with disease conditions as matrix names stored as keys and respective dataframes of 
            spearman correlations as respective values
            Args:
                DFs: A list of paths or variables with individual paths
            Returns:
                Correlation_Matrix_Dictionary: A dictionary of condition names and spearman correlation values            
        '''
        for File in DFs:
            if '.csv' not in os.path.basename(File):
                raise AssertionError("Expected File type is .csv")
            else:
                Condition_Name=os.path.basename(File)
                Condition_Name_1=Condition_Name.replace('.csv','')            
                if FC==None and SC==None:
                    Reading_File=pd.read_csv(File)
                else:
                    Reading_File=pd.read_csv(File)
                    if FC==None and SC==None:
                        pass
                    else:
                        Reading_File=Reading_File.iloc[:,FC:SC]
            Matrix_Names.append(Condition_Name_1)
            Corr_Gen=pd.DataFrame(Reading_File).corr()
            Correlation_Matrix_List.append(Corr_Gen)
            Correlation_Matrix_Dictionary=dict(zip(Matrix_Names, Correlation_Matrix_List))
        return Correlation_Matrix_Dictionary
    Final_Dict=Correlation_Matrix(User_List)
    def Perform_Spearman(Dictionary_of_Matrix):
        '''Returns Similarity of Global Profile of Gene Correlations
        Args:
            Dictionary containing the Cancer / Disease Condition as keys and their respective upper triangles
            of correlation matrices as values
        Returns:
            Percentage Similarity of Global Profile of Gene Correlations between two datasets as numerical value
        '''
        for k, v in Dictionary_of_Matrix.items():
            for k1, v1 in Dictionary_of_Matrix.items():
                if k==k1:
                    pass
                elif k!=k1:
                    Compared, Compared1=(k, k1), (k1, k)
                    if Compared and Compared1 not in List_of_Tuples:
                        List_of_Tuples.append(Compared)
                        List_of_Tuples.append(Compared1)
                        true_rho, _ = stats.spearmanr(upper(v), upper(v1))
                        print(f"The similarity between {k} and {k1} is {true_rho}\n")
                        true_rho = fisher_z_transform(true_rho)
                        m_ids = list(v.columns)
                        m2_v = upper(v1)
                        for iter in range(Number_of_iterations):
                            np.random.shuffle(m_ids)
                            r, _ = stats.spearmanr((upper(v.loc[m_ids, m_ids])), m2_v)
                            r = fisher_z_transform(r)
                            rhos.append(r)
                        perm_p = ((np.sum(np.abs(true_rho) <= np.abs(rhos)))+1)/(Number_of_iterations+1)
                        print(f"Associated p-value is {perm_p}\n")
                    else:
                        pass
        return
    Perform_Spearman(Final_Dict)
    return

def Local_Profiler(User_List, Folder_Name, **kwargs):
    '''Performs correlation analysis on User list, compares individual gene correlations, computes p-value indicating 
        significance of difference and prints the resultant percentage of similarity
    Args:
        User_List: Input is a list of paths given by the user or can be a list of variables having individual paths 
    Returns:
        Outputs percentage of similarity computed from data post and pre-evaluation of significance of difference between 
        gene correlations of two datasets
    '''
    List_of_Comparison_Files, List_of_Keys_for_SQRT=[], []
    Create_Path=os.path.join(os.path.dirname(User_List[0]), Folder_Name)
    if os.path.isdir(Create_Path):
        raise AssertionError (f"A folder with the same name already exists, please choose a new name or remove the folder from {Create_Path}")
    else:
        Make_Dir=os.mkdir(Create_Path)
        print(f"Folder created at {Create_Path}")
    FC = kwargs.get('FC', None)
    SC = kwargs.get('SC', None)
    def create_correlation_dfs(DFs):
        '''Returns a directory of files with gene correlations calculated from scipy, dictionary of sample sizes and
            corresponding file paths
        Args:
            DFs: A list of paths or variables having individual paths to read and perform correlation
        Returns:
            Dictionary of sample sizes of the datasets and respective file paths containing correlation values
        '''
        for CorrDFs in DFs:
            if '.csv' in os.path.basename(CorrDFs):
                if FC==None and SC==None:
                    ReadingFile=pd.read_csv(CorrDFs)
                else:
                    ReadingFile=pd.read_csv(CorrDFs)
                    ReadingFile=ReadingFile.iloc[:,FC:SC]
            elif '.txt' in os.path.basename(CorrDFs):
                if FC==None and SC==None:
                    ReadingFile=pd.read_csv(CorrDFs, sep='\t')
                else:
                    ReadingFile=pd.read_csv(CorrDFs, sep='\t')
                    ReadingFile=ReadingFile.iloc[:,FC:SC]
            else:
                raise AssertionError("Expected File type is .csv or .txt")
            List_of_Keys_for_SQRT.append(ReadingFile.shape[0])
            features1,features2, correlations, p_values, FZT = [], [], [], [], []
            for First_feature in ReadingFile.columns:
                for Second_feature in ReadingFile.columns:
                    if First_feature != Second_feature:
                        features1.append(First_feature)
                        features2.append(Second_feature)
                        rho, p_value = scipy.stats.spearmanr(ReadingFile[First_feature], ReadingFile[Second_feature])
                        correlations.append(rho)
                        p_values.append(p_value)
            df=pd.DataFrame({'Feature_1': features1,'Feature_2': features2, 'Correlation': correlations, 'p_value': p_values})
            for UTRV in df['Correlation']:
                if UTRV == -1:
                    UTRV=UTRV+0.0001
                    Transformed_values=fisher_z_transform(UTRV)
                    FZT.append(Transformed_values)
                elif UTRV == 1:
                    UTRV=UTRV-0.0001
                    Transformed_values=fisher_z_transform(UTRV)
                    FZT.append(Transformed_values)
                elif UTRV < 1:
                    Transformed_values=fisher_z_transform(UTRV)
                    FZT.append(Transformed_values)
            df['Fisher z Transformed Values'] = FZT
            NewFile=os.path.join(str('r'),os.path.dirname(CorrDFs), Folder_Name,os.path.basename(CorrDFs))
            df.to_csv(NewFile,index=False)
            List_of_Comparison_Files.append(NewFile)
        Sqrt_Dict=dict(zip(List_of_Keys_for_SQRT, List_of_Comparison_Files))
        return Sqrt_Dict
    Dictionary_of_CorrDFs_and_SQRT=create_correlation_dfs(User_List)
    List_of_Tuples=[]
    def Report_Similarity(Dictionary):
        '''Returns Extent of Similarity between individual gene correlations across two datasets as Percetange
        Args:
            Dictionary of sample size as key values for calculating standard error of difference and z-statistic and
            path of files as values
        Returns:
            Percetage similarity between two datasets
        '''
        for SQRT_1, File_Path_1 in Dictionary.items():
            File1=pd.read_csv(File_Path_1)
            File_Type_1=os.path.basename(File_Path_1)
            if '.csv' in File_Type_1:
                NewFT_1=File_Type_1.replace('.csv','')
            elif '.txt' in File_Type_1:
                NewFT_1=File_Type_1.replace('.txt','')
            else:
                raise AssertionError("Expected File type is .csv or .txt")
            for SQRT_2, File_Path_2 in Dictionary.items():
                if File_Path_1==File_Path_2:
                    pass
                else:
                    File2=pd.read_csv(File_Path_2)
                    File_Type_2=os.path.basename(File_Path_2)
                    if '.csv' in File_Type_2:
                        NewFT_2=File_Type_2.replace('.csv','')
                    elif '.txt' in File_Type_2:
                        NewFT_2=File_Type_2.replace('.txt','')
                    else:
                        raise AssertionError("Expected File type is .csv or .txt")
                    Compared, Compared1=(NewFT_1, NewFT_2), (NewFT_2, NewFT_1)
                    if Compared and Compared1 not in List_of_Tuples:
                        List_of_Tuples.append(Compared)
                        List_of_Tuples.append(Compared1)
                        print("Calculating comparison between",NewFT_1, "and", NewFT_2)
                        Final_ComparisonFile=pd.concat([File1,File2], axis=1)
                        Final_ComparisonFile.columns=['Feature_1_1', 'Feature_2_1', 'Correlation_1', 'p_value_1',
                                              'Fisher z Transformed Values_1', 'Feature_1_2', 'Feature_2_2', 'Correlation_2',
                                              'p_value_2', 'Fisher z Transformed Values_2']
                        Final_ComparisonFile.drop(Final_ComparisonFile.columns[[5,6]], axis = 1, inplace=True)
                        X1, X12 = Final_ComparisonFile.shape
                        #print(X1)
                        Final_ComparisonFile=Final_ComparisonFile[(Final_ComparisonFile['p_value_1']<=0.05) & (Final_ComparisonFile['p_value_2']<=0.05)]
                        X2, X22 = Final_ComparisonFile.shape
                        if X2!=0:
                            X2=X2
                        else:
                            X2=X2 + (0.0000000001)
                        #print(X2)
                        Final_ComparisonFile['DegofFreedom']=np.sqrt((1/(SQRT_1-3))+(1/(SQRT_2-3)))
                        Final_ComparisonFile['Difference']=Final_ComparisonFile['Fisher z Transformed Values_1']-Final_ComparisonFile['Fisher z Transformed Values_2']
                        Final_ComparisonFile['Z_statistic']=Final_ComparisonFile['Difference']/Final_ComparisonFile['DegofFreedom']
                        Final_ComparisonFile['Psychometric_p_val']=scipy.stats.norm.sf(abs(Final_ComparisonFile['Z_statistic']),0,1)*2
                        Final_ComparisonFile=Final_ComparisonFile[Final_ComparisonFile['Psychometric_p_val']<=0.05]
                        X3, X32 = Final_ComparisonFile.shape
                        #print(X3)
                        Similarity=(1-(X3/X2))*100
                        print("Similarity Calculated: The similairity between",NewFT_1, "and", NewFT_2, "is", Similarity, '\n')
                    else:
                        pass      
        return
    Report_Similarity(Dictionary_of_CorrDFs_and_SQRT)
    return

def PlasiaGeneCorrelationProfiler(User_List, Condition, **kwargs):
    Example = kwargs.get('Example', None)
    Iterations = kwargs.get('Number_of_Iterations', 500)
    Seed = kwargs.get('Random_Seed', random.randint(1, 1000))
    First_Column = kwargs.get('Column1', None)
    Second_Column = kwargs.get('Column2', None)
    Folder_Name = kwargs.get('Name', None)

    if Condition=='Global' and Example==None:
        if First_Column!=None and Second_Column!=None:
            raise AssertionError("Please remove 'Column1' and 'Column2' if you have specified column numbers. The values are only for the purpose of example files provided with this software package")
        else:
            Global_Profiler(User_List, Seed, Iterations)
    elif Condition=='Global' and Example=='Yes':
        warnings.warn("Please ensure you are providing your intended values for Column1 and Column2 which will select a subset of columns to perform analysis. Otherwise the calculations will take a very long time for default number of iterations", UserWarning) 
        Global_Profiler(User_List, Seed, Iterations, FC=First_Column, SC=Second_Column)
    elif Condition=='Local' and Example==None:
        print(f"Please note that we do not recommend this method, as each pair of gene-gene correlations is assessed independently, followed by the identification of the percentage of significantly different pairs, which indirectly provides a measure of similarity.\n")
        if First_Column!=None and Second_Column!=None:
            raise AssertionError("Please remove 'Column1' and 'Column2' if you have specified column numbers. The values are only for the purpose of example files provided with this software package")
        else:
            Local_Profiler(User_List, Folder_Name)
    elif Condition=='Local' and Example=='Yes':
        print(f"Please note that we do not recommend this method, as each pair of gene-gene correlations is assessed independently, followed by the identification of the percentage of significantly different pairs, which indirectly provides a measure of similarity.\n")
        warnings.warn("Please ensure you are providing your intended values for Column1 and Column2 which will select a subset of columns to perform analysis. Otherwise the calculations will take a very long time for default number of iterations", UserWarning)
        Local_Profiler(User_List, Folder_Name, FC=First_Column, SC=Second_Column)
    elif Condition==None:
        print("Please provide a valid condition. See documentation for types of conditions available")