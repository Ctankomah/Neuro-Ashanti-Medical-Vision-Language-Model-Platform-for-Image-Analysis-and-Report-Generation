import google.generativeai as genai
import os

# Configure Gemini AI API
API_KEY = os.getenv("GEMINI_API_KEY")  
genai.configure(api_key=API_KEY)



# Define function to analyze images with Gemini AI
def analyze_images_with_gemini(images):
    """Send images to Gemini AI and get structured preliminary reports."""
    model = genai.GenerativeModel("gemini-1.5-flash")  

    reports = []  # Store reports for all images

    for i, img in enumerate(images, 1):
        print(f"\n🔹 Processing Image {i}/{len(images)} 🔹")  #  Show progress

        # Prompt to guide AI response
        prompt = """
        You are an AI medical assistant analyzing medical images.
        Provide a structured preliminary report based on the image.
        Format the report like this:

        **Preliminary Medical Report**
        - **Findings:** (Describe abnormalities or normal conditions)
        - **Possible Diagnosis:** (Give possible conditions based on findings)
        - **Confidence Level:** (Indicate low, medium, or high confidence)
        - **Recommended Next Steps:** (Suggest further tests or medical consultation)

        **Analyze the provided medical image and respond in this format.**
        """

        try:
            response = model.generate_content([prompt, img])  #  Send image with prompt
            reports.append(f"### Image {i} Report\n{response.text}")  #  Store structured report
        except Exception as e:
            reports.append(f"⚠️ Error processing Image {i}: {str(e)}")  #  Handle errors

    return "\n\n".join(reports)  #  Combine all reports into a structured document


def print_formatted_report(report):
    """Prints the AI-generated report in a clean format."""
    print("\n" + "="*50)  #  Adds a separator
    print("📌 **PRELIMINARY MEDICAL REPORT**".center(50))
    print("="*50)
    print(report)
    print("="*50 + "\n")  #  End with a separator


#  Get AI-generated reports
preliminary_report = analyze_images_with_gemini(image_objects) #image_object will be the output from the preprecesing team

#  Print reports in a readable format
print_formatted_report(preliminary_report)
