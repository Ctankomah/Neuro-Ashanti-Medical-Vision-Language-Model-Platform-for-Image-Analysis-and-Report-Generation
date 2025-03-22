import streamlit as st
import os
import PIL.Image as Image
from io import BytesIO
from dotenv import load_dotenv
from processing import Preprocessor
from models import GeminiImageAnalyzer
from core import Patient

load_dotenv()
preprocessor = Preprocessor(target_size=(128, 128))
API_KEY = os.getenv("GOOGLE_API_KEY")
analyzer = GeminiImageAnalyzer(API_KEY)
patient = Patient()

# Streamlit App Title
st.title("💬 MedAnalytix Chatbot")
st.write("A Medical Vision Language Model Platform for Medical Image Analysis.")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "upload"
if "image_processed" not in st.session_state:
    st.session_state.image_processed = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "patient_info" not in st.session_state:
    st.session_state.patient_info = {}

# "New Chat" Button
if st.button("🔄 New Chat"):
    st.session_state.clear()
    st.rerun()

# File Uploader Page
if st.session_state.page == "upload":
    uploaded_file = st.file_uploader("Upload a medical image...", type=["jpg", "jpeg", "png", "bmp", "dcm"])
    
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success("✅ File uploaded successfully. Please enter patient details.")
        
        patient_id = st.text_input("Patient ID", value=st.session_state.patient_info.get("id", ""))
        name = st.text_input("Name", value=st.session_state.patient_info.get("name", ""))
        age = st.number_input("Age", min_value=0, max_value=150, step=1, value=st.session_state.patient_info.get("age", 0))
        sex = st.selectbox("Sex", ["Male", "Female", "Unknown"], index=["Male", "Female", "Unknown"].index(st.session_state.patient_info.get("sex", "Unknown")))
        medical_history = st.text_area("Medical History", value=st.session_state.patient_info.get("medical_history", ""))

        # Replace empty values
        patient_id = patient_id if patient_id.strip() else "N/A"
        name = name if name.strip() else "N/A"
        medical_history = medical_history if medical_history.strip() else "N/A"

        # Save into session state
        st.session_state.patient_info = {
            "id": patient_id,
            "name": name,
            "age": age,
            "sex": sex,
            "medical_history": medical_history
        }

    
    if st.session_state.uploaded_file is not None and st.button("➡️ Proceed to analize"):
        st.session_state.page = "chat"
        st.rerun()

# Chatbot Page
elif st.session_state.page == "chat":
    # Process Image
    if "image_processed" not in st.session_state or st.session_state["image_processed"] is None:
        try:
            with st.spinner("🔄 Analyzing image... Please wait."):
                preprocessed_image = preprocessor.preprocess_file(st.session_state.uploaded_file)
                
                img_byte_arr = BytesIO()
                preprocessed_image.save(img_byte_arr, format="PNG")
                img_byte_arr = img_byte_arr.getvalue()
                st.session_state["image_bytes"] = img_byte_arr

                patient.new_patient(st.session_state.patient_info.get('id', 'N/A'),
                                    st.session_state.patient_info.get('name', 'N/A'),
                                    st.session_state.patient_info.get('age', 'N/A'),
                                    st.session_state.patient_info.get('sex', 'N/A'),
                                    st.session_state.patient_info.get('medical_history', 'N/A'))
                patient_info_summary = patient.patient_info_summary()

                # print(patient_info_summary)

                preliminary_report = analyzer.analyze_image(preprocessed_image, patient_info_summary)[0]

                st.session_state.chat_history.append({"role": "user", "content": img_byte_arr})
                st.session_state.chat_history.append({"role": "assistant", "content": preliminary_report})
                st.session_state["image_processed"] = preprocessed_image
        except Exception as e:
            st.error(f"❌ Error processing the request: {e}")
    
    # Display uploaded image
    # if "image_bytes" in st.session_state:
    #     st.image(Image.open(BytesIO(st.session_state["image_bytes"])), caption="🖼️ Uploaded Image", use_container_width=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message["role"] == "user" and isinstance(message["content"], bytes):
                st.image(Image.open(BytesIO(message["content"])), caption="🖼️ Uploaded Image", use_container_width=True)
            else:
                st.markdown(message["content"])
    
    # Chat input
    user_question = st.chat_input("💬 Ask me something...")
    if user_question:
        try:
            with st.spinner("💭 Thinking..."):
                conversation_context = "\n".join(
                    [f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history if isinstance(entry['content'], str)]
                )

                preprocessed_image = st.session_state["image_processed"]
                new_response = analyzer.get_more_info(preprocessed_image, conversation_context, user_question)[0]

                st.session_state.chat_history.append({"role": "user", "content": user_question})
                st.session_state.chat_history.append({"role": "assistant", "content": new_response})

                with st.chat_message("user"):
                    st.write(user_question)
                with st.chat_message("assistant"):
                    st.markdown(new_response)
        except Exception as e:
            st.error(f"❌ Error processing the request: {e}")
