# MedAnalytix: Neuro Ashanti Medical Vision-Language Model Platform for Image Analysis and Report Generation

MedAnalytix is a Medical Vision Language Model Platform designed for analyzing medical images using Gemini. It allows users to upload medical images, receive preliminary AI-generated reports, and ask further questions in a chatbot-like interface.

## Screenshots

![App Screenshot](screenshots/image.png)
![App Screenshot](screenshots/Screenshot%202025-03-20%20205544.png)
![App Screenshot](screenshots/Screenshot%202025-03-20%20182202.png)

## Features

- Suport standard image formats (JPG, PNG, BMP)
- Supports DICOM files
- AI-Based Medical Analysis
- Start New Chats Anytime

## Run Locally

Clone the project

```bash
  git clone https://github.com/Ctankomah/Neuro-Ashanti-Medical-Vision-Language-Model-Platform-for-Image-Analysis-and-Report-Generation
```

Go to the project directory

```bash
  cd Neuro-Ashanti-Medical-Vision-Language-Model-Platform-for-Image-Analysis-and-Report-Generation-master
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set Up API Key

Get your Gemini API key from https://aistudio.google.com/apikey and update the .env file

Start the server

```bash
  streamlit run app.py
```
