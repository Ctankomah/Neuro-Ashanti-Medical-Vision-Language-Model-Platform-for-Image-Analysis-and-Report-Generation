import google.generativeai as genai
import os

class GeminiImageAnalyzer:
    def __init__(self, api_key):
        """Initialize the GeminiImageAnalyzer with the API key."""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def analyze_image(self, image, patient_info=None, study_info=None):
        report = []

        # Include patient information in the prompt if available
        patient_context = ""
        if patient_info:
            patient_context = f"""
            Patient Information:
            {patient_info}
            """
            
        study_context = ""
        if study_info:
            study_context = f"""
            Study Information:
            {study_info}
            """

        # Prompt to guide AI response
        prompt = f"""
        You are an AI medical assistant analyzing medical images.
        Provide a structured preliminary report based on the image.
        
        {patient_context}
        {study_context}
        
        Format the report like this:

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

    @staticmethod
    def print_formatted_report(report):
        """Prints the AI-generated report in a clean format."""
        print("\n" + "="*50)  # Adds a separator
        print("📌 **PRELIMINARY MEDICAL REPORT**".center(50))
        print("="*50)
        print(report)
        print("="*50 + "\n")  # End with a separator


# Example usage
if __name__ == "__main__":
    API_KEY = os.getenv("GEMINI_API_KEY")
    image_objects = [...]  # This should be the output from the preprocessing team

    analyzer = GeminiImageAnalyzer(API_KEY)
    preliminary_report = analyzer.analyze_image(image_objects[0], patient_info="Patient Name: John Doe, Age: 30", study_info="Study Type: MRI")
    analyzer.print_formatted_report(preliminary_report)