import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#gemini pro api response

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)

    return response.text

#handling the pdf
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    
    for page in range(len(reader.pages)): 
        page = reader.pages[page] #extracting info from these pages
        text += str(page.extract_text()) #putting the content from that page to text variable and converting into string
    
    return text


# Prompt Template
input_prompt = """
Hey, act like a highly skilled and experienced ATS (Application Tracking System) with deep expertise in the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to evaluate the provided resume against the given job description with a high degree of accuracy. The job market is very competitive, so you must provide the best possible assistance for improving the resume. Assign the percentage matching based on the job description and identify the missing keywords with high accuracy.

Your evaluation should include the following components:
1. JD Match Percentage: Calculate the percentage match between the resume and the job description.
2. Missing Keywords: Identify any missing keywords that are crucial for the job description.
3. Profile Summary: Summarize the candidate’s profile based on the resume and how well it fits the job description.
4. Education Background Check: Specifically check if the candidate’s educational background meets the requirements stated in the job description.
5: Check Project work: check the project section and experience section and find out the technical skills and if some are remaining find out them and suggest a good project that one should add inorder to be hired for the role. Give example name and problem statement too
Consider the following details from both the resume and the job description:
- Relevant skills and technologies.
- Work experience and roles.
- Educational qualifications.
- Certifications (if any).
- Specific projects or achievements relevant to the job description.

Provide your response in a single structured string with the following format:
{{"JD Match":"<percentage>%","MissingKeywords":[<keywords>],"Profile Summary":"<summary>","Project That this person should add in the resume":[<Name of projects>]}}

Here are the details for evaluation:
- Resume: {text}
- Job Description: {jd}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume for ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

if st.button("Submit"):
    if uploaded_file is not None and jd is not None:
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt.format(text=text, jd=jd)
        
        response_text = get_gemini_response(prompt)
        
        # Parse the JSON response
        response_json = json.loads(response_text)
        
        st.subheader("Job Description Match Percentage")
        st.write(response_json["JD Match"])

        st.subheader("Missing Keywords")
        st.write(", ".join(response_json["MissingKeywords"]))

        st.subheader("Profile Summary")
        st.write(response_json["Profile Summary"])

        st.subheader("Recommended Improvements")
        st.write("Here are some areas you can improve in your resume based on the job description:")
        # This can include more detailed feedback, parsing the profile summary and missing keywords to generate actionable items.
        improvements = []
        if "education" in response_json["Profile Summary"].lower():
            improvements.append("Ensure your education section meets the job requirements.")
        if response_json["MissingKeywords"]:
            improvements.append("Include the missing keywords in your resume: " + ", ".join(response_json["MissingKeywords"]))
        
        projects = response_json.get("Project That this person should add in the resume")
        if projects:
            if isinstance(projects, list):
                project_names = [project.get("Name of projects", "") for project in projects]
                project_str = ", ".join(project_names)
                improvements.append("Projects: " + project_str)
            else:
                project_name = projects.get("Name of projects", "")
                improvements.append("Projects: " + project_name)
        
        for improvement in improvements:
            st.write(f"- {improvement}")
    else:
        st.write("Please ensure you have submitted all the required materials")