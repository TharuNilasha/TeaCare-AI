import os
import cv2
import numpy as np
from PIL import Image

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
MAX_FILE_SIZE_MB = 20
MIN_RESOLUTION = (64, 64)

def validate_image_file(file_or_path):
    """
    Validates file format, size, and PIL image corruption.
    Accepts file path string, bytes, or BytesIO object.
    Returns: (is_valid: bool, status_message: str, img_pil: Image or None)
    """
    try:
        if isinstance(file_or_path, str):
            if not os.path.exists(file_or_path):
                return False, "File does not exist.", None
            
            ext = os.path.splitext(file_or_path)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                return False, f"Unsupported file format '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}.", None
            
            file_size_mb = os.path.getsize(file_or_path) / (1024 * 1024)
            if file_size_mb > MAX_FILE_SIZE_MB:
                return False, f"File size ({file_size_mb:.1f}MB) exceeds limit of {MAX_FILE_SIZE_MB}MB.", None
            
            img = Image.open(file_or_path)
        else:
            img = Image.open(file_or_path)
            
        img.verify()
        
        if isinstance(file_or_path, str):
            img = Image.open(file_or_path).convert("RGB")
        else:
            file_or_path.seek(0)
            img = Image.open(file_or_path).convert("RGB")
            
        width, height = img.size
        if width < MIN_RESOLUTION[0] or height < MIN_RESOLUTION[1]:
            return False, f"Image resolution ({width}x{height}) is too small. Minimum required: {MIN_RESOLUTION[0]}x{MIN_RESOLUTION[1]} px.", None
            
        return True, "Valid image file.", img
        
    except Exception as e:
        return False, f"Corrupted or invalid image file: {str(e)}", None


def check_leaf_domain_suitability(img_pil):
    """
    Performs heuristic color analysis to check if the image contains typical foliage/plant tones.
    Returns: (is_leaf_like: bool, metrics: dict)
    """
    img_np = np.array(img_pil)
    if img_np.ndim != 3 or img_np.shape[2] != 3:
        return True, {"plant_ratio": 1.0}
        
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    
    # Green range (Hue ~25 to 85)
    lower_green = np.array([20, 25, 25])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Brown / Yellow disease spots (Hue ~10 to 25 or ~85 to 110)
    lower_brown = np.array([5, 25, 25])
    upper_brown = np.array([25, 255, 255])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    
    # Dark lesions / decay
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([180, 255, 60])
    dark_mask = cv2.inRange(hsv, lower_dark, upper_dark)
    
    combined_mask = cv2.bitwise_or(green_mask, brown_mask)
    combined_mask = cv2.bitwise_or(combined_mask, dark_mask)
    
    plant_pixel_ratio = np.count_nonzero(combined_mask) / (img_np.shape[0] * img_np.shape[1])
    
    is_leaf_like = plant_pixel_ratio >= 0.05  # At least 5% leaf/lesion tones
    
    return is_leaf_like, {
        "plant_pixel_ratio": round(float(plant_pixel_ratio), 3),
        "green_ratio": round(float(np.count_nonzero(green_mask) / (img_np.shape[0] * img_np.shape[1])), 3),
        "brown_ratio": round(float(np.count_nonzero(brown_mask) / (img_np.shape[0] * img_np.shape[1])), 3)
    }

