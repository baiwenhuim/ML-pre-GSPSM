# 已导出的文件代码均注释掉
import pandas as pd
from Bio import SeqIO
from Bio import Entrez
from Bio.KEGG import REST
import string
from pandas.core.frame import DataFrame
import os

file_path = r'E:\shenzhen_project\thesis\data\unknown_genes\红豆杉-紫杉醇单体双萜\cds_pep.fa'
hmm_file_path = r'E:\shenzhen_project\thesis\data\unknown_genes\hmm.tblout'
entry_file = r'E:\shenzhen_project\thesis\data\unknown_genes\yingsu_all.txt'
URL_rot = r'E:\shenzhen_project\thesis\data\unknown_genes'
terpenoid_entry = r'E:\shenzhen_project\thesis\data\unknown_genes\罂粟-倍半萜三萜二萜\kegg_access.txt'

# 根据kegg得到的基因id和蛋白序列生成一个pep.fa的文件
def get_pep_file(data):
    with open('psom_pep.fa', 'w') as f:
        for i, j in zip(data['Gene_Name'], data['aa_seqs']):
            gene_id = '>' + str(i)
            gene_seq = j
            f.write(gene_id)
            f.write('\n')
            f.write(gene_seq)
            f.write('\n')


def get_pro_len(file_path):
    pep = SeqIO.parse(file_path, 'fasta')
    gene_id, aas, aas_length = [], [], []
    for i in pep:
        gene_id.append(i.id)
        pro = ' '.join(str(i.seq))
        length = len(str(i.seq))
        aas.append(pro)
        aas_length.append(length)
    return gene_id, aas, aas_length


# 基于pfam预测的结果来提取蛋白域
def get_domain(hmm_file_path):
    hmm = pd.read_table(hmm_file_path, header=None, comment='#')
    domain = []
    temp_id = hmm.iloc[0, 0].split()[2]
    seq_domain = []
    for i in range(hmm.shape[0]):
        if hmm.iloc[i, 0].split()[2] == temp_id:
            temp_domain = hmm.iloc[i, 0].split()[0]
            seq_domain.append(temp_domain)
        else:
            temp_id = hmm.iloc[i, 0].split()[2]
            domain.append(seq_domain)
            seq_domain = []
            seq_domain.append(hmm.iloc[i, 0].split()[0])
    domain.append(seq_domain)
    return domain


# 基于kegg提供的内部API利用kegg物种及entry号下载需要的特征，然后整理成csv文件输出
def download_kegg_features(entry_file, species):
    kegg_id = []  # list of all
    gene_length = []
    motifs = []
    aa_seqs = []
    aa_seq_nums = []
    entry = open(entry_file, 'r')
    entry_name = []
    for line in entry:
        entry_name.append(line.strip())
        # entry_name = line.split(',')
    print(len(entry_name))
    for n in entry_name:
        if n != 113340174:
            num = species + ':' + str(n)
            print(num)
            test = REST.kegg_get(num).read()
            aa_seq = ''
            current_section = None
            for line in test.rstrip().split('\n'):
                section = line[:12].strip()  # section names are within 12 columns
                if not section == "":
                    current_section = section
                # gain entry name
                if current_section == 'ENTRY':
                    entry_id = line[12:].split()[0].strip()
                # gain gene length
                if current_section == "POSITION":
                    if line[12:].split()[0] != 'Unknown':
                        pos = line[12:].split(':')[1]
                        length = pos
                        # length = int(pos.split('..')[1]) - int(pos.split('..')[0])
                    else:
                        length = 0
                # gain motif
                if current_section == "MOTIF":
                    domain = line[12:].split(':')[1].strip()
                # gain motif
                if current_section == "AASEQ":
                    aa_seq += line[12:].strip(string.digits)
            kegg_id.append(entry_id)
            gene_length.append(length)
            motifs.append(domain)
            aa_seqs.append(aa_seq)
            aa_seq_nums.append(len(aa_seq))
        else:
            print('None')
    print(len(gene_length), gene_length)
    print(kegg_id)
    print(aa_seq_nums)
    print(motifs)
    print(len(aa_seqs), aa_seqs)
    # change list to dictionary
    data_dict = {'Gene_Name': kegg_id,
                 'aa_seq_nums': aa_seq_nums,
                  'aa_seqs': aa_seqs,
                  'motifs': motifs,
                  'gene_length': gene_length}
    data = DataFrame(data_dict)
    outfile = species + '.csv'
    data.to_csv(outfile)


# 基于biopythonAPI，利用基因id从gene数据库中下载数据，此处用于下载基因开始和结束的位置
def download_ncbi_gene():
    Entrez.email = "516116998@qq.com"
    handle = Entrez.efetch(db='gene', id='113319259', rettype="fasta",  retmode="text")
    print(handle.read())


# 处理基因长度，现在excel中删除无用的符号（complement（）），然后在pandas处理一下
def gain_gene_length():
    file1 = r'E:\shenzhen_project\thesis\data\unknown_genes\psom.csv'
    data = pd.read_csv(file1, index_col=0, header=0)
    temp = []
    for i in data['gene_length']:
        length = int(i.split('..')[1]) - int(i.split('..')[0])
        temp.append(length)
    data['gene_length'] = temp
    data['label'] = ['Terpenoids' for i in range(data.shape[0])]
    # get_pep_file(data)
    # data.to_csv('psom_features.csv')
    return data


# 给每一个基因都贴上标签
def gain_gene_label():
    data = gain_gene_length()
    mafei_path = r'E:\shenzhen_project\thesis\data\unknown_genes\罂粟-咖啡因-吗啡\mafei.txt'
    with open(mafei_path, 'r') as m:
        sum_id = m.readline()
        id = sum_id.split(',')
    labels = []
    for i in data['Gene_Name']:
        if str(i) in id:
            label = 'Alkaloids'
        else:
            label = 'Phenolics'
        labels.append(label)
    data['label'] = labels
    final_data = data.drop_duplicates(['Gene_Name'], keep='first')
    # get_pep_file(data)
    # data.to_csv('yingsu_features1.csv')
    return final_data


def get_five_features():
    # blastp 结果去重
    blastp_url = os.path.join(URL_rot, 'psom.tbl')
    blast_out = pd.read_table(blastp_url, header=None)
    uni_blast_out = blast_out.drop_duplicates([0], keep='first')
    # orthofinder结果与blastp结果整合
    ortho_url = os.path.join(URL_rot, 'Orthogroups.tsv')
    ortho_out = pd.read_table(ortho_url, header=0, index_col=0)
    ortho_yingsu = ortho_out['yingsu']
    og = []
    gene_list = []
    genes = []
    count = 0
    for i in uni_blast_out[1]:
        for j in ortho_yingsu:
            if str(i) in str(j):
                count += 1
                # print('finish', count)
                og_index = ortho_yingsu[ortho_yingsu.values == j].index  # 根据series里面的值确定索引
                og.append(og_index)
                genes.append(str(i))
                gene_list.append(str(j))
    genes_all = genes + [i for i in uni_blast_out[1] if i not in genes]
    og1 = [list(i) for i in og] + [list('Na') for i in range(uni_blast_out.shape[0]-count)]
    gene_family_size = [len(i) for i in gene_list] + [1 for i in range(uni_blast_out.shape[0]-count)]
    data_dic = {'gene_id': genes_all,
                'othogroup': og1,
                'gene family size': gene_family_size}
    data = pd.DataFrame(data_dic)
    data_size = pd.merge(uni_blast_out, data, how='inner', right_on=data['gene_id'], left_on=uni_blast_out[1])
    uni_data_size = data_size.drop_duplicates([0], keep='first')
    print(uni_data_size)
    family_size = uni_data_size[[0, 'gene family size']]
    # uni_data_size.to_csv('temp.csv')
    # other_feature = gain_gene_label()
    other_feature = gain_gene_length()
    all_features = pd.merge(family_size, other_feature, how='inner',
                            left_on=family_size[0], right_on=other_feature['Gene_Name'])
    all_features.to_csv('yingsu_35_all_features.csv')
    print(all_features)


if __name__ == '__main__':
    print('hello world')
    # download_kegg_features(terpenoid_entry, 'psom')
    get_five_features()

