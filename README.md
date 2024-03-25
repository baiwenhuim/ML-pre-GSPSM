# ML-pre-GSPSM

Utilize automated machine learning to predict gene synthesis plant specialized metabolites

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

And you can also download the pre-trained model in three species (Arabidopsis thaliana, maize, and tomato) from [Zenodo](https://zenodo.org/doi/10.5281/zenodo.10803091).

Once downloaded, you can unzip it:

`unzip azs.zip`

Then, you can use the script predict_unknown_gene.py to predict enzyme genes which you want to predict:

`python predict_unknown_gene.py --path /prefix/model_path/azs --input /prefix/input_file.csv --output output.csv`

The following results are output into"/Downloaded_directory_path/output.csv":  

●    Cross validation results in the basic models and AutoGluon-Tabular  
●    Test results in the AutoGluon-Tabular mode.

Run time depends on the dataset size.

# 4.  License

This software is released under the MIT License, according to LICENSE.
