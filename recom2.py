import streamlit as st 
import google.generativeai as genai 
import PyPDF2 as pdf 

# Configure Gemini API key
genai.configure(api_key = "AIzaSyDfKTgXJAIIlcl1iGlEAE682ZRJAl3MGKk")

# Gemini function to get response from Gemini model
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

# Function to convert PDF to text
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Placeholder function to fetch job offers
# Replace this with actual API call or database query
def fetch_job_offers(keywords):
    # Simulated job offers
    job_offers = [
        {"title": "Data Scientist", "location": "New York, USA", "salary": "$120,000", "link": "http://example.com/job1"},
        {"title": "Machine Learning Engineer", "location": "San Francisco, USA", "salary": "$130,000", "link": "http://example.com/job2"},
        {"title": "AI Researcher", "location": "Boston, USA", "salary": "$115,000", "link": "http://example.com/job3"},
    ]
    return job_offers

# Input prompt template
input_prompt = """
As a skilled Application Tracking System (ATS) with advanced knowledge in technology and data science, your role is to meticulously evaluate a candidate's resume based on the provided job description. 
Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for key buzzwords and specific criteria outlined in the job description to determine the candidate's suitability for the position.
Provide a detailed assessment of how well the resume matches the job requirements, highlighting strengths, weaknesses, and any potential areas of concern. Offer constructive feedback on how the candidate can enhance their resume to better align with the job description and improve their chances of securing the position.
Your evaluation should be thorough, precise, and objective, ensuring that the most qualified candidates are accurately identified based on their resume content in relation to the job criteria.
Remember to utilize your expertise in technology and data science to conduct a comprehensive evaluation that optimizes the recruitment process for the hiring company. Your insights will play a crucial role in determining the candidate's compatibility with the job role.
resume= {text}
jd= {jd}
Evaluation Output:
1. Calculate the percentage of match between the resume and the job description. Give a number 
2. Identify any key keywords that are missing from the resume in comparison to the job description.
3. Offer specific and actionable tips to enhance the resume and improve its alignment with the job requirements.
4. Provide job offers recommendations currently avalaible with comapny name, city, salary,link and job description in india.
"""

# Streamlit interface
st.title("Job Recommendation System")
st.text("Improve your resume score and get job recommendations")
jd = st.text_area("Paste job description here")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload the pdf")

submit = st.button('Check Your Score')

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))
        
        st.subheader("Evaluation Output")
        st.write(response)

        # Extract keywords from job description for fetching job offers
        # keywords = jd.split()  # Simplified keyword extraction
        # job_offers = fetch_job_offers(keywords)
        
        # st.subheader("Job Offers Recommendations")
        # for offer in job_offers:
        #     st.write(f"**Title:** {offer['title']}")
        #     st.write(f"**Location:** {offer['location']}")
        #     st.write(f"**Salary:** {offer['salary']}")
        #     st.write(f"[Job Link]({offer['link']})\n")
