import os
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support

from src.dataset import load_tea_dataset, create_dataloaders
from src.model import build_model

def train_and_evaluate():
    dataset_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(dataset_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 1. Load Dataset
    print("Loading dataset and creating train/val/test splits...")
    ds_info = load_tea_dataset(dataset_dir=dataset_dir, test_size=0.15, val_size=0.15, random_seed=42)
    
    num_classes = len(ds_info['raw_classes'])
    print(f"Classes ({num_classes}): {ds_info['raw_classes']}")
    print(f"Train samples: {len(ds_info['train'][0])}, Val samples: {len(ds_info['val'][0])}, Test samples: {len(ds_info['test'][0])}")
    
    train_loader, val_loader, test_loader = create_dataloaders(ds_info, batch_size=16, img_size=224, num_workers=0)
    
    # 2. Build Model
    backbone_name = 'resnet18'
    print(f"Building transfer learning model with backbone: {backbone_name}...")
    model = build_model(num_classes=num_classes, backbone=backbone_name, pretrained=True)
    model.to(device)
    
    # 3. Loss & Optimizer
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = optim.AdamW(model.parameters(), lr=5e-4, weight_decay=1e-4)
    epochs = 12
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)
    
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': []
    }
    
    best_val_acc = 0.0
    best_model_path = os.path.join(models_dir, "tea_leaf_model.pth")
    
    print("\nStarting training loop...")
    start_time = time.time()
    
    for epoch in range(epochs):
        # --- Training ---
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
            
        scheduler.step()
        epoch_train_loss = running_loss / total
        epoch_train_acc = correct / total
        
        # --- Validation ---
        model.eval()
        val_running_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_running_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)
                
        epoch_val_loss = val_running_loss / val_total
        epoch_val_acc = val_correct / val_total
        
        history['train_loss'].append(epoch_train_loss)
        history['train_acc'].append(epoch_train_acc)
        history['val_loss'].append(epoch_val_loss)
        history['val_acc'].append(epoch_val_acc)
        
        print(f"Epoch {epoch+1:02d}/{epochs:02d} | "
              f"Train Loss: {epoch_train_loss:.4f} - Train Acc: {epoch_train_acc*100:.2f}% | "
              f"Val Loss: {epoch_val_loss:.4f} - Val Acc: {epoch_val_acc*100:.2f}%")
        
        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save(model.state_dict(), best_model_path)
            
    total_duration = time.time() - start_time
    print(f"\nTraining completed in {total_duration/60:.2f} minutes. Best Val Acc: {best_val_acc*100:.2f}%")
    
    # Load best model for evaluation on Test set
    model.load_state_dict(torch.load(best_model_path, map_location=device))
    model.eval()
    
    test_preds = []
    test_targets = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            test_preds.extend(preds.cpu().numpy())
            test_targets.extend(labels.numpy())
            
    test_acc = accuracy_score(test_targets, test_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(test_targets, test_preds, average='weighted')
    
    print("\n--- Test Set Performance ---")
    print(f"Accuracy:  {test_acc*100:.2f}%")
    print(f"Precision: {precision*100:.2f}%")
    print(f"Recall:    {recall*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    
    # Detailed per-class report
    display_names = [ds_info['idx_to_display_name'][i] for i in range(num_classes)]
    cls_report = classification_report(test_targets, test_preds, target_names=display_names, output_dict=True)
    print("\nClassification Report:")
    print(classification_report(test_targets, test_preds, target_names=display_names))
    
    # 4. Save Confusion Matrix Plot
    cm = confusion_matrix(test_targets, test_preds)
    plt.figure(figsize=(9, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=display_names, yticklabels=display_names)
    plt.title('Tea Leaf Disease Detection - Confusion Matrix', fontsize=14, pad=12)
    plt.xlabel('Predicted Label', fontsize=11)
    plt.ylabel('True Label', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    cm_path = os.path.join(models_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    
    # 5. Save Training History Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(range(1, epochs+1), history['train_loss'], 'o-', label='Train Loss', color='#e74c3c')
    ax1.plot(range(1, epochs+1), history['val_loss'], 'o-', label='Val Loss', color='#3498db')
    ax1.set_title('Training & Validation Loss', fontsize=12)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    
    ax2.plot(range(1, epochs+1), [a*100 for a in history['train_acc']], 'o-', label='Train Accuracy', color='#2ecc71')
    ax2.plot(range(1, epochs+1), [a*100 for a in history['val_acc']], 'o-', label='Val Accuracy', color='#9b59b6')
    ax2.set_title('Training & Validation Accuracy (%)', fontsize=12)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    
    plt.tight_layout()
    history_path = os.path.join(models_dir, "training_history.png")
    plt.savefig(history_path, dpi=300)
    plt.close()
    
    # 6. Save Metadata JSON
    metadata = {
        'model_backbone': backbone_name,
        'num_classes': num_classes,
        'raw_classes': ds_info['raw_classes'],
        'class_to_idx': ds_info['class_to_idx'],
        'idx_to_class': {str(k): v for k, v in ds_info['idx_to_class'].items()},
        'idx_to_display_name': {str(k): v for k, v in ds_info['idx_to_display_name'].items()},
        'test_metrics': {
            'accuracy': round(float(test_acc), 4),
            'precision': round(float(precision), 4),
            'recall': round(float(recall), 4),
            'f1_score': round(float(f1), 4)
        },
        'per_class_metrics': cls_report,
        'training_epochs': epochs,
        'best_val_acc': round(float(best_val_acc), 4),
        'training_history': history,
        'dataset_counts': {ds_info['idx_to_display_name'][i]: int(np.sum(np.array(ds_info['train'][1] + ds_info['val'][1] + ds_info['test'][1]) == i)) for i in range(num_classes)}
    }
    
    meta_path = os.path.join(models_dir, "model_metadata.json")
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\nModel metadata saved to {meta_path}")
    print("Training pipeline complete!")

if __name__ == '__main__':
    train_and_evaluate()

