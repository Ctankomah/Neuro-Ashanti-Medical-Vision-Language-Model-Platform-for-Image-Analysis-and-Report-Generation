import google.generativeai as genai
import os

class GeminiImageAnalyzer:
    def __init__(self, api_key):
        """Initialize the GeminiImageAnalyzer with the API key."""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_image(self, image, patient_info_summary):
        report = []

        # Prompt to guide AI response
        prompt = f"""
        You are an AI medical assistant analyzing medical images.
        Provide a structured preliminary report based on the image.
        Use the provided patient information summary which is {patient_info_summary} to guide your analysis.
        Format the report like this:

            {patient_info_summary} Make the keys of the summary bold and separate the summary with new lines
        - **Findings:** (Describe abnormalities or normal conditions)
        - **Possible Diagnosis:** (Give possible conditions based on findings)
        - **Confidence Level:** (Indicate low, medium, or high confidence)
        - **Recommended Next Steps:** (Suggest further tests or medical consultation)

        **Analyze the provided medical image and respond in this format.**
        """

        try:
            response = self.model.generate_content([image, prompt])  # Send preprocessed image with prompt
            report.append(f"### PRELIMINARY MEDICAL REPORT\n{response.text}")  # Store structured report
        except Exception as e:
            report.append(f"⚠️ Error processing Image: {str(e)}")  # Handle errors

        return report
    
    def get_more_info(self, preprocessed_image, conversation_context, user_question):
        report = []

        # Prompt to guide AI response
        prompt = f"""
            You are an AI medical assistant analyzing medical images. 
            The user has provided an image, and you have already given a preliminary report.

            Previous conversation:
            {conversation_context}

            User's follow-up question:
            {user_question}

            Provide a response.
            """

        try:
            response = self.model.generate_content([preprocessed_image, prompt])  # Send preprocessed image with prompt
            report.append(f"{response.text}")
        except Exception as e:
            report.append(f"⚠️ Error processing Image: {str(e)}")  # Handle errors

        return report
