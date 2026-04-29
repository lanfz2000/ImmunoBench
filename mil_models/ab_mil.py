import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
sys.path.append('/cpfs04/user/yanfang/workspace/IHC_Benchmarks/code/Master')
from .mil import BaseMILModel

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


class AB_MIL(BaseMILModel):
    def __init__(self, L=512, D=128, in_dim=1024, n_classes=1, dropout=True, act=nn.ReLU(), task_type='subtyping'):
        super(AB_MIL, self).__init__(task=task_type)
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

    def forward(self, x, **kwargs):
        if len(x.shape) == 3 and x.shape[0] > 1:
            raise RuntimeError('Batch size must be 1, current batch size is:{}'.format(x.shape[0]))
        if len(x.shape) == 3 and x.shape[0] == 1:
            x = x[0]
            
        feature = self.feature(x)
        # feature = group_shuffle(feature)
        feature = feature.squeeze(0)
        A = self.attention(feature)
        A_ori = A.clone()
        A = torch.transpose(A, -1, -2)  # KxN
        A = F.softmax(A, dim=-1)  # softmax over N
        M = torch.mm(A, feature)  # 1,KxL
        logits = self.classifier(M)
        
        wsi_logits, wsi_prob, wsi_label = self.task_adapter(logits)

        outputs = {
            'wsi_logits': wsi_logits,
            'wsi_prob': wsi_prob,
            'wsi_label': wsi_label,
        }
        return outputs
    
    # def relocate(self):
    #     device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #     self.head = self.head.to(device)


if __name__ == '__main__':
    mean_model = AB_MIL(n_classes=2)
    x = torch.randn(100, 1024)
    y = mean_model(x)
    print(y)