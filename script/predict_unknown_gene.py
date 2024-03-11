import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
import sys
import warnings
import random
warnings.filterwarnings('ignore')  # 忽略警告
pd.set_option('display.max_rows', None)


# 加载模型并预测新基因（只需预测一次）
def load_model(save_path, test_data, out_path):  # save_path 原来模型存储路径
    label = 'label'
    extra_metric = ['accuracy', 'f1_weighted', 'roc_auc_ovo_macro', 'precision_weighted', 'recall_weighted']

    predictor = TabularPredictor.load(save_path)  # 加载模型
    y_test = test_data[label]  # values to predict
    test_data_nolab = test_data.drop(columns=[label])  # delete label column to prove we're not cheating
    test_data_nolab.head()
    y_pred = predictor.predict(test_data_nolab)
    print("Predictions:  \n", y_pred)
    perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred, auxiliary_metrics=True)
    print(perf)
    pre_test = predictor.leaderboard(test_data, extra_metrics=extra_metric)
    pre_test.to_csv(out_path)


if __name__ == '__main__':
    asz_path = r'/home/baiwenhui/SM_project/predict-sly/Model_tabular/asz-z_'
    test_path = r'/home/baiwenhui/SM_project/predict-sly/yingsu_all_features.csv'
    test_data = pd.read_csv(test_path).drop(['Gene_Name'], axis=1)
    test_data['aa_seq'] = [' '.join(str(i)) for i in test_data['aa_seq']]
    for i in range(1, 6):
        save_path = str(asz_path) + str(i)
        out_path = 'unknown_gene_pre' + str(i) + '.csv'
        load_model(save_path, test_data, out_path)