import os
from io import BytesIO
import streamlit as st
import PIL.Image as Image
from dotenv import load_dotenv
from processing import Preprocessor
from models import GeminiImageAnalyzer
from core import Patient, Study, Report

preprocessor = Preprocessor(target_size=(128, 128))
# Streamlit App Title
st.title("💬 MedAnalytix Chatbot")
st.write("A Medical Vision Language Model Platform for Medical Image Analysis.")

API_KEY = st.text_input("Enter Gemini API Key:", type="password")
if API_KEY:
    analyzer = GeminiImageAnalyzer(API_KEY)

# tracking chat history and patient data
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if "patient" not in st.session_state:
    st.session_state.patient = None
    
if "study_id_counter" not in st.session_state:
    st.session_state.study_id_counter = 1
    
if "reports" not in st.session_state:
    st.session_state.reports = []

# "New Chat" Button
if st.button("🔄 New Chat"):
    st.session_state.clear() 
    st.rerun()  

# Patient Information Section
st.sidebar.header("📋 Patient Information")

with st.sidebar.form("patient_form"):
    patient_id = st.text_input("Patient ID", key="patient_id")
    patient_name = st.text_input("Patient Name", key="patient_name")
    patient_age = st.number_input("Age", min_value=0, max_value=120, key="patient_age")
    patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="patient_gender")
    
    # Medical history as a multi-line text area
    medical_history = st.text_area("Medical History (separate conditions with commas)", key="medical_history")
    
    submit_patient = st.form_submit_button("Save Patient Info")
    
    if submit_patient:
        # Convert medical history string to list
        medical_history_list = [item.strip() for item in medical_history.split(",") if item.strip()]
        
        # Create Patient object
        st.session_state.patient = Patient(
            patient_id,
            patient_name,
            patient_age,
            patient_gender,
            medical_history_list
        )
        st.sidebar.success("Patient information saved!")

# Display patient info if available
if st.session_state.patient:
    st.sidebar.subheader("Current Patient")
    st.sidebar.info(st.session_state.patient.patient_info_summary())

# File Uploader
uploaded_file = st.file_uploader("📤 Upload a medical image...", type=["jpg", "jpeg", "png", "bmp", "dcm"])

# Study information (only show when a patient exists and a file is uploaded)
if st.session_state.patient and uploaded_file is not None and "study" not in st.session_state:
    with st.form("study_form"):
        st.subheader("Study Information")
        study_id = st.text_input("Study ID", value=f"STUDY{st.session_state.study_id_counter:03d}")
        modality = st.selectbox("Modality", ["MRI", "CT Scan", "X-Ray", "Ultrasound", "PET", "Other"])
        
        submit_study = st.form_submit_button("Create Study")
        
        if submit_study:
            # Create Study object
            study = Study(study_id, modality, st.session_state.patient)
            st.session_state.study = study
            st.session_state.study_id_counter += 1
            st.success(f"Study {study_id} created successfully!")

if uploaded_file is not None and "image_processed" not in st.session_state:
    try:
        with st.spinner("🔄 Analyzing image... Please wait."):
            # Load and preprocess the image
            preprocessed_image = preprocessor.preprocess_file(uploaded_file)

            img_byte_arr = BytesIO()
            preprocessed_image.save(img_byte_arr, format="PNG")
            img_byte_arr = img_byte_arr.getvalue()
            st.session_state["image_bytes"] = img_byte_arr
            
            # Get patient and study information if available
            patient_info = None
            study_info = None
            
            if st.session_state.patient:
                patient_info = st.session_state.patient.patient_info_summary()
                
            if "study" in st.session_state:
                study_info = st.session_state.study.get_study_details()
            
            # Analyze the image with patient and study context
            preliminary_report = analyzer.analyze_image(
                preprocessed_image, 
                patient_info=patient_info,
                study_info=study_info
            )[0]

            st.session_state.chat_history.append({"role": "user", "content": img_byte_arr})
            st.session_state.chat_history.append({"role": "assistant", "content": preliminary_report})
            st.session_state["image_processed"] = preprocessed_image
            
            # Extract findings and diagnosis from the preliminary report
            findings = ""
            diagnosis = ""
            
            # Simple parsing of the report text to extract findings and diagnosis
            report_lines = preliminary_report.split('\n')
            for line in report_lines:
                if "**Findings:**" in line:
                    findings = line.replace("**Findings:**", "").strip()
                if "**Possible Diagnosis:**" in line:
                    diagnosis = line.replace("**Possible Diagnosis:**", "").strip()
            
            # Store extracted findings and diagnosis
            st.session_state["findings"] = findings
            st.session_state["diagnosis"] = diagnosis

    except Exception as e:
        st.error(f"❌ Error processing the request: {e}")

# Display study information if available
if "study" in st.session_state:
    st.subheader("Study Details")
    st.info(st.session_state.study.get_study_details())
    
    # Add a section to generate a formal report
    if "image_processed" in st.session_state and "findings" in st.session_state:
        st.subheader("Generate Formal Report")
        
        with st.form("report_form"):
            # Pre-fill with AI-generated findings and diagnosis
            findings = st.text_area("Findings", value=st.session_state.get("findings", ""))
            diagnosis = st.text_area("Diagnosis", value=st.session_state.get("diagnosis", ""))
            recommendations = st.text_area("Recommendations", value="")
            
            generate_report = st.form_submit_button("Generate Report")
            
            if generate_report:
                # Create a Report object
                report = Report(st.session_state.study, findings, diagnosis)
                
                # Add recommendations attribute to the Report object (not in the original class)
                report.recommendations = recommendations
                
                # Add the report to the session state
                st.session_state.reports.append(report)
                
                st.success("Report generated successfully!")

# Display generated reports if available
if st.session_state.reports:
    st.subheader("Generated Reports")
    
    for i, report in enumerate(st.session_state.reports):
        with st.expander(f"Report for Study {report.study.study_id}"):
            st.markdown(f"**Patient:** {report.study.patient.name} (ID: {report.study.patient.patient_ID})")
            st.markdown(f"**Modality:** {report.study.modality}")
            st.markdown(f"**Findings:** {report.findings}")
            st.markdown(f"**Diagnosis:** {report.diagnosis}")
            if hasattr(report, 'recommendations'):
                st.markdown(f"**Recommendations:** {report.recommendations}")

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
            
            # Add patient context if available
            if st.session_state.patient:
                patient_context = f"Patient Information: {st.session_state.patient.patient_info_summary()}"
                conversation_context = patient_context + "\n\n" + conversation_context
                
            # Add study context if available
            if "study" in st.session_state:
                study_context = f"Study Information: {st.session_state.study.get_study_details()}"
                conversation_context = study_context + "\n\n" + conversation_context

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