# https://github.com/AMLab-Amsterdam/AttentionDeepMIL/blob/master/model.py
# https://arxiv.org/pdf/1802.04712.pdf

import torch
import torch.nn as nn
import torch.nn.functional as F
from .mil import BaseMILModel

class WSI_MIL(BaseMILModel):
    def __init__(self, in_dim, n_classes, task_type='subtyping'):
        super(WSI_MIL, self).__init__(task=task_type)

        self.classifier = nn.Sequential(nn.Linear(in_dim, 256), 
                                        nn.GELU(), nn.Dropout(0.25), nn.Linear(256, n_classes))

    def forward(self, x, **kwargs):
        # x: [D] not [1,D]
        # print(x.shape)
        x = x.float()
        x = torch.mean(x, dim=0, keepdim=True)
        # x = x.view(1, -1)
        logits = self.classifier(x)
        
        wsi_logits, wsi_prob, wsi_label = self.task_adapter(logits)

        outputs = {
                'wsi_logits': wsi_logits,
                'wsi_prob': wsi_prob,
                'wsi_label': wsi_label
            }
            
        return outputs
    
    def relocate(self):
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classifier = self.classifier.to(device)