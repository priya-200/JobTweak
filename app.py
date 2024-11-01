import streamlit as st
import os
import PyPDF2 as pdf
import json
import google.generativeai as genai
from dotenv import load_dotenv
import base64

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_genini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    if input != '':
        response = model.generate_content([input,pdf_content,prompt])
    else:
        response = model.generate_content([pdf_content,prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


## Streamlit applications

st.set_page_config(page_title = "JobTweak",
                   page_icon= "📄",
                   initial_sidebar_state= "collapsed",
                   layout="wide",
                   )

def display_footer():
    st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        font-size: 12px;
        color: grey;
        text-align: center;
    }
    </style>
    <div class="footer">
        <p>Created by PRIYADHARSHINI</p>
        <p>This application is designed to support college students in enhancing their resumes and preparing for job applications with confidence.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        body {
            background-color: #2E2E2E;
            color: white;
        }
        .navbar {
            background-color: #333;
            padding: 10px;
            display: flex;
            justify-content: space-around;
            color: white;
        }
        .navbar a {
            color: #ffffff;
            text-decoration: none;
            padding: 10px;
            border-radius: 5px;
        }
        .navbar a:hover {
            background-color: #555;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="navbar">
        <a href="?section=Home">Home</a>
        <a href="?section=Analyze Resume">Analyze Resume</a>
        <a href="?section=About Various Domains">About Various Domains</a>
    </div>
    """, unsafe_allow_html=True
)

section = st.query_params.get('section', 'Home')

if section == 'Home':
    st.title("Welcome to JobTweak")
    st.subheader("Optimize your resume for better job matches!")

    st.markdown(
        """
        With **JobTweak**, you can analyze and elevate your resume for a better match with job descriptions. Here’s how it works:

        ### How It Works
        1. **Upload Your Resume**: Submit your resume as a PDF.
        2. **Automated Analysis**: **JobTweak** converts the resume to text and applies advanced AI to assess it.
        3. **Input Job Description**: Enter the specific job description you're aiming to match.
        4. **Select Options**:
            - **Match Percentage**: Understand how well your resume aligns with the job description.
            - **Resume Feedback**: Receive insights on strengths and potential improvement areas.
            - **Keyword Suggestions**: Discover missing keywords to enhance your resume's relevance.
            - **Complete Overview**: Choose to get all features in one report.

        ### Tailored Insights Powered by Google’s Gemini AI
        Using AI, **JobTweak** delivers personalized suggestions to refine your resume, making it easier to stand out in job applications!
        """
    )
    display_footer()


elif section == 'Analyze Resume':
    st.header("JobTweak - Resume Analysis")
    input_text = st.text_area("Job Description: ", key="input", height=300)
    uploaded_file = st.file_uploader("Upload your resume(PDF)...",type = ['pdf'])

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully.")
        st.markdown(f"[View Uploaded Resume]({uploaded_file.name})")

        pdf_data = uploaded_file.getvalue()
        b64 = base64.b64encode(pdf_data).decode('utf-8')

        st.write("Here is a preview of your uploaded resume:")
        st.markdown(f'<iframe src="data:application/pdf;base64,{b64}" width="700" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)


    pdf_content = ""

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully.")

    submit1 = st.button("Tell me about my resume.")

    submit2 = st.button("What are the keywords that are missing.")

    submit3 = st.button("What is the percentage match of the job and my resume.")

    submit4 = st.button("All the above.")

    submit5 = st.button("Answer my query.")

    input_prompt1 = """
     You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
      Please share your professional evaluation on whether the candidate's profile aligns with the role. 
     Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt2 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. As a Human Resource manager,
     assess the compatibility of the resume with the role. Give me what are the keywords that are missing
     Also, provide recommendations for enhancing the candidate's skills and identify which areas require further development.
    """

    input_prompt3 = """
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
    """

    input_prompt4 = """
    You are a seasoned Technical Human Resource Manager and an expert in Applicant Tracking Systems (ATS), 
    tasked with performing a comprehensive evaluation of the provided resume against the job description.

    Please analyze and deliver:
    1. **Resume Overview**: Assess the candidate's profile strengths and weaknesses in relation to the role.
    2. **Keyword Matching**: Identify any missing keywords that may enhance the candidate's alignment with the job.
    3. **Match Percentage**: Provide a calculated percentage indicating how well the resume matches the job description.
    4. **Final Thoughts**: Offer professional recommendations for resume improvement, detailing areas for skill enhancement.

    Ensure a structured and thorough response to guide the candidate effectively.
    """

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file=uploaded_file)
            response = get_genini_response(input=input_text,prompt=input_prompt1,pdf_content=pdf_content)
            st.subheader("The response is : ")
            st.write(response)
        else:
            st.write("Please uploade the PDF file to proceed further.")



    if submit2:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file=uploaded_file)
            response = get_genini_response(input=input_text,prompt=input_prompt2,pdf_content=pdf_content)
            st.subheader("The response is : ")
            st.write(response)
        else:
            st.write("Please uploade the PDF file to proceed further.")



    if submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file=uploaded_file)
            response = get_genini_response(input=input_text,prompt=input_prompt3,pdf_content=pdf_content)
            st.subheader("The response is : ")
            st.write(response)
        else:
            st.write("Please uploade the PDF file to proceed further.")

    if submit4:
        if uploaded_file is not None:
            pdf_content = input_pdf_text(uploaded_file=uploaded_file)
            response = get_genini_response(input=input_text,prompt=input_prompt4,pdf_content=pdf_content)
            st.subheader("The response is : ")
            st.write(response)
        else:
            st.write("Please uploade the PDF file to proceed further.")

    display_footer()

elif section == "About Various Domains":
    st.title("This section provide students a complete road map of the various domains in the industry.")
    options = st.selectbox(
        'Choose your domain : ',
        ('Cloud Computing','Full Stack Technology','Cybersecurity',
'AI (ML & DL)','AR & VR','Blockchain Technology','DevOps','Mobile Application Development & Systems, Applications, and Products','Big Data Analytics & Data Science')
    )
    input_prompt_domain = '''
Imagine you are an expert across all major domains in computer science, well-versed in the latest technologies, industry trends, and research. 
A student seeks your guidance on a specific domain, and your task is to provide them with a comprehensive overview, including:

1. **Advantages**: Explain the benefits of pursuing a career in this domain.
2. **Disadvantages**: Outline potential challenges or limitations within this field.
3. **Skills Required**: Describe the essential skills and knowledge necessary for an entry-level job.
4. **Project Suggestions**: Recommend impactful projects that students can undertake to build relevant experience.
5. **Initial Salary**: Give an estimate of the typical starting salary for freshers in this domain.

Provide all relevant insights to help the student make an informed decision on this career path.
'''
    response = get_genini_response(pdf_content=options,prompt=input_prompt_domain,input = '')
    st.write(response)
    display_footer()
