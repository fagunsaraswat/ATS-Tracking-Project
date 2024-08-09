import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import json

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#gemini pro api response

def get_gemini_response(input,pdf_content,prompt):
    """
    This function is used to get the response from the gemini api
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input,pdf_content[0],prompt])

    return response.text

#handling the pdf
def input_pdf_text(uploaded_file):
    """
    This function is used to get the pdf content from the uploaded file
    """
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    
    for page in range(len(reader.pages)): 
        page = reader.pages[page] #extracting info from these pages
        text += str(page.extract_text()) #putting the content from that page to text variable and converting into string
    
    return text


# Streamlit application (UI)
    

st.set_page_config(page_title = "ATS Resume Expert")
st.header("ATS Tracking System Version: 0.0.1")

input_text = st.text_area("Job Description: ",key = "input") #JD

uploaded_file = st.file_uploader("Upload your Resume (in pdf format): ", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Sucessfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my Resume")

submit3 = st.button("Missing Keywords and Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Provide the output with emphasis on missing skills and how the candidate can improve their Resume in general. For instance, you can mention any typos or grammatical errors.
"""     

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First, The output should come up as Percentage Match and then, the missing keywords.
"""     


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt1)

        st.subheader("The Response is :")
        st.write(response)
    
    else:
        st.write("Please Upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt2)

        st.subheader("The Response is :")
        st.write(response)
    
    else:
        st.write("Please Upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_text,pdf_content,input_prompt3)

        st.subheader("The Response is :")
        st.write(response)
    
    else:
        st.write("Please Upload the resume")
