import os
import pandas as pd
import numpy as np


def print_metrics(root_dir):
    # 定义模型及其对应的子目录
    model_dirs = {
        "att_mil": [
            "uni", "virchow2", "virchow", "h_optimus_0", "phikon",
            "GPFM", "ctranspath", "gigapath", "chief", "conch_v1_5", "conch", 
        ],
        "wsi_mil": [
            "gigapath_wsi", "chief_wsi", "titan_wsi", "madeleine_wsi"
        ]
    }

    # 存储所有模型结果
    all_results = {}

    # 遍历每个子目录和对应的模型
    for sub_dir, models in model_dirs.items():
        full_dir_path = os.path.join(root_dir, sub_dir)
        
        # 检查子目录是否存在
        if not os.path.exists(full_dir_path):
            print(f"警告: 目录 {full_dir_path} 不存在")
            continue
        
        # 遍历该子目录下的所有文件夹
        for model_folder in os.listdir(full_dir_path):
            # 在文件夹名中查找匹配的模型名称
            matched_model = None
            for model in models:
                if model in model_folder:  # 子字符串匹配
                    matched_model = model
                    break
            
            if matched_model:
                csv_path = os.path.join(full_dir_path, model_folder, 'summary.csv')
                if os.path.exists(csv_path):
                    # 读取CSV文件
                    df = pd.read_csv(csv_path)
                    
                    # 确保有5个folds
                    if len(df) == 5:
                        # 计算各项指标的均值和标准差
                        all_results[matched_model] = {
                            'test_auc': (df['test_auc'].mean(), df['test_auc'].std()),
                            'test_acc': (df['test_acc'].mean(), df['test_acc'].std()),
                            'test_f1': (df['test_f1'].mean(), df['test_f1'].std())
                        }
                    else:
                        print(f"警告: {model_folder} 只有 {len(df)} folds，预期5个")
                else:
                    print(f"警告: {model_folder} 中没有找到summary.csv文件")

    # 按照指定顺序打印结果
    print("模型结果（按指定顺序输出）:")
    for sub_dir, models in model_dirs.items():
        print(f"\n=== {sub_dir} ===")
        for model in models:
            if model in all_results:
                metrics = all_results[model]
                print(f"{model} | "
                    f"test_auc: {metrics['test_auc'][0]:.4f}±{metrics['test_auc'][1]:.4f} | "
                    f"test_acc: {metrics['test_acc'][0]:.4f}±{metrics['test_acc'][1]:.4f} | "
                    f"test_f1: {metrics['test_f1'][0]:.4f}±{metrics['test_f1'][1]:.4f}")
            else:
                print(f"警告: 未找到模型 {model} 的结果")


import os
import pandas as pd
import csv

def print_metrics_and_save_csv(root_dir, output_csv='results_summary.csv'):
    model_dirs = {
        "att_mil": [
            "uni", "virchow2", "virchow", "h_optimus_0", "phikon",
            "GPFM", "ctranspath", "gigapath", "chief", "conch_v1_5", "conch", 
        ],
        "wsi_mil": [
            "gigapath_wsi", "chief_wsi", "titan_wsi", "madeleine_wsi"
        ]
    }

    all_results = {}

    for sub_dir, models in model_dirs.items():
        full_dir_path = os.path.join(root_dir, sub_dir)
        if not os.path.exists(full_dir_path):
            print(f"警告: 目录 {full_dir_path} 不存在")
            continue

        for model_folder in os.listdir(full_dir_path):
            matched_model = None
            for model in models:
                if model in model_folder:
                    matched_model = model
                    break

            if matched_model:
                csv_path = os.path.join(full_dir_path, model_folder, 'summary.csv')
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    if len(df) == 5:
                        all_results[matched_model] = {
                            'test_auc': (df['test_auc'].mean(), df['test_auc'].std()),
                            'test_acc': (df['test_acc'].mean(), df['test_acc'].std()),
                            'test_f1': (df['test_f1'].mean(), df['test_f1'].std())
                        }
                    else:
                        print(f"警告: {model_folder} 只有 {len(df)} folds，预期5个")
                else:
                    print(f"警告: {model_folder} 中没有找到 summary.csv 文件")

    # 打印结果
    print("模型结果（按指定顺序输出）:")
    for sub_dir, models in model_dirs.items():
        print(f"\n=== {sub_dir} ===")
        for model in models:
            if model in all_results:
                metrics = all_results[model]
                print(f"{model} | "
                      f"test_auc: {metrics['test_auc'][0]:.4f}±{metrics['test_auc'][1]:.4f} | "
                      f"test_acc: {metrics['test_acc'][0]:.4f}±{metrics['test_acc'][1]:.4f} | "
                      f"test_f1: {metrics['test_f1'][0]:.4f}±{metrics['test_f1'][1]:.4f}")
            else:
                print(f"警告: 未找到模型 {model} 的结果")

    # 写入 CSV 文件（两行格式）
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 第一行：表头（模型名）
        header = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    header.append(model)
        writer.writerow(header)

        # 第二行：每个模型的指标字符串
        values = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    m = all_results[model]
                    value_str = f"test_auc:{m['test_auc'][0]:.4f}±{m['test_auc'][1]:.4f}" + "  "\
                                f"test_acc:{m['test_acc'][0]:.4f}±{m['test_acc'][1]:.4f}" + "  "\
                                f"test_f1:{m['test_f1'][0]:.4f}±{m['test_f1'][1]:.4f}"
                    values.append(value_str)
        writer.writerow(values)


def print_metrics_and_save_csv_patch(root_dir, output_csv='results_summary.csv'):
    model_dirs = {
        "LP": [
            "uni", "virchow2", "virchow", "h_optimus_0", "phikon",
            "GPFM", "ctranspath", "gigapath", "chief", "conch_v1_5", "conch", 
        ]
    }

    all_results = {}

    for sub_dir, models in model_dirs.items():
        full_dir_path = os.path.join(root_dir, sub_dir)
        if not os.path.exists(full_dir_path):
            print(f"警告: 目录 {full_dir_path} 不存在")
            continue

        for model_folder in os.listdir(full_dir_path):
            matched_model = None
            for model in models:
                if model in model_folder:
                    matched_model = model
                    break

            if matched_model:
                csv_path = os.path.join(full_dir_path, model_folder, 'summary.csv')
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    if len(df) == 5:
                        all_results[matched_model] = {
                            'test_auc': (df['test_auc'].mean(), df['test_auc'].std()),
                            'test_acc': (df['test_acc'].mean(), df['test_acc'].std()),
                            'test_f1': (df['test_f1'].mean(), df['test_f1'].std())
                        }
                    else:
                        print(f"警告: {model_folder} 只有 {len(df)} folds，预期5个")
                else:
                    print(f"警告: {model_folder} 中没有找到 summary.csv 文件")

    # 打印结果
    print("模型结果（按指定顺序输出）:")
    for sub_dir, models in model_dirs.items():
        print(f"\n=== {sub_dir} ===")
        for model in models:
            if model in all_results:
                metrics = all_results[model]
                print(f"{model} | "
                      f"test_auc: {metrics['test_auc'][0]:.4f}±{metrics['test_auc'][1]:.4f} | "
                      f"test_acc: {metrics['test_acc'][0]:.4f}±{metrics['test_acc'][1]:.4f} | "
                      f"test_f1: {metrics['test_f1'][0]:.4f}±{metrics['test_f1'][1]:.4f}")
            else:
                print(f"警告: 未找到模型 {model} 的结果")

    # 写入 CSV 文件（两行格式）
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 第一行：表头（模型名）
        header = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    header.append(model)
        writer.writerow(header)

        # 第二行：每个模型的指标字符串
        values = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    m = all_results[model]
                    value_str = f"test_auc:{m['test_auc'][0]:.4f}±{m['test_auc'][1]:.4f}" + "  "\
                                f"test_acc:{m['test_acc'][0]:.4f}±{m['test_acc'][1]:.4f}" + "  "\
                                f"test_f1:{m['test_f1'][0]:.4f}±{m['test_f1'][1]:.4f}"
                    values.append(value_str)
        writer.writerow(values)

import os
import pandas as pd
import numpy as np


def print_metrics(root_dir):
    # 定义模型及其对应的子目录
    model_dirs = {
        "att_mil": [
            "uni", "virchow2", "virchow", "h_optimus_0", "phikon",
            "GPFM", "ctranspath", "gigapath", "chief", "conch_v1_5", "conch", 
        ],
        "wsi_mil": [
            "gigapath_wsi", "chief_wsi", "titan_wsi", "madeleine_wsi"
        ]
    }

    # 存储所有模型结果
    all_results = {}

    # 遍历每个子目录和对应的模型
    for sub_dir, models in model_dirs.items():
        full_dir_path = os.path.join(root_dir, sub_dir)
        
        # 检查子目录是否存在
        if not os.path.exists(full_dir_path):
            print(f"警告: 目录 {full_dir_path} 不存在")
            continue
        
        # 遍历该子目录下的所有文件夹
        for model_folder in os.listdir(full_dir_path):
            # 在文件夹名中查找匹配的模型名称
            matched_model = None
            for model in models:
                if model in model_folder:  # 子字符串匹配
                    matched_model = model
                    break
            
            if matched_model:
                csv_path = os.path.join(full_dir_path, model_folder, 'summary.csv')
                if os.path.exists(csv_path):
                    # 读取CSV文件
                    df = pd.read_csv(csv_path)
                    
                    # 确保有5个folds
                    if len(df) == 5:
                        # 计算各项指标的均值和标准差
                        all_results[matched_model] = {
                            'test_auc': (df['test_auc'].mean(), df['test_auc'].std()),
                            'test_acc': (df['test_acc'].mean(), df['test_acc'].std()),
                            'test_f1': (df['test_f1'].mean(), df['test_f1'].std())
                        }
                    else:
                        print(f"警告: {model_folder} 只有 {len(df)} folds，预期5个")
                else:
                    print(f"警告: {model_folder} 中没有找到summary.csv文件")

    # 按照指定顺序打印结果
    print("模型结果（按指定顺序输出）:")
    for sub_dir, models in model_dirs.items():
        print(f"\n=== {sub_dir} ===")
        for model in models:
            if model in all_results:
                metrics = all_results[model]
                print(f"{model} | "
                    f"test_auc: {metrics['test_auc'][0]:.4f}±{metrics['test_auc'][1]:.4f} | "
                    f"test_acc: {metrics['test_acc'][0]:.4f}±{metrics['test_acc'][1]:.4f} | "
                    f"test_f1: {metrics['test_f1'][0]:.4f}±{metrics['test_f1'][1]:.4f}")
            else:
                print(f"警告: 未找到模型 {model} 的结果")


import os
import pandas as pd
import csv

def print_metrics_and_save_csv_survival(root_dir, output_csv='results_summary.csv'):
    model_dirs = {
        "att_mil": [
            "uni", "virchow2", "virchow", "h_optimus_0", "phikon",
            "GPFM", "ctranspath", "gigapath", "chief", "conch_v1_5", "conch", 
        ],
        "wsi_mil": [
            "gigapath_wsi", "chief_wsi", "titan_wsi", "madeleine_wsi"
        ]
    }

    all_results = {}

    for sub_dir, models in model_dirs.items():
        full_dir_path = os.path.join(root_dir, sub_dir)
        if not os.path.exists(full_dir_path):
            print(f"警告: 目录 {full_dir_path} 不存在")
            continue

        for model_folder in os.listdir(full_dir_path):
            matched_model = None
            for model in models:
                if model in model_folder:
                    matched_model = model
                    break

            if matched_model:
                csv_path = os.path.join(full_dir_path, model_folder, 'summary.csv')
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    if len(df) == 5:
                        all_results[matched_model] = {
                            'test_cindex': (df['test_cindex'].mean(), df['test_cindex'].std())
                        }
                    else:
                        print(f"警告: {model_folder} 只有 {len(df)} folds，预期5个")
                else:
                    print(f"警告: {model_folder} 中没有找到 summary.csv 文件")

    # 打印结果
    print("模型结果（按指定顺序输出）:")
    for sub_dir, models in model_dirs.items():
        print(f"\n=== {sub_dir} ===")
        for model in models:
            if model in all_results:
                metrics = all_results[model]
                print(f"{model} | "
                      f"test_cindex: {metrics['test_cindex'][0]:.4f}±{metrics['test_cindex'][1]:.4f}")
            else:
                print(f"警告: 未找到模型 {model} 的结果")

    # 写入 CSV 文件（两行格式）
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 第一行：表头（模型名）
        header = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    header.append(model)
        writer.writerow(header)

        # 第二行：每个模型的指标字符串
        values = []
        for sub_dir, models in model_dirs.items():
            for model in models:
                if model in all_results:
                    m = all_results[model]
                    value_str = f"test_ci:{m['test_cindex'][0]:.4f}±{m['test_cindex'][1]:.4f}"
                    values.append(value_str)
        writer.writerow(values)
