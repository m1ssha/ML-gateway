import torch
import torch.nn as nn
from transformers import AutoModel, BertConfig, BertModel
from typing import Tuple

class MultiTaskGatewayModel(nn.Module):
    def __init__(self, config_path: str):
        super().__init__()
        
        # 1. Backbone Encoder
        try:
            self.config = BertConfig.from_json_file(config_path)
            self.backbone = BertModel(self.config)
        except Exception:
            self.backbone = AutoModel.from_pretrained(config_path)
            self.config = self.backbone.config

        hidden_size = self.config.hidden_size # Should be 312
        
        # 3. Stabilization Subgraph (matches 'bottleneck' in weights)
        self.bottleneck = nn.Sequential(
            nn.Linear(hidden_size, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(p=0.1)
        )
        
        # 4. Classifier Head
        self.classifier = nn.Linear(128, 1)
        
        # 5. Regressor Head
        self.regressor = nn.Sequential(
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # 1. Backbone pass
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        
        # 2. Contextual Pooling
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
        sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        pooled_output = sum_embeddings / sum_mask
        
        # 3. Stabilization
        shared_features = self.bottleneck(pooled_output)
        
        # 4. Classifier
        logits = self.classifier(shared_features)
        
        # 5. Regressor
        risk_score = self.regressor(shared_features)
        
        return logits, risk_score
