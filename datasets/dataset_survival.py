from __future__ import print_function, division
import math
import os
import pdb
import pickle
import re

import h5py
from PIL import Image
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler

import torch
from torch.utils.data import Dataset

from utils.clam_utils import generate_split, nth


class Generic_WSI_Survival_Dataset(Dataset):
    def __init__(self,
        csv_path = 'dataset_csv/ccrcc_clean.csv', mode = 'omic', apply_sig = False,
        shuffle = False, seed = 7, print_info = True, n_bins = 4, ignore=[],
        patient_strat=True, label_col = None, filter_dict = {}, eps=1e-6):
        r"""
        Generic_WSI_Survival_Dataset 
        """
        self.custom_test_ids = None
        self.seed = seed
        self.print_info = print_info
        self.patient_strat = patient_strat
        self.train_ids, self.val_ids, self.test_ids  = (None, None, None)
        self.data_dir = None

        # ⚠️ 注意：Survival 任务不能像分类那样全局 dtype=str，因为生存期是浮点数。
        # 我们使用 low_memory=False 读取，稍后单独对 ID 列进行字符化
        slide_data = pd.read_csv(csv_path, low_memory=False)

        if 'case_id' not in slide_data:
            slide_data.index = slide_data.index.str[:12]
            slide_data['case_id'] = slide_data.index
            slide_data = slide_data.reset_index(drop=True)

        # 🌟 优化：确保 ID 列一定是字符串，防止丢失 0 填充，也防止后续比对失败
        if 'case_id' in slide_data.columns:
            slide_data['case_id'] = slide_data['case_id'].astype(str)
        if 'slide_id' in slide_data.columns:
            slide_data['slide_id'] = slide_data['slide_id'].astype(str)

        # 🌟 引入 Subtype 的去重逻辑：基于 slide_id 去除重复行 🌟
        if 'slide_id' in slide_data.columns:
            original_len = len(slide_data)
            slide_data = slide_data.drop_duplicates(subset=['slide_id'], keep='first').reset_index(drop=True)
            if print_info and (original_len - len(slide_data) > 0):
                print(f"⚠️ 警告: 发现了 {original_len - len(slide_data)} 个重复的 slide_id，已自动去重。")

        if shuffle:
            np.random.seed(seed)
            # pandas sample 方法更安全
            slide_data = slide_data.sample(frac=1).reset_index(drop=True) 

        if not label_col:
            label_col = 'survival_months'
        else:
            assert label_col in slide_data.columns
        self.label_col = label_col

        patients_df = slide_data.drop_duplicates(['case_id']).copy()
        uncensored_df = patients_df[patients_df['censorship'] < 1]

        disc_labels, q_bins = pd.qcut(uncensored_df[label_col], q=n_bins, retbins=True, labels=False)
        q_bins[-1] = slide_data[label_col].max() + eps
        q_bins[0] = slide_data[label_col].min() - eps
        
        disc_labels, q_bins = pd.cut(patients_df[label_col], bins=q_bins, retbins=True, labels=False, right=False, include_lowest=True)
        patients_df.insert(2, 'label', disc_labels.values.astype(int))

        # 🔥 核心优化：使用 groupby 一次性聚合 patient_dict，消灭原始缓慢的 for 循环！
        if 'slide_id' in slide_data.columns:
            self.patient_dict = slide_data.groupby('case_id')['slide_id'].apply(lambda x: list(set(x))).to_dict()
        else:
            self.patient_dict = {pid: [pid] for pid in patients_df['case_id']}

        slide_data = patients_df
        slide_data.reset_index(drop=True, inplace=True)
        slide_data = slide_data.assign(slide_id=slide_data['case_id'])

        label_dict = {}
        key_count = 0
        for i in range(len(q_bins)-1):
            for c in [0, 1]:
                # print('{} : {}'.format((i, c), key_count))  # 可选关闭无用输出
                label_dict.update({(i, c):key_count})
                key_count+=1

        self.label_dict = label_dict
        
        # 将原始的 iterrows 级别的循环向量化 (如果可能的话，此处保留你的原始逻辑以防出错)
        for i in slide_data.index:
            key = slide_data.loc[i, 'label']
            slide_data.at[i, 'disc_label'] = key
            censorship = slide_data.loc[i, 'censorship']
            key = (key, int(censorship))
            slide_data.at[i, 'label'] = label_dict[key]

        self.bins = q_bins
        self.num_classes=len(self.label_dict)
        patients_df = slide_data.drop_duplicates(['case_id'])
        self.patient_data = {'case_id':patients_df['case_id'].values, 'label':patients_df['label'].values}

        new_cols = list(slide_data.columns[-2:]) + list(slide_data.columns[:-2])
        slide_data = slide_data[new_cols]
        self.slide_data = slide_data
        self.metadata = slide_data.columns[:12]
        self.mode = mode
        self.cls_ids_prep()

        if print_info:
            self.summarize()

        ### Signatures
        self.apply_sig = apply_sig
        if self.apply_sig:
            self.signatures = pd.read_csv('./dataset_csv_sig/signatures.csv')
        else:
            self.signatures = None

        if print_info:
            self.summarize()

    def cls_ids_prep(self):
        self.patient_cls_ids = [[] for i in range(self.num_classes)]        
        for i in range(self.num_classes):
            self.patient_cls_ids[i] = np.where(self.patient_data['label'] == i)[0]

        self.slide_cls_ids = [[] for i in range(self.num_classes)]
        for i in range(self.num_classes):
            self.slide_cls_ids[i] = np.where(self.slide_data['label'] == i)[0]

    def patient_data_prep(self):
        # 🔥 核心优化：移植 Subtype 的 groupby 并行聚合，消灭 $O(N^2)$ 的暴力搜索！
        # 对于 Survival，同一个 case_id 的 label 是唯一的（因为基于病人生存期计算），直接取 first()
        patient_df = self.slide_data.groupby('case_id')['label'].first().reset_index()
        
        self.patient_data = {
            'case_id': patient_df['case_id'].values, 
            'label': patient_df['label'].values
        }

    @staticmethod
    def df_prep(data, n_bins, ignore, label_col):
        mask = data[label_col].isin(ignore)
        data = data[~mask]
        data.reset_index(drop=True, inplace=True)
        disc_labels, bins = pd.cut(data[label_col], bins=n_bins)
        return data, bins

    def __len__(self):
        if self.patient_strat:
            return len(self.patient_data['case_id'])
        else:
            return len(self.slide_data)

    def summarize(self):
        print("label column: {}".format(self.label_col))
        print("label dictionary: {}".format(self.label_dict))
        print("number of classes: {}".format(self.num_classes))
        print("slide-level counts: ", '\n', self.slide_data['label'].value_counts(sort = False))
        for i in range(self.num_classes):
            print('Patient-LVL; Number of samples registered in class %d: %d' % (i, self.patient_cls_ids[i].shape[0]))
            print('Slide-LVL; Number of samples registered in class %d: %d' % (i, self.slide_cls_ids[i].shape[0]))

    def get_split_from_df(self, backbone, patch_size, all_splits: dict, split_key: str='train', scaler=None):
        split = all_splits[split_key]
        split = split.dropna().reset_index(drop=True)

        if len(split) > 0:
            mask = self.slide_data['slide_id'].isin(split.tolist())
            df_slice = self.slide_data[mask].reset_index(drop=True)
            # 请确保 Generic_Split 已正确导入
            split = Generic_Split(df_slice, metadata=self.metadata, mode=self.mode, signatures=self.signatures, data_dir=self.data_dir, label_col=self.label_col, patient_dict=self.patient_dict, num_classes=self.num_classes)
            split.set_backbone(backbone)
            split.set_patch_size(patch_size)
        else:
            split = None
        
        return split

    def return_splits(self, backbone, patch_size = '', from_id: bool=True, csv_path: str=None):
        if from_id:
            if len(self.train_ids) > 0:
                train_data = self.slide_data.loc[self.train_ids].reset_index(drop=True)
                train_split = Generic_Split(train_data, mode = self.mode, metadata= self.apply_sig, data_dir=self.data_dir, num_classes=self.num_classes)
                train_split.set_backbone(backbone)
                train_split.set_patch_size(patch_size)
            else:
                train_split = None

            if len(self.val_ids) > 0:
                val_data = self.slide_data.loc[self.val_ids].reset_index(drop=True)
                val_split = Generic_Split(val_data, metadata = self.apply_sig, mode = self.mode, data_dir=self.data_dir, num_classes=self.num_classes)
                val_split.set_backbone(backbone)
                val_split.set_patch_size(patch_size)
            else:
                val_split = None

            if len(self.test_ids) > 0:
                test_data = self.slide_data.loc[self.test_ids].reset_index(drop=True)
                test_split = Generic_Split(test_data, metadata = self.apply_sig, mode = self.mode, data_dir=self.data_dir, num_classes=self.num_classes)
                test_split.set_backbone(backbone)
                test_split.set_patch_size(patch_size)
            else:
                test_split = None
        else:
            assert csv_path
            # 🌟 强制转换为字符串类型，匹配你的 Subtype 修复逻辑
            self.slide_data['slide_id'] = self.slide_data['slide_id'].astype(str) 
            all_splits = pd.read_csv(csv_path, dtype=self.slide_data['slide_id'].dtype)
            
            train_split = self.get_split_from_df(backbone, patch_size, all_splits=all_splits, split_key='train')
            val_split = self.get_split_from_df(backbone, patch_size, all_splits=all_splits, split_key='val')
            test_split = self.get_split_from_df(backbone, patch_size, all_splits=all_splits, split_key='test')

        return train_split, val_split, test_split
    
    # create_splits 和 set_splits 与之前保持一致
    def create_splits(self, k = 3, val_num = (25, 25), test_num = (40, 40), label_frac = 1.0, custom_test_ids = None):
        settings = {
                    'n_splits' : k, 
                    'val_num' : val_num, 
                    'test_num': test_num,
                    'label_frac': label_frac,
                    'seed': self.seed,
                    'custom_test_ids': custom_test_ids
                    }

        if self.patient_strat:
            settings.update({'cls_ids' : self.patient_cls_ids, 'samples': len(self.patient_data['case_id'])})
        else:
            settings.update({'cls_ids' : self.slide_cls_ids, 'samples': len(self.slide_data)})

        self.split_gen = generate_split(**settings)
    
    def set_splits(self,start_from=None):
        if start_from:
            ids = nth(self.split_gen, start_from)
        else:
            ids = next(self.split_gen)

        if self.patient_strat:
            slide_ids = [[] for i in range(len(ids))] 
            for split in range(len(ids)): 
                for idx in ids[split]:
                    case_id = self.patient_data['case_id'][idx]
                    slide_indices = self.slide_data[self.slide_data['case_id'] == case_id].index.tolist()
                    slide_ids[split].extend(slide_indices)

            self.train_ids, self.val_ids, self.test_ids = slide_ids[0], slide_ids[1], slide_ids[2]
        else:
            self.train_ids, self.val_ids, self.test_ids = ids

    def get_list(self, ids):
        return self.slide_data['slide_id'][ids]

    def getlabel(self, ids):
        return self.slide_data['label'][ids]

    def __getitem__(self, idx):
        return None

    def test_split_gen(self, return_descriptor=False):
        if return_descriptor:
            index = [list(self.label_dict.keys())[list(self.label_dict.values()).index(i)] for i in range(self.num_classes)]
            columns = ['train', 'val', 'test']
            df = pd.DataFrame(np.full((len(index), len(columns)), 0, dtype=np.int32), index= index,
                            columns= columns)

        count = len(self.train_ids)
        print('\nnumber of training samples: {}'.format(count))
        labels = self.getlabel(self.train_ids)
        unique, counts = np.unique(labels, return_counts=True)
        for u in range(len(unique)):
            print('number of samples in cls {}: {}'.format(unique[u], counts[u]))
            if return_descriptor:
                df.loc[index[u], 'train'] = counts[u]
        
        count = len(self.val_ids)
        print('\nnumber of val samples: {}'.format(count))
        labels = self.getlabel(self.val_ids)
        unique, counts = np.unique(labels, return_counts=True)
        for u in range(len(unique)):
            print('number of samples in cls {}: {}'.format(unique[u], counts[u]))
            if return_descriptor:
                df.loc[index[u], 'val'] = counts[u]

        count = len(self.test_ids)
        print('\nnumber of test samples: {}'.format(count))
        labels = self.getlabel(self.test_ids)
        unique, counts = np.unique(labels, return_counts=True)
        for u in range(len(unique)):
            print('number of samples in cls {}: {}'.format(unique[u], counts[u]))
            if return_descriptor:
                df.loc[index[u], 'test'] = counts[u]

        assert len(np.intersect1d(self.train_ids, self.test_ids)) == 0
        assert len(np.intersect1d(self.train_ids, self.val_ids)) == 0
        assert len(np.intersect1d(self.val_ids, self.test_ids)) == 0

        if return_descriptor:
            return df

    def save_split(self, filename):
        train_split = self.get_list(self.train_ids)
        val_split = self.get_list(self.val_ids)
        test_split = self.get_list(self.test_ids)
        df_tr = pd.DataFrame({'train': train_split})
        df_v = pd.DataFrame({'val': val_split})
        df_t = pd.DataFrame({'test': test_split})
        df = pd.concat([df_tr, df_v, df_t], axis=1) 
        df.to_csv(filename, index = False)


class Generic_MIL_Survival_Dataset(Generic_WSI_Survival_Dataset):
    def __init__(self, data_dir, mode: str='path', **kwargs):
        super(Generic_MIL_Survival_Dataset, self).__init__(**kwargs)
        self.data_dir = data_dir
        self.mode = mode
        self.use_h5 = False

    def load_from_h5(self, toggle):
        self.use_h5 = toggle

    def __getitem__(self, idx):
        label = self.slide_data['disc_label'][idx]
        event_time = self.slide_data[self.label_col][idx]
        c = self.slide_data['censorship'][idx]
        # slide_id = self.slide_data['slide_id'][idx]
        case_id = self.slide_data['case_id'][idx]
        # print('2222', case_id)
        slide_ids = self.patient_dict[case_id]
        # print('2222', slide_ids)
        slide_id = []
        for id in slide_ids:
            slide_id.append(id)
        assert len(slide_id) == 1
        slide_id = slide_id[0]

        if type(self.data_dir) == dict:
            source = self.slide_data['source'][idx]
            data_dir = self.data_dir[source]
        elif self.data_dir is None:
            data_dir = self.slide_data['dir'][idx]
        else:
            data_dir = self.data_dir
        
        pt_path = os.path.join(data_dir, 'pt_files', self.backbone, '{}.pt'.format(slide_id))
        # print('1111', pt_path, '111', slide_id)
        features = torch.load(pt_path)
            
        label = torch.LongTensor([label])
        output = {
            'features': features, 'label': label,
            'event_time': event_time,
            'c': c,
        }
        return output


class Generic_MIL_h5_Survival_Dataset(Generic_WSI_Survival_Dataset):
    def __init__(self, data_dir, mode: str='path', **kwargs):
        super(Generic_MIL_h5_Survival_Dataset, self).__init__(**kwargs)
        self.data_dir = data_dir
        self.mode = mode

    def __getitem__(self, idx):
        label = self.slide_data['disc_label'][idx]
        event_time = self.slide_data[self.label_col][idx]
        c = self.slide_data['censorship'][idx]
        # slide_id = self.slide_data['slide_id'][idx]
        case_id = self.slide_data['case_id'][idx]
        slide_ids = self.patient_dict[case_id]
        slide_id = []
        for id in slide_ids:
            slide_id.append(id)
        assert len(slide_id) == 1
        slide_id = slide_id[0]

        data_dir = self.data_dir
        # print('22222', data_dir)
        coords_path = os.path.join(data_dir, 'h5_files', '{}.h5'.format(slide_id))
        
        with h5py.File(coords_path, 'r') as f:
            features = f['features'][:]
        #     coords = f['coords'][:]
            
        label = torch.LongTensor([label])
        output = {
            'features': features, 'label': label,
            'event_time': event_time,
            'c': c,
        }
        return output

class Generic_Split(Generic_MIL_Survival_Dataset):
    def __init__(self, slide_data, metadata, mode, signatures=None, data_dir=None, label_col=None, patient_dict=None, num_classes=2):
        self.use_h5 = False
        self.slide_data = slide_data
        self.metadata = metadata
        self.mode = mode
        self.data_dir = data_dir
        self.num_classes = num_classes
        self.label_col = label_col
        self.patient_dict = patient_dict
        self.slide_cls_ids = [[] for i in range(self.num_classes)]
        for i in range(self.num_classes):
            self.slide_cls_ids[i] = np.where(self.slide_data['label'] == i)[0]

    def __len__(self):
        return len(self.slide_data)

    ### --> Getting StandardScaler of self.genomic_features
    def get_scaler(self):
        scaler_omic = StandardScaler().fit(self.genomic_features)
        return (scaler_omic,)
    ### <--

    ### --> Applying StandardScaler to self.genomic_features
    def apply_scaler(self, scalers: tuple=None):
        transformed = pd.DataFrame(scalers[0].transform(self.genomic_features))
        transformed.columns = self.genomic_features.columns
        self.genomic_features = transformed
    ### <--
    
    def set_backbone(self, backbone):
        print('Setting Backbone:', backbone)
        self.backbone = backbone

    def set_patch_size(self, size):
        print('Setting Patchsize:', size)
        self.patch_size = size

    def pre_loading(self, thread=8):
        # set flag
        self.cache_flag = True

        ids = list(range(len(self)))
        from multiprocessing.pool import ThreadPool
        exe = ThreadPool(thread)
        exe.map(self.__getitem__, ids)