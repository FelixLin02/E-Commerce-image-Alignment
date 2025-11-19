import cv2
import numpy as np
import os
import glob
from pathlib import Path

# Constants from PRD
CANVAS_SIZE = (1000, 1000) # Width, Height
Y_BOTTOM = 900
X_LEFT = 70
X_RIGHT = 930
Y_TOP = 80

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

def ensure_dirs():
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Created directory: {INPUT_DIR}")
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

def get_bbox(image):
    """
    Detects the bounding box of the product in the image.
    Assumes white background.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to find non-white pixels (product)
    # Invert so object is white, background is black
    # Using 250 as threshold to catch near-white noise if any, but PRD suggests simple threshold
    _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # Find the combined bounding box of all contours
    x_min, y_min = float('inf'), float('inf')
    x_max, y_max = float('-inf'), float('-inf')
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)
        
    return (x_min, y_min, x_max, y_max)

def process_image(img):
    """
    Core logic to process a single image array (OpenCV format).
    Returns the transformed image or None if processing fails.
    """
    h, w = img.shape[:2]
    
    # FR1.2: Size requirement check (warning only)
    if h <= 1000 or w <= 1000:
        print(f"Warning: Image dimensions ({w}x{h}) are not > 1000px as per FR1.2")

    # FR2: Detect Bounding Box
    bbox = get_bbox(img)
    if bbox is None:
        print(f"Error: No object detected")
        return None
        
    p_x_min, p_y_min, p_x_max, p_y_max = bbox
    p_width = p_x_max - p_x_min
    p_height = p_y_max - p_y_min
    
    if p_width == 0 or p_height == 0:
        print(f"Error: Detected object has 0 width or height")
        return None

    # FR3: Calculate Scaling and Translation
    
    # Step A: Calculate Scaling Factors
    s_h = 900.0 / p_height
    s_w = 860.0 / p_width
    s_t = 820.0 / p_height
    
    # Step B: Final Scaling Factor
    s = min(s_h, s_w, s_t)
    
    # Step C: Calculate Translation
    t_y = 900.0 - (p_y_max * s)
    t_x = 500.0 - (p_width * s / 2.0) - (p_x_min * s)
    
    # FR4: Image Output Processing
    # FR4.1 Geometric Transformation
    M = np.float32([[s, 0, t_x], [0, s, t_y]])
    
    transformed_img = cv2.warpAffine(
        img, 
        M, 
        CANVAS_SIZE, 
        borderMode=cv2.BORDER_CONSTANT, 
        borderValue=(255, 255, 255)
    )
    
    return transformed_img

def process_single_image(filepath):
    filename = os.path.basename(filepath)
    print(f"Processing: {filename}")
    
    # Check input file size (FR: Limit 500KB)
    file_size_kb = os.path.getsize(filepath) / 1024
    if file_size_kb > 500:
        print(f"Skipping {filename}: File size {file_size_kb:.2f}KB exceeds 500KB limit.")
        return

    # Read image
    img = cv2.imread(filepath)
    if img is None:
        print(f"Error: Could not read {filepath}")
        return

    transformed_img = process_image(img)
    if transformed_img is None:
        print(f"Skipping {filename} due to processing error.")
        return
    
    # FR4.3 Output Format
    # Ensure output is always JPG
    filename_no_ext = os.path.splitext(filename)[0]
    output_filename = f"{filename_no_ext}.jpg"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    # Save with initial quality
    quality = 95
    cv2.imwrite(output_path, transformed_img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    
    # Check output size (FR: Limit 200KB)
    target_size_kb = 200.0
    while os.path.getsize(output_path) > target_size_kb * 1024 and quality > 10:
        quality -= 5
        cv2.imwrite(output_path, transformed_img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        
    print(f"Saved: {output_path} (Size: {os.path.getsize(output_path)/1024:.2f} KB)")

def main():
    ensure_dirs()
    
    # Find all JPG and WebP images in input directory
    extensions = ['*.jpg', '*.JPG', '*.webp', '*.WEBP']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))
    
    files = sorted(list(set(files))) # Remove duplicates
    
    if not files:
        print(f"No JPG or WebP files found in {INPUT_DIR}")
        return
        
    print(f"Found {len(files)} images.")
    
    for filepath in files:
        try:
            process_single_image(filepath)
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    main()
