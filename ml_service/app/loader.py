import os
import torch
import logging
from transformers import PreTrainedTokenizerFast, AutoTokenizer
from .model import MultiTaskGatewayModel
from .config import settings

logger = logging.getLogger(__name__)

def load_tokenizer():
    tokenizer_path = os.path.join(settings.ARTIFACTS_PATH, settings.TOKENIZER_FILENAME)
    config_path = os.path.join(settings.ARTIFACTS_PATH, settings.TOKENIZER_CONFIG_FILENAME)
    
    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"Tokenizer file not found at {tokenizer_path}")
    
    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            tokenizer_config = json.load(f)
        
        tokenizer = PreTrainedTokenizerFast(
            tokenizer_file=tokenizer_path,
            **tokenizer_config
        )
    except Exception as e:
        logger.error(f"Failed to load tokenizer: {e}")
        raise
        
    return tokenizer

def load_model(device: torch.device):
    config_path = os.path.join(settings.ARTIFACTS_PATH, settings.CONFIG_FILENAME)
    weights_path = os.path.join(settings.ARTIFACTS_PATH, settings.WEIGHTS_FILENAME)
    
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Model weights not found at {weights_path}")
        
    model = MultiTaskGatewayModel(config_path)
    
    try:
        state_dict = torch.load(weights_path, map_location=device, weights_only=True)
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()
    except Exception as e:
        logger.error(f"Failed to load model weights: {e}")
        raise
        
    return model

def get_device():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return device
