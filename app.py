import streamlit as st
import os
import PIL.Image as Image
from io import BytesIO
from dotenv import load_dotenv
from processing import Preprocessor
from models import GeminiImageAnalyzer

load_dotenv()
preprocessor = Preprocessor(target_size=(128, 128))
API_KEY = os.getenv("GEMINI_API_KEY")
analyzer = GeminiImageAnalyzer(API_KEY)

# Streamlit App Title
st.title("💬 MedAnalytix Chatbot")
st.write("A Medical Vision Language Model Platform for Medical Image Analysis.")

# Session state to track chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# "New Chat" Button
if st.button("🔄 New Chat"):
    st.session_state.clear()  # Clear all stored data
    st.rerun()   # Refresh

# File Uploader
uploaded_file = st.file_uploader("📤 Upload a medical image...", type=["jpg", "jpeg", "png", "bmp", "dcm"])

if uploaded_file is not None and "image_processed" not in st.session_state:
    try:
        with st.spinner("🔄 Analyzing image... Please wait."):
            # Load and preprocess the image
            preprocessed_image = preprocessor.preprocess_file(uploaded_file)

            img_byte_arr = BytesIO()
            preprocessed_image.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
            st.session_state["image_bytes"] = img_byte_arr
            
            # Analyze the image
            preliminary_report = analyzer.analyze_image(preprocessed_image)[0]

            st.session_state.chat_history.append({"role": "user", "content": img_byte_arr})
            st.session_state.chat_history.append({"role": "assistant", "content": preliminary_report})
            st.session_state["image_processed"] = preprocessed_image

    except Exception as e:
        st.error(f"❌ Error processing the request: {e}")

# show chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["role"] == "user" and isinstance(message["content"], bytes):
            st.image(Image.open(BytesIO(message["content"])), caption="🖼️ Uploaded Image", use_container_width=True)
        else:
            st.markdown(message["content"])


user_question = st.chat_input("💬 Ask me something...")

if user_question:
    try:
        with st.spinner("💭 Thinking..."):
            conversation_context = "\n".join(
                [f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history if isinstance(entry['content'], str)]
            )

            preprocessed_image = st.session_state["image_processed"]
            # Get new response
            new_response = analyzer.get_more_info(preprocessed_image, conversation_context, user_question)[0]

            # Store new question and response
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            st.session_state.chat_history.append({"role": "assistant", "content": new_response})

            # dhow new responses
            with st.chat_message("user"):
                st.write(user_question)

            with st.chat_message("assistant"):
                st.markdown(new_response)

    except Exception as e:
        st.error(f"❌ Error processing the request: {e}")