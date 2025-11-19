import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os
import zipfile
from main import process_image

st.set_page_config(
    page_title="Smart E-commerce Image Alignment",
    page_icon="🖼️",
    layout="wide"
)

st.title("🖼️ Smart E-commerce Image Alignment")
st.markdown("""
Upload your product images (white background) to automatically align and crop them according to the standard specifications.
- **Output Size**: 1000x1000 px
- **Bottom Alignment**: Y=900
- **Boundaries**: X=70-930, Y>=80
""")

uploaded_files = st.file_uploader("Choose images...", type=['jpg', 'jpeg', 'webp'], accept_multiple_files=True)

if uploaded_files:
    st.divider()
    st.subheader("Processing Results")
    
    # Create a progress bar
    progress_bar = st.progress(0)
    
    processed_images = []
    
    # Create columns for grid layout
    cols = st.columns(3)
    
    for idx, uploaded_file in enumerate(uploaded_files):
        # Read file as bytes
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if img is not None:
            # Process image
            processed_img = process_image(img)
            
            if processed_img is not None:
                # Convert BGR to RGB for display
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                processed_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                
                # Add to list for zip download
                # Encode back to JPEG for download
                quality = 95
                _, encoded_img = cv2.imencode('.jpg', processed_img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                
                # Output size limit check (400KB)
                target_size_bytes = 400 * 1024
                while len(encoded_img) > target_size_bytes and quality > 10:
                    quality -= 5
                    _, encoded_img = cv2.imencode('.jpg', processed_img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                
                # Ensure filename ends with .jpg
                original_name = uploaded_file.name
                name_no_ext = os.path.splitext(original_name)[0]
                new_filename = f"{name_no_ext}.jpg"
                
                processed_images.append((new_filename, encoded_img.tobytes()))
                
                # Display in grid
                with cols[idx % 3]:
                    st.markdown(f"**{uploaded_file.name}**")
                    comp_col1, comp_col2 = st.columns(2)
                    with comp_col1:
                        st.image(img_rgb, caption="Original", use_container_width=True)
                    with comp_col2:
                        st.image(processed_rgb, caption="Processed", use_container_width=True)
                    st.divider()
            else:
                st.error(f"Failed to process {uploaded_file.name}. No object detected or other error.")
        
        # Update progress
        progress_bar.progress((idx + 1) / len(uploaded_files))

    if processed_images:
        st.success(f"Successfully processed {len(processed_images)} images!")
        
        # Create ZIP file for download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, img_data in processed_images:
                zip_file.writestr(f"processed_{filename}", img_data)
        
        st.download_button(
            label="📦 Download All Processed Images (ZIP)",
            data=zip_buffer.getvalue(),
            file_name="processed_images.zip",
            mime="application/zip"
        )
