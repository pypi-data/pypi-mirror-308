[![License](https://img.shields.io/badge/License-BSD\%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)

# PlasiaCorrelationProfiler

Metaplastic epithelium comprises both tissue-resident and non-resident cells. Tissue non-resident cells are reported to be phenotypically similar to their counterparts in the resident tissue/organ, but their genotypic characteristics may differ. Given the stochastic nature of cancer progression, where cells often acquire genetic alterations independent of change in phenotypic characteristics, we developed a tool to assess whether the non-resident cells of the metaplastic epithelium are genotypically more similar to the normal cells of the resident tissue or to the cancerous cells of the resident tissue. This distinction is crucial for understanding the molecular mechanisms driving metaplasia and its potential role in cancer progression.  

The genotypic similarity between two given cohorts was assessed by estimating the extent of similarity of gene-correlation profile of one cohort with another where, gene-correlations are obtained using the genes that contribute to the extent of metaplasia-associated differentiation (MAD; identified using *Quantplasia*). 

### Global Profile

**Input File Pre-requisites**
* The file should contain gene expression z-scores in .csv format

**Available Parameters**
* User_List : [List] contains list of strings of the .csv files
* Condition : [string] either 'Global' or 'Local' (Please note that we do not recommend the usage of 'Local'. However, this can be used to compare the performance of the tool for both 'Global' and 'Local' profile conditions for a test dataset)

**Optional Parameters**
* Example [string] : Default=None; Otherwise 'Yes' (only to be used when running the tool against the test dataset provided with the package)
* Number_of_Iterations [integer] : Default=500; Otherwise a user-defined value (We recommend a minimum of 500 iterations, however this can be increase or decreased)
* Random_Seed [integer] : Default=A random number between 1 and 1000; Otherwise a user-defined value 
* Column1 [integer] : Default=None; Otherwise a user-defined value to select a column from where the dataset will be filtered (only to be used when running the tool against the test dataset provided with the package as the dataset is considerably large and the analysis may take time)
* Column2 [integer] : Default=None; Otherwise a user-defined value to select a column till where the dataset will be filtered (only to be used when running the tool against the test dataset provided with the package as the dataset is considerably large and the analysis may take time)
* Name [string] : Default=None, Please mention a folder name when using the condition 'Local' so that the gene correlation profiles are calculated and stored in a file before calculating the similarity (only to be used when running the tool for Condition='Local' against the test dataset provided with the package)

**Installation**
```
pip install PlasiaCorrelationProfiler
```

**Use Case 1**
```

#=============================Example Files, and Global Profiler and Local Profiler==========================#
from PlasiaCorrelationProfiler import Normal_path, Synthetic_path, PlasiaGeneCorrelationProfiler


Barretts, Normal, StageI, StageII, StageIII = Normal_path()                                                                           #Path to Example File containing Normal Dataset
N_Barretts, N_StageI, N_StageII, N_StageIII, PseudoNormal_StageIII = Synthetic_path()                                                 #Path to Example File containing Synthetic Dataset
FilePath_List=[Normal, Barretts, StageI, StageII, StageIII, N_Barretts, N_StageI, N_StageII, N_StageIII, PseudoNormal_StageIII]       #Input List of Paths

#PlasiaGeneCorrelationProfiler(User_List, Condition, *Optional Parameters*)                                                           #Main Function

#This example is for Synthetic dataset generated from GSE13898 Global Profile
PlasiaGeneCorrelationProfiler(FilePath_List, Condition='Global', Example='Yes', Seed=345, Number_of_Iterations=500, Column1=1, Column2=800)


#This example is for Synthetic dataset generated from GSE13898 Local profile
PlasiaGeneCorrelationProfiler(FilePath_List, Condition='Local', Example='Yes', Name='GSE13898_Test', Column1=1, Column2=800)

```
**Use Case 2**
```
#=============================User-defined Files and Global Profiler==========================#
#Please note that we do not recommend the use of Local Profiler to examine the datasets for their similarities in the landscape of gene profile correlations as it assumes that each pair of 
#gene-gene correlation is independent and assessed accordingly. However, it can be used to test the tools functionality and compare the same with global profiles

#Please refer to the GitHub page to get examples of user-defined files 

#PlasiaGeneCorrelationProfiler(User_List, Condition, *Optional Parameters*)                                                           #Main Function

#This example is for dataset files as obtained GitHub page for Global Profile
PlasiaGeneCorrelationProfiler(FilePath_List, Condition='Global', Seed=345, Number_of_Iterations=500)


#This example is for dataset files as obtained GitHub page for Global Profile
PlasiaGeneCorrelationProfiler(FilePath_List, Condition='Local', Name='CorrelationsProfiler')
```

**References**  
[1] Chang LJ, Jolly E, Cheong JH, Rapuano KM, Greenstein N, Chen PHA, et al. Endogenous variation in ventromedial prefrontal cortex state dynamics during naturalistic viewing reflects affective experience. Sci Adv. 2021 Apr 23;7(17):eabf7129.  
[2] Eid M, Gollwitzer M, Schmitt M. Statistik und Forschungsmethoden [Statistics and research methods]. 5th ed. Weinheim, Germany: Beltz; 2017.  

COPYRIGHT

Copyright (c) 2024, Pravallika Govada All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

CONTACT INFORMATION

Please address any queries or bug reports to Pravallika Govada at pravallika.govada2018@vitstudent.ac.in or pravallika2606g@gmail.com
