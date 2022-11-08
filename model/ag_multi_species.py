import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
import sys
import warnings
import random
warnings.filterwarnings('ignore')  # 忽略警告


def get_cita():
    cita_file_path = r'../data/Citation_training_data.csv'
    cita = pd.read_csv(cita_file_path, usecols=['Gene_Name', 'label', 'gene_legth', 'gene_family_size',	'aa_seq',
                                                'aa_seq_length', 'Domain'])
    return cita


def get_train_test_data(data, seed=42):
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


def five_repeat(data1, data2, outfile):
    for i in range(1, 6):
        train_data, test_data = data1, data2
        out_name = str(outfile).split('.')[0] + '_' + str(42)
        path = './Model_tabular/' + out_name

        predictor = training(train_data, path)
        pre_result = testing(predictor, test_data)
        # 获取特征重要性 最终的混合模型就不用计算feature importance
        # fea_import = predictor.feature_importance(data=test_data, num_shuffle_sets=5)
        # result = pd.concat([pre_result, fea_import])
        result = pre_result
        finally_out = out_name + '.csv'
        result.to_csv(finally_out)
        print('finish %d' % i)
        break
    return True


def get_three_species_data(all):
    ath = all.loc[all['Gene_Name'].str.contains('AT')]  # 拟南芥含AT, 玉米含Zm, 番茄含Soly
    sly = all.loc[all['Gene_Name'].str.contains('So')]
    zma = all.loc[all['Gene_Name'].str.contains('Zm')]
    return ath, sly, zma


if __name__ == '__main__':
    # 三组学
    cita = get_cita()
    ath, sly, zma = get_three_species_data(cita)
    ath_sly = ath.append(sly)
    ath_zma = ath.append(zma)
    sly_zma = sly.append(zma)
    ath_train_data, ath_test_data = get_train_test_data(ath)
    all_data = ath_train_data.append(sly_zma)
    #five_repeat(ath_train_data, ath_test_data, outfile='1.csv')
    # Train a multi species three classification;
    five_repeat(all_data, ath_test_data, outfile='123.csv')
    #five_repeat(sly, ath, outfile='21.csv')
    #five_repeat(zma, ath, outfile='31.csv')
    #five_repeat(sly, zma, outfile='23.csv')
    #five_repeat(ath_sly, zma, outfile='12_3.csv')
    #five_repeat(ath_zma, sly, outfile='13_2.csv')
    #five_repeat(sly_zma, ath, outfile='23_1.csv')
