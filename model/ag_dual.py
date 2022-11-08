#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python 
@File    ：ag_tabular_multi_omics.py
@IDE     ：PyCharm 
@Author  ：Wenhui Bai
@Date    ：2022/4/19 16:21 
@contact ：516116998@qq.com
'''
import sys
#sys.path.append('../')
import basic_func
import pandas as pd


def get_data(path, n, m, col_name='Seq_feature'):
    omics_name = ['123', 'Genomics', 'Transcriptomics', 'Epigenomics', 'Proteomics', 'others']
    test1 = pd.read_excel(path, sheet_name=omics_name[n])
    test2 = pd.read_excel(path, sheet_name=omics_name[m]).drop(['Gene_Name', 'label'], axis=1)
    data = test1.join(test2)
    if col_name in data.columns:
        data[col_name] = basic_func.space_aa_seq(data, col_name)
    return data


if __name__ == '__main__':
    # 双组学
    cita = basic_func.get_cita()
    old_Ath = r'../data/123.xlsx'
    for i in range(1, 5):
        for j in range(i+1, 6):
            all = get_data(old_Ath, i, j)
            new_Ath = pd.merge(all, cita, on='Gene_Name', how='inner')
            outfile = str(i) + str(j) + '.csv'
            basic_func.five_repeat(new_Ath, outfile=outfile)
