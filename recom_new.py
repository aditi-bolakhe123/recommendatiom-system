import streamlit as st
import google.generativeai as genai
import spacy

# Configure the generative AI model (assuming API key is available)
genai.configure(api_key="AIzaSyDfKTgXJAIIlcl1iGlEAE682ZRJAl3MGKk")  # Replace with your actual API key

# Function to get a response from the generative AI model with improved personalization
def get_gemini_response(input_prompt, user_problem):
    model = genai.GenerativeModel('gemini-pro')

    # Prioritize user problem keywords for personalization
    keywords = extract_keywords(user_problem)  # Implement a keyword extraction function
    personalized_prompt = input_prompt.format(jd=user_problem, keywords=keywords)

    response = model.generate_content(personalized_prompt)
    return response.text

# Function to extract keywords from user input (implementation example)
def extract_keywords(text):
    # Use a suitable NLP library (e.g., spaCy, NLTK) for keyword extraction
    # This is a basic example, customize it for your specific needs
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "VERB"]
    return keywords

# Dummy data for Sarah Johnson
dummy_data = """
**Personal Details:**
- **Name:** Sarah Johnson
- **Student ID:** J654321
- **Gender:** Female
- **Email:** sarahjohnson@gmail.com
- **Phone:** 2354689076
- **Date of Birth:** 23/6/2024

**Course Details:**
- **Courses Offered:** Cybersecurity Certification Program
- **Course Start Date:** March 1, 2023
- **Course End Date:** August 31, 2023

**Academic Progress:**
- **Modules Completed:** 8 out of 8 (100%)
- **Modules Due:** 0
- **Classes Attended:** 92%
- **Courses Completed:** 5
- **Courses Due:** 5
- **Assignments Finished:** 15 out of 15 (100%)
- **Assignments Due:** 0

**Projects:**
- **Total Projects Completed:** 4
- **Projects Due:** 2
- **Submission of Each Project:** 4
- **Cleared Viva for Projects:** 1 out of 4
- **Resume Uploaded:** Yes
- **Discussion Forum Participation:** Yes
  - **Academic Projects:** 3
  - **Personal Projects:** 1

**Quizzes:**
- **Quizzes Completed:** 12 out of 12 (100%)
- **Quizzes Marks:** 10/10

**Research Papers:**
- **Research Papers Submitted:** 6 out of 10
- **Research Papers Completed:** 5 out of 10
- **Research Papers Due:** 5

**Attendance:**
- **Overall Attendance:** 94%

**Courses Completed:**
1. Introduction to Cybersecurity (Grade: A)
2. Network Security (Grade: A-)
3. Ethical Hacking Fundamentals (Grade: B+)
4. Cryptography Basics (Grade: A)
5. Incident Response and Forensics (Grade: A-)

**Projects Details:**
1. Network Penetration Testing
2. Cybersecurity Incident Simulation
3. Security Awareness Campaign
4. Personal Cybersecurity Blog
"""

# Input prompt template with keyword placeholder
input_prompt = """
You are a machine learning model designed to provide personalized learning recommendations for students at 360digiTMG. A student named Sarah Johnson has recently completed a course, and we need to recommend additional learning resources and activities to help her further her knowledge and skills. Here is a detailed breakdown of her performance and academic progress:

{jd}

**Task:**

1. **Analyze Sarah’s Potential Learning Style:**
   - Based on her performance in modules, quizzes, assignments, and projects, infer her potential learning style (e.g., visual, auditory, kinesthetic).
   - Explain how her performance varies across different course components.

2. **Provide Specific Recommendations:**
   - Considering Sarah's progress and potential learning style, recommend specific learning resources and activities available on 360digiTMG that would be most beneficial for her.

**Example Recommendations:**

- **For Improvement in Projects:**
  - Recommend personalized project mentoring sessions.
  - Suggest enrolling in a project-focused workshop relevant to the completed course.

- **Based on Learning Style:**
  - If Sarah performs better in quizzes and assignments (indicating a strong grasp of concepts), recommend video lectures or interactive modules to solidify her understanding.
  - If Sarah excels in assignments (indicating practical application skills), recommend enrolling in a course with more hands-on projects.

**Constraints:**
- Ensure recommendations are relevant and personalized to Sarah’s needs.
- Avoid recommending resources Sarah has already completed.
- Provide a balance between theory, practice, and hands-on projects to promote holistic learning.

Create a detailed and personalized recommendation for Sarah Johnson’s continued education at 360digiTMG.
"""

# Streamlit interface
st.title("Recommendation System")

st.subheader("Student Data")
st.text(dummy_data)

st.subheader("Adjust Sarah Johnson's Academic Progress")

# Add sliders for various academic progress parameters
projects_completed = st.slider("Projects Completed (%)", 0, 100, 67)
assignments_completed = st.slider("Assignments Completed (%)", 0, 100, 100)
quizzes_completed = st.slider("Quizzes Completed (%)", 0, 100, 100)
attendance = st.slider("Attendance (%)", 0, 100, 94)
research_papers_completed = st.slider("Research Papers Completed (%)", 0, 100, 50)
modules_completed = st.slider("Modules Completed (%)", 0, 100, 100)

# Dummy data updated with slider values
dummy_data_updated = f"""
**Personal Details:**
- **Name:** Sarah Johnson
- **Student ID:** J654321
- **Gender:** Female
- **Email:** sarahjohnson@gmail.com
- **Phone:** 2354689076
- **Date of Birth:** 23/6/2024

**Course Details:**
- **Courses Offered:** Cybersecurity Certification Program
- **Course Start Date:** March 1, 2023
- **Course End Date:** August 31, 2023

**Academic Progress:**
- **Modules Completed:** {modules_completed}% (8 out of 8)
- **Modules Due:** 0
- **Classes Attended:** {attendance}%
- **Courses Completed:** 5
- **Courses Due:** 5
- **Assignments Finished:** {assignments_completed}% (15 out of 15)
- **Assignments Due:** 0

**Projects:**
- **Total Projects Completed:** {projects_completed}% (4 out of 6)
- **Projects Due:** 2
- **Submission of Each Project:** 4
- **Cleared Viva for Projects:** 1 out of 4
- **Resume Uploaded:** Yes
- **Discussion Forum Participation:** Yes
  - **Academic Projects:** 3
  - **Personal Projects:** 1

**Quizzes:**
- **Quizzes Completed:** {quizzes_completed}% (12 out of 12)
- **Quizzes Marks:** 10/10

**Research Papers:**
- **Research Papers Submitted:** {research_papers_completed}% (6 out of 10)
- **Research Papers Completed:** 5 out of 10
- **Research Papers Due:** 5

**Attendance:**
- **Overall Attendance:** {attendance}%

**Courses Completed:**
1. Introduction to Cybersecurity (Grade: A)
2. Network Security (Grade: A-)
3. Ethical Hacking Fundamentals (Grade: B+)
4. Cryptography Basics (Grade: A)
5. Incident Response and Forensics (Grade: A-)

**Projects Details:**
1. Network Penetration Testing
2. Cybersecurity Incident Simulation
3. Security Awareness Campaign
4. Personal Cybersecurity Blog
"""

jd = st.text_area("State Problem")

submit = st.button('Recommend')
if submit:
    response = get_gemini_response(input_prompt.format(jd=dummy_data_updated), jd)
    st.subheader("Output")
    st.text(response)
