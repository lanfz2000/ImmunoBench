import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
# sys.path.append('/cpfs04/user/yanfang/workspace/IHC_Benchmarks/code/Master')
# from .mil import BaseMILModel

def initialize_weights(module):
    for m in module.modules():
        if isinstance(m, nn.Conv2d):
            nn.init.xavier_normal_(m.weight)
            if m.bias is not None:
                m.bias.data.zero_()
        elif isinstance(m,nn.Linear):
            nn.init.xavier_normal_(m.weight)
            if m.bias is not None:
                m.bias.data.zero_()
        elif isinstance(m,nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)


# 注意：为了你能直接运行测试，我这里暂时注释掉了继承 BaseMILModel。
# 你自己放到工程里的时候，把 BaseMILModel 的继承加回去即可。
class AB_MIL(nn.Module): 
    def __init__(self, L=512, D=128, in_dim=1024, n_classes=1, dropout=True, act=nn.ReLU(), task_type='subtyping'):
        super(AB_MIL, self).__init__() # 实际工程中这里用 super(AB_MIL, self).__init__(task=task_type)
        self.rrt = None
        self.in_dim = in_dim
        self.num_classes = n_classes
        self.L = L
        self.D = D
        self.K = 1
        self.feature = [nn.Linear(in_dim, self.L)]
        
        self.feature += [act]

        if dropout:
            self.feature += [nn.Dropout(dropout)]
            
        if self.rrt != None:
            self.feature += [self.rrt]

        self.feature = nn.Sequential(*self.feature)

        self.attention = nn.Sequential(
            nn.Linear(self.L, self.D),
            nn.Tanh(),
            nn.Linear(self.D, self.K)
        )
        self.classifier = nn.Sequential(
            nn.Linear(self.L*self.K, self.num_classes),
        )

        self.apply(initialize_weights)

    def forward(self, x, mask=None, **kwargs):
        """
        支持 Batch 运算的 Forward
        x:    [B, max_N, in_dim] 填充后的特征张量
        mask: [B, max_N] 布尔型张量，真实有效 Patch 处为 True，补 0 处为 False
        """
        # 1. 提取特征 (PyTorch 的 Linear 天然支持对 3D 张量的最后一维进行变换)
        # 输入 [B, max_N, in_dim] -> 输出 [B, max_N, L]
        feature = self.feature(x) 
        
        # 2. 计算未归一化的 Attention 分数
        # 输入 [B, max_N, L] -> 输出 [B, max_N, K]
        A = self.attention(feature) 
        
        # 维度转换以备矩阵乘法: [B, K, max_N]
        A = torch.transpose(A, 1, 2) 

        # 3. 🌟 核心魔法：应用 Mask
        if mask is not None:
            # 扩展 mask 维度对齐 A: [B, max_N] -> [B, 1, max_N]
            mask = mask.unsqueeze(1)
            # 把填充位置的 Attention 分数替换为一个极小的负数
            A = A.masked_fill(~mask, -1e9) 

        # 4. Softmax 归一化 (补 0 的地方因为是 -1e9，算完就是完美的 0)
        A = F.softmax(A, dim=-1)  # [B, K, max_N]
        
        # 5. 批量矩阵乘法 (BMM) 进行特征聚合
        # [B, K, max_N] x [B, max_N, L] -> [B, K, L]
        M = torch.bmm(A, feature) 
        
        # 将聚合后的特征展平给分类器: [B, K*L]
        M = M.view(M.size(0), -1) 
        
        # 6. 最终分类
        logits = self.classifier(M) # [B, num_classes]
        
        # 模拟你的 task_adapter (实际工程中放开你原来的代码)
        # wsi_logits, wsi_prob, wsi_label = self.task_adapter(logits)
        wsi_logits = logits
        wsi_prob = torch.sigmoid(logits) if self.num_classes == 1 else F.softmax(logits, dim=-1)
        wsi_label = torch.argmax(wsi_prob, dim=-1)

        outputs = {
            'wsi_logits': wsi_logits,
            'wsi_prob': wsi_prob,
            'wsi_label': wsi_label,
            'A': A # 把注意力权重返回，方便后期画热力图
        }
        return outputs


if __name__ == '__main__':
    # 🌟 测试一下并行的威力
    mean_model = AB_MIL(n_classes=2)
    
    B = 4          # 模拟 Batch Size 为 4
    max_N = 50     # 最大 Patch 数量只有 50
    in_dim = 1024
    
    # 模拟真实场景：4 张图的真实 Patch 数量分别是 50, 30, 10, 45
    valid_lengths = [50, 30, 10, 45]
    
    # 初始化填充张量和 Mask
    x_padded = torch.zeros(B, max_N, in_dim)
    mask = torch.zeros(B, max_N, dtype=torch.bool)
    
    for i, length in enumerate(valid_lengths):
        # 填入真实数据 (用随机数模拟)
        x_padded[i, :length, :] = torch.randn(length, in_dim)
        # 将有效位置标记为 True
        mask[i, :length] = True
        
    # 直接整个 Batch 一起扔进模型！
    outputs = mean_model(x_padded, mask=mask)
    
    print(f"输入 X 形状: {x_padded.shape}")
    print(f"Mask 形状: {mask.shape}")
    print(f"输出 Logits 形状: {outputs['wsi_logits'].shape}")
    
    # 验证一下第一张图 (真实长度 30) 的 Attention，看第 31 个是不是被完美变成 0 了
    print("\n检查第二张图的 Attention 权重 (最后 5 个应该是 0):")
    print(outputs['A'][1, 0, -5:])