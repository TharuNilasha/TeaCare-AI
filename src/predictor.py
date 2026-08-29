import os
import json
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from src.model import build_model
from src.validator import validate_image_file, check_leaf_domain_suitability
from src.advisory import get_disease_advisory
from src.dataset import NORM_MEAN, NORM_STD

class TeaLeafPredictor:
    def __init__(self, models_dir=None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
            
        self.models_dir = models_dir
        self.model_path = os.path.join(models_dir, "tea_leaf_model.pth")
        self.metadata_path = os.path.join(models_dir, "model_metadata.json")
        
        if not os.path.exists(self.metadata_path) or not os.path.exists(self.model_path):
            raise FileNotFoundError("Model or metadata files not found. Please train the model first by running train_model.py.")
            
        with open(self.metadata_path, 'r') as f:
            self.metadata = json.load(f)
            
        self.raw_classes = self.metadata['raw_classes']
        self.idx_to_display_name = {int(k): v for k, v in self.metadata['idx_to_display_name'].items()}
        self.num_classes = len(self.raw_classes)
        backbone_name = self.metadata.get('model_backbone', 'resnet18')
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = build_model(num_classes=self.num_classes, backbone=backbone_name, pretrained=True)
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
        ])

    def predict(self, file_or_img, min_confidence_threshold=0.40):
        """
        Runs validation and model prediction on image input.
        """
        # 1. Image File Validation
        is_valid, status_msg, img_pil = validate_image_file(file_or_img)
        if not is_valid:
            return {
                'success': False,
                'error': status_msg,
                'is_leaf_like': False,
                'validation_status': 'FAILED'
            }
            
        # 2. Leaf Domain Suitability Check
        is_leaf_like, color_metrics = check_leaf_domain_suitability(img_pil)
        
        # 3. Model Inference
        tensor_img = self.transform(img_pil).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(tensor_img)
            probabilities = F.softmax(outputs, dim=1)[0].cpu().numpy()
            
        top_idx = int(probabilities.argmax())
        top_confidence = float(probabilities[top_idx])
        raw_class_name = self.raw_classes[top_idx]
        display_name = self.idx_to_display_name[top_idx]
        
        # All class probabilities
        class_probs = []
        for idx in range(self.num_classes):
            class_probs.append({
                'raw_name': self.raw_classes[idx],
                'display_name': self.idx_to_display_name[idx],
                'confidence': float(probabilities[idx]),
                'percentage': round(float(probabilities[idx]) * 100, 2)
            })
            
        class_probs = sorted(class_probs, key=lambda x: x['confidence'], reverse=True)
        
        # Advisory Information
        advisory = get_disease_advisory(raw_class_name)
        
        # Low confidence or out-of-domain warning
        domain_warning = None
        if top_confidence < min_confidence_threshold:
            domain_warning = f"Low confidence ({top_confidence*100:.1f}%). The image may not be a tea leaf or has severe lighting/blur distortion."
        elif not is_leaf_like:
            domain_warning = "Color distribution warning: Image has low foliage pigment ratio. Ensure the uploaded image is a tea leaf."
            
        return {
            'success': True,
            'image_pil': img_pil,
            'predicted_class_raw': raw_class_name,
            'predicted_class_display': display_name,
            'confidence': top_confidence,
            'confidence_percentage': round(top_confidence * 100, 2),
            'class_probabilities': class_probs,
            'advisory': advisory,
            'is_leaf_like': is_leaf_like,
            'color_metrics': color_metrics,
            'domain_warning': domain_warning,
            'validation_status': 'PASSED'
        }

_predictor_instance = None

def get_predictor():
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = TeaLeafPredictor()
    return _predictor_instance

