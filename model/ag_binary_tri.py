#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python
@File    ：ag_tabular_binary_tri.py
@IDE     ：PyCharm
@Author  ：Wenhui Bai
@Date    ：2022/5/10 11:11
@contact ：516116998@qq.com
'''
import sys
sys.path.append('../../')
# current_dir = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(current_dir)
import basic_func
import pandas as pd


def get_binary_tri_data(all):
    all = all.drop('Gene_Name', axis=1)
    t_p = all[(all['label'] == 'Terpenoids') | (all['label'] == 'Phenolic')]
    t_a = all[(all['label'] == 'Terpenoids') | (all['label'] == 'Alkaloids')]
    a_p = all[(all['label'] == 'Alkaloids') | (all['label'] == 'Phenolic')]
    return t_p, t_a, a_p


if __name__ == '__main__':
    # 三个参数 第一个是文件路径，第二个是组学位置，第三个是输出文件名
    Cita_file_path = r'/home/baiwenhui/auto-ML-SM/Citation_training_data.csv'
    Cita = pd.read_csv(Cita_file_path, usecols=['Gene_Name'])
    old_Ath = r'/home/baiwenhui/auto-ML-SM/Ath_binary_multi/123.xlsx'  # r'E:\shenzhen_project\thesis\result\ath_binary_tri\123.xlsx'
    all = pd.read_excel(old_Ath)
    col_name = 'Seq_feature'
    all[col_name] = basic_func.space_aa_seq(all, col_name)
    #new_Ath = pd.merge(all, Cita, on='Gene_Name', how='inner')  # 将引用数据与特征数据进行合并得到570个数据
    #print(new_Ath.shape)
    t_p, t_a, a_p = get_binary_tri_data(all)
    print(t_p.shape, t_a.shape, a_p.shape)
    basic_func.five_repeat(all, outfile='123.csv')
    basic_func.five_repeat(t_p, outfile='12.csv')
    basic_func.five_repeat(t_a, outfile='13.csv')
    basic_func.five_repeat(a_p, outfile='23.csv')

