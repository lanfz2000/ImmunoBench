from .dataset_generic import Generic_MIL_Dataset, Generic_MIL_pt_Dataset
from .dataset_survival import Generic_MIL_Survival_Dataset, Generic_MIL_h5_Survival_Dataset
import os


def get_survival_dataset(task, seed=119, data_root_dir = None):
    study = '_'.join(task.split('_')[:2])
    # print('111', study)
    if study == 'tcga_kirc' or study == 'tcga_kirp':
        combined_study = 'tcga_kidney'
    elif study == 'tcga_luad' or study == 'tcga_lusc':
        combined_study = 'tcga_lung'
    else:
        # combined_study = study
        combined_study = task
    # combined_study = combined_study.split('_')[1]
    # csv_path = 'dataset_csv/survival_by_case/{}_Splits.csv'.format(combined_study)
    csv_path = 'dataset_csv_lanfz/{}.csv'.format(combined_study)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(csv_path)
    
    # dataset = Generic_MIL_Survival_Dataset(csv_path = 'dataset_csv/%s_processed.csv' % combined_study,
    print(csv_path)
    # dataset = Generic_MIL_Survival_Dataset(csv_path=csv_path,
    #                                         data_dir=data_root_dir,
    #                                         shuffle=False, 
    #                                         seed=seed, 
    #                                         print_info = True,
    #                                         patient_strat= True,
    #                                         n_bins=4,
    #                                         label_col = 'survival_months',
    #                                         ignore=[])
    print('11111??')
    dataset = Generic_MIL_Survival_Dataset(csv_path=csv_path,
                                            data_dir=data_root_dir,
                                            shuffle=False, 
                                            seed=seed, 
                                            print_info = True,
                                            patient_strat = True,
                                            n_bins=4,
                                            label_col = 'survival_months',
                                            ignore=[])
    return dataset


def get_subtying_dataset(task, seed=119, data_dir=None):
    if task == 'LUAD_LUSC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv/LUAD_LUSC.csv',
                                data_dir= data_dir,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'LUAD':0, 'LUSC':1},
                                patient_strat=True,
                                ignore=[])

    elif task == 'DLBCL_Morph':
        # print('2222here')
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv/DLBCL_Morph.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'stage1':0, 'stage2':1, 'stage3':2, 'stage4':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'DLBCL_Morph_HE':
        # print('2222here')
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/DLBCL_Morph_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'stage1':0, 'stage2':1, 'stage3':2, 'stage4':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'DLBCL_Morph_IHC':
        # print('2222here')
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/DLBCL_Morph_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'stage1':0, 'stage2':1, 'stage3':2, 'stage4':3},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'CK7_B1':
        # print('2222here')
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/CK7_B1_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'ER_B1':
        # print('2222here')
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/ER_B1_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'PR_B1':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/PR_B1_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'P63_B1':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/P63_B1_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'PD_L1_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/PD_L1_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'P40_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/P40_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'NapsinA_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/NapsinA_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'CDX2_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/CDX2_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'P53_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/P53_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'Wild-type expression':0, 'Mutant expression':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'Histai_P53_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/Histai_P53_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'PSA_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/PSA_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'AR_breast':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/AR_breast_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HER2_breast':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HER2_breast_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'score_0':0, 'score_1':1, 'score_2':2, 'score_3':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'S100_B1':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/S100_B1_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_malignant_benign':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_malignant_benign_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'benign':0, 'malignant':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_malignant_benign_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_malignant_benign_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'benign':0, 'malignant':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_malignant_benign_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_malignant_benign_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'benign':0, 'malignant':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_subtype':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_subtype_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'IDC':0, 'ILC':1, 'DCIS':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_subtype_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_subtype_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'IDC':0, 'ILC':1, 'DCIS':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'breast_subtype_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/breast_subtype_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'IDC':0, 'ILC':1, 'DCIS':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'brain_subtype':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/brain_subtype_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'brain_subtype_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/brain_subtype_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'brain_subtype_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/brain_subtype_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'Ki_67_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/Ki_67_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'score_10':0, 'score_20':1, 'score_30':2, 'score_40':3, 'score_50':4, 'score_60':5, 'score_70':6, 'score_80':7, 'score_90':8},
                                patient_strat= True,
                                ignore=[])

    elif task == 'InUIT':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/InUIT_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])
    elif task == 'InUIT_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/InUIT_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'InUIT_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/InUIT_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'meningioma':0, 'glioma':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'CK56_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/CK56_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'SYN_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/SYN_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'GATA3_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/GATA3_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'P16_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/P16_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'CD34_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/CD34_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'PAX8_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/PAX8_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'TTF1_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/TTF1_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'D2_40_pancancer':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/D2_40_pancancer_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ_BCL2':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_BCL2_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ_CD10':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_CD10_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ_EBER':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_EBER_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ_CD20':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_CD20_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'positive':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'NK-T':0, 'FL':1, 'DLBCL':2, 'AITL':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_RJ_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'NK-T':0, 'FL':1, 'DLBCL':2, 'AITL':3},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'lymphoma_RJ_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_RJ_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'NK-T':0, 'FL':1, 'DLBCL':2, 'AITL':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'lymphoma_JY':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/lymphoma_JY_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'DLBCL':0, 'NK-T':1, 'AITL':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'Breast_RCB_X':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/Breast_RCB_X_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0.0':0, '1.0':1, '2.0':2, '3.0':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'Breast_RCB_X_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/Breast_RCB_X_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0.0':0, '1.0':1, '2.0':2, '3.0':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'Breast_RCB_X_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/Breast_RCB_X_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0.0':0, '1.0':1, '2.0':2, '3.0':3},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'HE_Ki67_Ki67predictScore':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_Ki67predictScore_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'Score_0':0, 'Score_1':1, 'Score_2':2, 'Score_3':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_HEpredictKi67Score':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_HEpredictKi67Score_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'Score_0':0, 'Score_1':1, 'Score_2':2, 'Score_3':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_infiltration_of_rete_testis':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_infiltration_of_rete_testis_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'without infiltration':0, 'infiltrated':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_infiltration_of_rete_testis_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_infiltration_of_rete_testis_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'without infiltration':0, 'infiltrated':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_infiltration_of_rete_testis_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_infiltration_of_rete_testis_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'without infiltration':0, 'infiltrated':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'HE_Ki67_tumour_pTNM_staging':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_tumour_pTNM_staging_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'pT1':0, 'pT2':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_tumour_pTNM_staging_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_tumour_pTNM_staging_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'pT1':0, 'pT2':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HE_Ki67_tumour_pTNM_staging_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HE_Ki67_tumour_pTNM_staging_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'pT1':0, 'pT2':1},
                                patient_strat= True,
                                ignore=[])


    elif task == 'BREAST_IMPRESS_HER2_DEID_pCR':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_HER2_DEID_pCR_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_HER2_DEID_pCR_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_HER2_DEID_pCR_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_HER2_DEID_pCR_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_HER2_DEID_pCR_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'BREAST_IMPRESS_TNBC_DEID_pCR':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_pCR_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_TNBC_DEID_pCR_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_pCR_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_TNBC_DEID_pCR_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_pCR_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_TNBC_DEID_residualTumor':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_residualTumor_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_TNBC_DEID_residualTumor_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_residualTumor_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'BREAST_IMPRESS_TNBC_DEID_residualTumor_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/BREAST_IMPRESS_TNBC_DEID_residualTumor_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_recurrence':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_recurrence_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_recurrence_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_recurrence_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_recurrence_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_recurrence_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'HANCOCK_progress':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_progress_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_progress_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_progress_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_progress_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_progress_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[])
        
    elif task == 'HANCOCK_metastasis':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_metastasis_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_metastasis_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_metastasis_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_metastasis_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_metastasis_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_adjuvant_radiotherapy':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_radiotherapy_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_adjuvant_radiotherapy_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_radiotherapy_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_adjuvant_radiotherapy_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_radiotherapy_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_adjuvant_systemic_therapy':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_systemic_therapy_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_adjuvant_systemic_therapy_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_systemic_therapy_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_adjuvant_systemic_therapy_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_adjuvant_systemic_therapy_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_surviva_status':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'living':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_surviva_status_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'living':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_surviva_status_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'living':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HANCOCK_surviva_status_with_cause':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_with_cause_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'deceased not tumor specific':1, 'deceased tumor specific':2,
                                              'living':3},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_surviva_status_with_cause_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_with_cause_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'deceased not tumor specific':1, 'deceased tumor specific':2,
                                              'living':3},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_surviva_status_with_cause_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_surviva_status_with_cause_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'deceased':0, 'deceased not tumor specific':1, 'deceased tumor specific':2,
                                              'living':3},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_histologic_type':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_histologic_type_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'SCC_Basaloid':0, 'SCC_Conventional-Keratinizing':1, 'SCC_Conventional-NonKeratinizing':2,
                                              'Other':3},
                                patient_strat= True,
                                ignore=[]) 
    
    elif task == 'HANCOCK_histologic_type_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_histologic_type_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'SCC_Basaloid':0, 'SCC_Conventional-Keratinizing':1, 'SCC_Conventional-NonKeratinizing':2,
                                              'Other':3},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_histologic_type_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_histologic_type_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'SCC_Basaloid':0, 'SCC_Conventional-Keratinizing':1, 'SCC_Conventional-NonKeratinizing':2,
                                              'Other':3},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_grading':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_grading_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'G1':0, 'G2':1, 'G3':2},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_grading_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_grading_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'G1':0, 'G2':1, 'G3':2},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_grading_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_grading_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'G1':0, 'G2':1, 'G3':2},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Metastatic':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Metastatic_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Metastatic_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Recurrence':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Recurrence_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'HANCOCK_Radiotherapy_Recurrence_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    # 新加治疗和预后 (HANCOCK)
    elif task == 'HANCOCK_Radiotherapy_Metastatic':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Radiotherapy_Metastatic_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Radiotherapy_Metastatic_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Metastatic_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_Radiotherapy_Recurrence':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Radiotherapy_Recurrence_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Radiotherapy_Recurrence_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Radiotherapy_Recurrence_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_Chemotherapy_Metastatic':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Metastatic_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
    elif task == 'HANCOCK_Chemotherapy_Metastatic_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Metastatic_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
    elif task == 'HANCOCK_Chemotherapy_Metastatic_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Metastatic_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
        
    elif task == 'HANCOCK_Chemotherapy_Recurrence':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Recurrence_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Chemotherapy_Recurrence_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Recurrence_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Chemotherapy_Recurrence_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Chemotherapy_Recurrence_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
        
    elif task == 'HANCOCK_Surgery_Metastatic':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Metastatic_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
    elif task == 'HANCOCK_Surgery_Metastatic_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Metastatic_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
    elif task == 'HANCOCK_Surgery_Metastatic_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Metastatic_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'non-metastatic':0, 'metastatic':1},
                                patient_strat= True,
                            ignore=[]) 
        
    elif task == 'HANCOCK_Surgery_Recurrence':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Recurrence_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Surgery_Recurrence_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Recurrence_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
    elif task == 'HANCOCK_Surgery_Recurrence_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HANCOCK_Surgery_Recurrence_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'no':0, 'yes':1},
                                patient_strat= True,
                                ignore=[]) 
        

    elif task == 'NADT_Prostate_Gleason_withHE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/NADT_Prostate_Gleason_withHE_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'3+3=6':0, '3+4=7':1, '4+3=7':2, '4+4=8':3, '5+3=8':4, '3+5=8':5, '4+5=9':6, '5+4=9':7,'5+5=10':8},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'NADT_Prostate_Gleason_withoutHE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/NADT_Prostate_Gleason_withoutHE_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'3+3=6':0, '3+4=7':1, '4+3=7':2, '4+4=8':3, '5+3=8':4, '3+5=8':5, '4+5=9':6, '5+4=9':7,'5+5=10':8},
                                patient_strat= True,
                                ignore=[]) 

    elif task == 'cervical_CIN_grading':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/cervical_CIN_grading_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'1':0, '2':1, '3':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'cervical_CIN_grading_HE':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/cervical_CIN_grading_subtyping_HE.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'1':0, '2':1, '3':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'cervical_CIN_grading_IHC':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/cervical_CIN_grading_subtyping_IHC.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'1':0, '2':1, '3':2},
                                patient_strat= True,
                                ignore=[])

    elif task == 'MSKMINDProjectM':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/MSKMINDProjectM_subtyping.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'0':0, '1':1},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HPA10M_staining_intensity':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HPA10M_staining_intensity.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'negative':0, 'weak':1, 'moderate':2, 'strong':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HPA10M_staining_location':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HPA10M_staining_location.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'none':0, 'nuclear':1, 'cytoplasmic/membranous':2, 'cytoplasmic/membranous,nuclear':3},
                                patient_strat= True,
                                ignore=[])

    elif task == 'HPA10M_staining_quantity':
        dataset = Generic_MIL_Dataset(csv_path = 'dataset_csv_lanfz/HPA10M_staining_quantity.csv',
                                data_dir= None,
                                shuffle = False, 
                                seed = seed, 
                                print_info = True,
                                label_dict = {'none':0, '<25%':1, '25%-75%':2, '>75%':3},
                                patient_strat= True,
                                ignore=[])
    else:
        raise NotImplementedError
    return dataset
        