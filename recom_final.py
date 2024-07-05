import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure the generative AI model
genai.configure(api_key="AIzaSyDfKTgXJAIIlcl1iGlEAE682ZRJAl3MGKk")

# Gemini function
def gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(input_text)
    return response.text

st.title('Recommendation System')

with st.form("Student_details_form"):
    user_name = st.text_input("Enter Your Name")
    age = st.slider("What is your Age", 0, 100)
    email = st.text_input("Enter Your Email")
    gender = st.radio("What is your Gender", ("Male", "Female"))
    date_of_birth = st.date_input("Your DOB", datetime(2024, 6, 21))
    ph_no = st.text_input("Enter Your Phone Number")
    student_id = st.text_input("Enter Your Registration ID")
    courses = st.multiselect(
        "What are the courses you have enrolled in",
        ["Data Science", "Data Analytics", "Data Engineering", "GenAI"]
    )
    course_duration = st.slider("What is your course duration (in weeks)?", 0, 100)
    modules_completed = st.slider("What percentage of modules have you completed?", 0, 100)
    attendance = st.slider("What is your attendance percentage?", 0, 100)
    resume_building = st.selectbox("Have you built your resume?", ("Yes", "No"))
    projects_completed = st.slider("Projects Completed (%)", 0, 100)
    projects_viva = st.slider("Projects Viva Cleared (%)", 0, 100)
    research_papers_completed = st.slider("Research Papers Completed (%)", 0, 100)
    assignments_completed = st.slider("Assignments Completed (%)", 0, 100)
    quizzes_completed = st.slider("Quizzes Completed (%)", 0, 100)
    interview_preparedness = st.selectbox("Are you prepared for interviews?", ("Yes", "No"))
    submitted = st.form_submit_button("Submit")

    if submitted:
        # Calculate due work
        modules_due = 100 - modules_completed
        projects_due = 100 - projects_completed
        research_papers_due = 100 - research_papers_completed
        assignments_due = 100 - assignments_completed
        quizzes_due = 100 - quizzes_completed
        interview_preparedness_due = 100 if interview_preparedness == "No" else 0

        input_prompt = f'''
        Student Profile:
        Name: {user_name}
        Age: {age}
        Gender: {gender}
        Date of Birth: {date_of_birth}
        Email: {email}
        Phone Number: {ph_no}
        Student ID: {student_id}
        Courses Taken: {', '.join(courses)}
        Course Duration: {course_duration} weeks
        Modules Completed: {modules_completed}%
        Modules Due: {modules_due}%
        Attendance: {attendance}%
        Resume Building: {resume_building}
        Projects Completed: {projects_completed}%
        Projects Due: {projects_due}%
        Projects Viva Cleared: {projects_viva}%
        Research Papers Completed: {research_papers_completed}%
        Research Papers Due: {research_papers_due}%
        Assignments Completed: {assignments_completed}%
        Assignments Due: {assignments_due}%
        Quizzes Completed: {quizzes_completed}%
        Quizzes Due: {quizzes_due}%
        Interview Preparedness: {interview_preparedness}
        Interview Preparedness Due: {interview_preparedness_due}%
        
        Provide detailed and specific recommendations for improving the student's job placement chances and areas of improvement, including:

        1. How to complete due modules.
        2. How to complete due projects.
        3. How to complete due research papers.
        4. How to complete due assignments.
        5. How to complete due quizzes.
        6. How to improve interview preparedness.
        
        
        provide recommendations on how to complete them by suggesting relevant 360digiTMG courses.
        Additionally, provide guidance on maintaining a balance between these areas to ensure holistic progress.
        
        while giving recommendation incule the below:
        Handy study materials: Relevant articles, video lectures, or interactive modules to address specific learning needs.
        - Engaging Discussions: Connect with peers and instructors in relevant forum discussions to clarify doubts and share perspectives. Direct them to the discussion forum of AISPRY website LINK: https://aispry.com/forum
        - Project-focused Workshops or Mentorship (if applicable): Get hands-on guidance if applying concepts to practical projects is a challenge. Suggest talking to the team leader.
        - Career Support (if applicable): Learn how to translate your learnings into a strong resume with resume mapping sessions.
          If the resume building session is not attended then suggest this link: https://360digitmg.com/resume-mapper
          If any doubts then suggest a doubt clarification session.

        
        if all the threshold requirements are almost met suggest suitable data science companies in India they can apply to.
        

        '''
        recommendation = gemini_response(input_prompt)
        
        st.subheader("Computed Values")
        st.write(f"Modules Due: {modules_due}%")
        st.write(f"Projects Due: {projects_due}%")
        st.write(f"Research Papers Due: {research_papers_due}%")
        st.write(f"Assignments Due: {assignments_due}%")
        st.write(f"Quizzes Due: {quizzes_due}%")
        st.write(f"Interview Preparedness Due: {interview_preparedness_due}%")
        
        # st.subheader("Recommendation")
        st.write(recommendation)
