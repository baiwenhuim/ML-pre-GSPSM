# ML-pre-GSPSM

Utilize machine learning to predict gene synthesis plant specialized metabolites

1. System requirements
2. Installation guide
3. Demo 
4. Instructions for use
5. License
6. Reference

# 1.  System requirements

The software was tested on CentOS 7.5.1804 (Core) with Miniconda3.
Other packages were used as follows:  

python 3.8.12  
autogluon 0.3.1  
numpy  
scipy  
pandas  

# 2.  Installation guide

**Install miniconda:**
`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh`

**Create a new conda environment and update**

`conda create --name autogluon python==3.8.12`
`conda update -n base conda`

**Activate conda environment**

`conda activate autogluon`

**Install dependencies:**
`pip install -U setuptools wheel`

`pip install autogluon==0.3.1`

**Install ML-pre-GSPSM:** 

`git clone https://github.com/baiwenhuim/ML-pre-GSPSM.git`

# 3.  Demo

The directory including in model script is changed into:  
`cd /ML-pre-GSPSM/model`

Model script is run for prediction of CYP76AD sequences with a simplified data set, by the following command:  
python run_ml.py 

The following results are output into"/Downloaded_directory_path/SVM_E-model/result/":  
●    More accurate five models  
●    Cross validation results in the five models  
●    Test results in the most accurate model  

The demo run time is several minutes.

# 4.  Instructions for use

Enzyme family classification (binary classification) models are enabled to build using your data. Enzyme sequences for training and test data should first be converted into vectors, all using the same feature extractions. Positive and negative datasets should be named "sample_positive.vec" and "sample_negative.vec", respectively. Both files should be found in "/Downloaded_directory_path/SVM_E-model/train/". The test dataset file should be  named "sample_test.vec", and found in "/Downloaded_directory_path/SVM_E-model/test/".

Run time depends on the dataset size and the number of vector dimensions.

# 5.  License

This software is released under the MIT License, according to LICENSE.
