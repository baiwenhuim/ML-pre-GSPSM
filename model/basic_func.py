import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
import sys
import warnings
import random
warnings.filterwarnings('ignore')  # 忽略警告


def space_aa_seq(df, col_name):
    aa_seqs = df[col_name].to_list()
    new_aa_seqs = []
    for aa_seq in aa_seqs:
        temp = ' '.join(str(aa_seq))
        new_aa_seqs.append(temp)
    return new_aa_seqs


def get_cita():
    cita_file_path = r'/home/baiwenhui/auto-ML-SM/Citation_training_data.csv'
    cita = pd.read_csv(cita_file_path, usecols=['Gene_Name'])
    return cita

def get_binary_tri_data(all):
    all = all.drop('Gene_Name', axis=1)
    t_p = all[(all['label'] == 'Terpenoids') | (all['label'] == 'Phenolic')]
    t_a = all[(all['label'] == 'Terpenoids') | (all['label'] == 'Alkaloids')]
    a_p = all[(all['label'] == 'Alkaloids') | (all['label'] == 'Phenolic')]
    return t_p, t_a, a_p


def get_train_test_data(data, seed):
    data_label = data['label']
    data_set = data.drop('label', axis=1)
    train_data, test_data, train_label, test_label = train_test_split(data_set, data_label, test_size=0.2,
                                                                      random_state=seed)
    train_data = train_data.join(train_label)
    test_data = test_data.join(test_label)
    return train_data, test_data


def training(train_data, path):
    # 训练参数
    label = 'label'
    time_limit = 1000
    excluded_model_types = ['KNN', 'NN_TORCH', 'custom']
    # 训练
    predictor = TabularPredictor(label=label, path=path).fit(train_data, time_limit=time_limit, presets='best_quality',
                                                             num_bag_folds=5, excluded_model_types=excluded_model_types)
    return predictor


def testing(predictor, test_data):
    # 使用不同的评价标准来评价模型，在测试数据集上
    extra_metric = ['accuracy', 'f1_weighted', 'roc_auc_ovo_macro', 'precision_weighted', 'recall_weighted']
    pre_result = predictor.leaderboard(test_data, extra_metrics=extra_metric)
    return pre_result


def five_repeat(data, outfile):
    for i in range(1, 6):
        train_data, test_data = get_train_test_data(data, i)
        out_name = str(outfile).split('.')[0] + '_' + str(i)
        path = './Model_tabular/' + out_name

        predictor = training(train_data, path)
        pre_result = testing(predictor, test_data)
        # 获取特征重要性
        fea_import = predictor.feature_importance(data=test_data, num_shuffle_sets=5)
        result = pd.concat([pre_result, fea_import])
        finally_out = out_name + '.csv'
        result.to_csv(finally_out)
    return True
