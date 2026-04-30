import argparse
import csv
import os
import warnings

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from torch.utils.data import DataLoader, TensorDataset

warnings.filterwarnings("ignore")

# 两层 MLP 模型
class MLP(nn.Module):
    def __init__(self, in_dim, num_classes):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(in_dim, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.model(x)

# 模型评估
def evaluate(model, loader, device, num_classes):
    model.eval()
    y_true, y_pred, y_prob = [], [], []
    with torch.no_grad():
        for xb, yb in loader:
            xb = xb.to(device)
            logits = model(xb)
            probs = torch.softmax(logits, dim=1).cpu()
            preds = torch.argmax(probs, dim=1)
            y_true.extend(yb.numpy())
            y_pred.extend(preds.numpy())
            y_prob.extend(probs.numpy())

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_prob = np.array(y_prob)

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')
    try:
        y_true_onehot = np.eye(num_classes)[y_true]
        auc = roc_auc_score(y_true_onehot, y_prob, multi_class='ovr', average='macro')
    except:
        auc = np.nan

    return acc, f1, auc

# 训练 + 验证
def train_and_validate(model, train_loader, val_loader, test_loader, device, fold, num_classes, save_path):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    model.to(device)

    best_val_acc = 0
    best_model_state = None

    for epoch in range(30):
        model.train()
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            logits = model(xb)
            loss = criterion(logits, yb)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        val_acc, _, _ = evaluate(model, val_loader, device, num_classes)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict()
    # 保存最佳模型
    if best_model_state is not None and save_path:
        os.makedirs(save_path, exist_ok=True)
        torch.save(best_model_state, os.path.join(save_path, f's_{fold}_checkpoint.pt'))

    # 测试阶段
    model.load_state_dict(best_model_state)
    test_acc, test_f1, test_auc = evaluate(model, test_loader, device, num_classes)
    print(f"[Fold {fold}] Acc: {test_acc:.4f}, F1: {test_f1:.4f}, AUC: {test_auc:.4f}")
    return test_acc, test_f1, test_auc

# 主函数
def main(args):
    data = torch.load(args.pt_path)
    # print(data.keys())
    features = data['feature']
    labels = data['label']
    label_map = {label: idx for idx, label in enumerate(set(labels))}
    labels = [label_map[label] for label in labels]
    labels = torch.tensor(labels).long()
    _, counts = np.unique(labels.numpy(), return_counts=True)
    print(len(torch.unique(labels)), features.shape, counts)

    in_dim = features.shape[1]
    num_classes = len(torch.unique(labels))
    print('num_classes:', num_classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    all_acc, all_f1, all_auc = [], [], []

    # 写入 CSV 文件
    if not os.path.exists(os.path.dirname(args.out_csv)):
        os.makedirs(os.path.dirname(args.out_csv))  # 创建文件夹

    with open(args.out_csv, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['fold', 'test_auc', 'test_acc', 'test_f1'])

        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        for fold, (trainval_idx, test_idx) in enumerate(skf.split(features, labels)):
            trainval_features = features[trainval_idx]
            trainval_labels = labels[trainval_idx]
            test_features = features[test_idx]
            test_labels = labels[test_idx]

            # 从 trainval 中划分 val
            train_idx, val_idx = train_test_split(
                np.arange(len(trainval_labels)),
                test_size=0.2,
                stratify=trainval_labels,
                random_state=fold
            )

            train_dataset = TensorDataset(trainval_features[train_idx], trainval_labels[train_idx])
            val_dataset = TensorDataset(trainval_features[val_idx], trainval_labels[val_idx])
            test_dataset = TensorDataset(test_features, test_labels)

            train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
            val_loader = DataLoader(val_dataset, batch_size=128)
            test_loader = DataLoader(test_dataset, batch_size=128)

            model = MLP(in_dim, num_classes)
            acc, f1, auc = train_and_validate(model, train_loader, val_loader, test_loader, device, fold, num_classes, args.save_path)

            all_acc.append(acc)
            all_f1.append(f1)
            all_auc.append(auc)
            writer.writerow([fold, f"{auc:.4f}", f"{acc:.4f}", f"{f1:.4f}"])

    print("\n=== Final 5-Fold Results ===")
    print(f"Acc: {np.mean(all_acc):.4f} ± {np.std(all_acc):.4f}")
    print(f"F1 : {np.mean(all_f1):.4f} ± {np.std(all_f1):.4f}")
    print(f"AUC: {np.nanmean(all_auc):.4f} ± {np.nanstd(all_auc):.4f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pt_path', type=str, required=True, help='Path to .pt file containing features and labels')
    parser.add_argument('--out_csv', type=str, default='results.csv', help='Path to output CSV file')
    parser.add_argument('--save_path', type=str, default='', help='Directory to save checkpoints')
    args = parser.parse_args()
    main(args)
