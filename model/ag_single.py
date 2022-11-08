#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python 
@File    ：ag_tabular.py
@IDE     ：PyCharm 
@Author  ：Wenhui Bai
@Date    ：2022/4/14 19:31 
@contact ：516116998@qq.com
'''
# 单组学预测；5/5增加预测结果与特征重要性整合，修改为多次训练结果；

import sys
#sys.path.append('../')
import basic_func
import pandas as pd


def get_data(path, n, col_name='Seq_feature'):
    omics_name = ['123', 'Genomics', 'Transcriptomics', 'Epigenomics', 'Proteomics', 'others']
    data = pd.read_excel(path, sheet_name=omics_name[n])
    if col_name in data.columns:
        data[col_name] = basic_func.space_aa_seq(data, col_name)
    return data


if __name__ == '__main__':
    # 单组学
    cita = basic_func.get_cita()
    old_Ath = r'../data/123.xlsx'
    for i in range(1, 6):
        all = get_data(old_Ath, i)  # original dataset with multi-omics
        new_Ath = pd.merge(all, cita, on='Gene_Name', how='inner') # Using cita_data's gene name to gain GS dataset with multi-omics features.
        outfile = str(i) + '.csv' 
        basic_func.five_repeat(new_Ath, outfile=outfile)
