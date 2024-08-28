from dotenv import load_dotenv
load_dotenv()

import io
import base64
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash-latest")
    response=model.generate_content([input,pdf_content[0],prompt])   #inputing some content based ont he prompt
    return response.text


def input_pdf_setup(uploaded_file):
    # Convert the uploaded PDF to images
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())  #reading and converting from bytes

        first_page=images[0]

        #convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts=[
            {
                'mime_type':'image/jpeg',
                'data':base64.b64encode(img_byte_arr).decode()  #enode to base 64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")


# Streamlit App

st.set_page_config(page_title="ResumeFit")
st.header("An Intelligent System for Matching and Enhancing Resumes")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload Your Resume(PDF only)...",type=['pdf'])

if uploaded_file is not None:
    st.write("PDF Upload Successful")

submit1=st.button("Tell about my resume...")
submit2=st.button("How can I Improvise my Skills")
submit3=st.button("Percentage Match")


input_prompt1=""" 
You are an Experienced HR with Expertise in Field of any one job role from  Data Science or Full Stack Web Development or
Big Data Engineering or DEVOPS or Data Analysis, your task is to review the providede resune against the 
Job Description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with it.
Highlight the strengths and weaknesses of the applicant in relation ot the specified job role.
"""

input_prompt3="""
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack Web Development
, Big Data Engineering, DEVOPS, Data Analysis and deep ATS functionality, your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches with the job description. First the output should come as the percentage and then keywords missing
in the resume and final insights.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader('Insights: ')
        st.write(response)
    else:
        st.write('Please Upload the Resume')

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader('Insights: ')
        st.write(response)
    else:
        st.write('Please Upload the Resume')
