import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import re
import mysql.connector

# Configure the generative AI 
# model
genai.configure(api_key="AIzaSyDfKTgXJAIIlcl1iGlEAE682ZRJAl3MGKk")

# MySQL connection function
def create_connection():
    return mysql.connector.connect(
        host='localhost',        # e.g., 'localhost'
        user='root',    # e.g., 'root'
        password='ANUaditi@123',# your MySQL password
        database='student_recommendation'
    )

# Function to insert recommendation into MySQL
def insert_recommendation(data):
    conn = create_connection()
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO recommendations (
        user_name, age, gender, date_of_birth, email, phone_number, student_id, courses,
        course_duration, modules_completed, modules_due, attendance, resume_building,
        projects_completed, projects_due, projects_viva, research_papers_completed, research_papers_due,
        assignments_completed, assignments_due, quizzes_completed, quizzes_due, interview_preparedness,
        interview_preparedness_due, recommendations
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        data['user_name'], data['age'], data['gender'], data['date_of_birth'], data['email'], data['phone_number'],
        data['student_id'], json.dumps(data['courses']), data['course_duration'], data['modules_completed'],
        data['modules_due'], data['attendance'], data['resume_building'], data['projects_completed'],
        data['projects_due'], data['projects_viva'], data['research_papers_completed'], data['research_papers_due'],
        data['assignments_completed'], data['assignments_due'], data['quizzes_completed'], data['quizzes_due'],
        data['interview_preparedness'], data['interview_preparedness_due'], json.dumps(data['recommendations'])
    ))
    conn.commit()
    cursor.close()
    conn.close()

# Gemini function
def gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(input_text)
    return response.text

def parse_recommendation_text(recommendation_text):
    parsed_recommendations = {}
    sections = re.split(r'\n\s*(\d+\.\s*.+)\s*(?=^\d+\.\s*|\Z)', recommendation_text.strip(), flags=re.MULTILINE)
    for section in sections:
        if section.strip():
            heading, *recommendations = section.strip().split('\n')
            heading = heading.strip(':')
            parsed_recommendations[heading] = [rec.strip('*') for rec in recommendations]
    return parsed_recommendations

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
        
        Provide recommendations on how to complete them by suggesting relevant 360digiTMG courses.
        Additionally, provide guidance on maintaining a balance between these areas to ensure holistic progress.
        
        While giving recommendations, include the below:
        Handy study materials: Relevant articles, video lectures, or interactive modules to address specific learning needs.
        - Engaging Discussions: Connect with peers and instructors in relevant forum discussions to clarify doubts and share perspectives. Direct them to the discussion forum of AISPRY website LINK: https://aispry.com/forum
        - Project-focused Workshops or Mentorship (if applicable): Get hands-on guidance if applying concepts to practical projects is a challenge. Suggest talking to the team leader.
        - Career Support (if applicable): Learn how to translate your learnings into a strong resume with resume mapping sessions. If the resume building session is not attended then suggest this link: https://360digitmg.com/resume-mapper
        If any doubts then suggest a doubt clarification session.
        
        If all the threshold requirements are almost met suggest suitable data science companies in India they can apply to.

        If resume building and interview preparedness are completed, ask if you have completed mock interviews (total 4) or not. If projects are completed, ask if your projects are industry level or not. Provide a yes or no button for user input. If the user puts option 'No', suggest taking mock interviews and doing industry-level projects. If the user puts 'Yes', tell them they have completed everything.
        
        '''

        recommendation_text = gemini_response(input_prompt)
        
        parsed_recommendations = parse_recommendation_text(recommendation_text)

        recommendation_data = {
            "user_name": user_name,
            "age": age,
            "gender": gender,
            "date_of_birth": str(date_of_birth),
            "email": email,
            "phone_number": ph_no,
            "student_id": student_id,
            "courses": courses,
            "course_duration": f"{course_duration} weeks",
            "modules_completed": f"{modules_completed}%",
            "modules_due": f"{modules_due}%",
            "attendance": f"{attendance}%",
            "resume_building": resume_building,
            "projects_completed": f"{projects_completed}%",
            "projects_due": f"{projects_due}%",
            "projects_viva": f"{projects_viva}%",
            "research_papers_completed": f"{research_papers_completed}%",
            "research_papers_due": f"{research_papers_due}%",
            "assignments_completed": f"{assignments_completed}%",
            "assignments_due": f"{assignments_due}%",
            "quizzes_completed": f"{quizzes_completed}%",
            "quizzes_due": f"{quizzes_due}%",
            "interview_preparedness": interview_preparedness,
            "interview_preparedness_due": f"{interview_preparedness_due}%",
            "recommendations": parsed_recommendations
        }

        # Insert recommendation data into MySQL
        insert_recommendation(recommendation_data)

        # Prepare JSON structure for display
        recommendation_json = {
            "Student Profile": {
                "Name": user_name,
                "Age": age,
                "Gender": gender,
                "Date of Birth": str(date_of_birth),
                "Email": email,
                "Phone Number": ph_no,
                "Student ID": student_id,
                "Courses Taken": courses,
                "Course Duration": f"{course_duration} weeks",
                "Modules Completed": f"{modules_completed}%",
                "Modules Due": f"{modules_due}%",
                "Attendance": f"{attendance}%",
                "Resume Building": resume_building,
                "Projects Completed": f"{projects_completed}%",
                "Projects Due": f"{projects_due}%",
                "Projects Viva Cleared": f"{projects_viva}%",
                "Research Papers Completed": f"{research_papers_completed}%",
                "Research Papers Due": f"{research_papers_due}%",
                "Assignments Completed": f"{assignments_completed}%",
                "Assignments Due": f"{assignments_due}%",
                "Quizzes Completed": f"{quizzes_completed}%",
                "Quizzes Due": f"{quizzes_due}%",
                "Interview Preparedness": interview_preparedness,
                "Interview Preparedness Due": f"{interview_preparedness_due}%"
            },
            "Recommendation": {
                "StudentName": user_name,
                "Recommendations": parsed_recommendations
            }
        }

        # Display JSON output
        st.subheader("Output in JSON")
        st.json(recommendation_json)
