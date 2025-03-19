import streamlit as st
from processing import Preprocessor

preprocessor = Preprocessor(target_size=(128, 128))

# Streamlit app
st.title("MedAnalytix")
st.write("A Medical Vision Language Model Platform for Image Analysis and Report Generation")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])


if uploaded_file is not None:
    # Preprocess the image
    try:
        preprocessed_image = preprocessor.preprocess_file(uploaded_file)
        st.write("Preprocessed image shape:", preprocessed_image.shape)

        # Display the preprocessed image
        st.image(preprocessed_image, caption="Preprocessed Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error processing the image: {e}")