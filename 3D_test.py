import streamlit as st
import numpy as np
import pydicom
from PIL import Image
from skimage.exposure import rescale_intensity

def load_dicom(file):
    """Loads a DICOM file and extracts the image."""
    dicom_data = pydicom.dcmread(file)
    image_array = dicom_data.pixel_array  

    # If 3D (multi-slice), extract the middle slice
    if image_array.ndim == 3:
        mid_slice = image_array.shape[0] // 2
        image_array = image_array[mid_slice]

    # Normalize image (Rescale intensity to [0, 255])
    image_array = rescale_intensity(image_array.astype(np.float32), out_range=(0, 255))
    
    # Convert grayscale to RGB (for display)
    image_array = np.stack([image_array] * 3, axis=-1).astype(np.uint8)
    
    return Image.fromarray(image_array)


st.title("DICOM Image Viewer")

uploaded_file = st.file_uploader("Upload a DICOM file", type=["dcm"])

if uploaded_file is not None:
    try:
        # Load and process the DICOM image
        dicom_image = load_dicom(uploaded_file)
        
        # Display the image in Streamlit
        st.image(dicom_image, caption="DICOM Image", use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading DICOM: {e}")
