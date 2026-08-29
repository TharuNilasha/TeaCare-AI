import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split

CLASS_NAME_MAP = {
    'Anthracnose': 'Anthracnose',
    'algal leaf': 'Algal Leaf Spot',
    'bird eye spot': 'Bird\'s Eye Spot',
    'brown blight': 'Brown Blight',
    'gray light': 'Gray Light',
    'healthy': 'Healthy Tea Leaf',
    'red leaf spot': 'Red Leaf Spot',
    'white spot': 'White Spot'
}

ALLOWED_CLASSES = set(CLASS_NAME_MAP.keys())

# Standard normalization stats
NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

def get_transforms(img_size=224):
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(degrees=20),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=NORM_MEAN, std=NORM_STD)
    ])
    
    return train_transform, val_transform

class TeaLeafDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        label = self.labels[idx]
        try:
            image = Image.open(path).convert('RGB')
        except Exception:
            image = Image.new('RGB', (224, 224), (0, 0, 0))
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

def load_tea_dataset(dataset_dir, test_size=0.15, val_size=0.15, random_seed=42):
    raw_classes = sorted([
        d for d in os.listdir(dataset_dir)
        if d in ALLOWED_CLASSES and os.path.isdir(os.path.join(dataset_dir, d))
    ])
    
    class_to_idx = {cls: idx for idx, cls in enumerate(raw_classes)}
    idx_to_class = {idx: cls for idx, cls in enumerate(raw_classes)}
    idx_to_display_name = {idx: CLASS_NAME_MAP.get(cls, cls) for idx, cls in enumerate(raw_classes)}
    
    all_paths = []
    all_labels = []
    
    for cls in raw_classes:
        cls_dir = os.path.join(dataset_dir, cls)
        for fname in os.listdir(cls_dir):
            fpath = os.path.join(cls_dir, fname)
            if os.path.isfile(fpath) and fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                all_paths.append(fpath)
                all_labels.append(class_to_idx[cls])
                
    train_paths, test_paths, train_labels, test_labels = train_test_split(
        all_paths, all_labels, test_size=(test_size + val_size), stratify=all_labels, random_state=random_seed
    )
    
    relative_val_size = val_size / (test_size + val_size)
    val_paths, test_paths, val_labels, test_labels = train_test_split(
        test_paths, test_labels, test_size=(1.0 - relative_val_size), stratify=test_labels, random_state=random_seed
    )
    
    return {
        'train': (train_paths, train_labels),
        'val': (val_paths, val_labels),
        'test': (test_paths, test_labels),
        'class_to_idx': class_to_idx,
        'idx_to_class': idx_to_class,
        'idx_to_display_name': idx_to_display_name,
        'raw_classes': raw_classes
    }

def create_dataloaders(dataset_info, batch_size=16, img_size=224, num_workers=0):
    train_transform, val_transform = get_transforms(img_size)
    
    train_dataset = TeaLeafDataset(dataset_info['train'][0], dataset_info['train'][1], transform=train_transform)
    val_dataset = TeaLeafDataset(dataset_info['val'][0], dataset_info['val'][1], transform=val_transform)
    test_dataset = TeaLeafDataset(dataset_info['test'][0], dataset_info['test'][1], transform=val_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, val_loader, test_loader

