import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="InternMatch - Find Your Perfect Internship",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .internship-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .skill-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 1rem;
        background-color: #e3f2fd;
        color: #1976d2;
        font-size: 0.9rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'courses' not in st.session_state:
    st.session_state.courses = []
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'psychometric_completed' not in st.session_state:
    st.session_state.psychometric_completed = False
if 'personality_type' not in st.session_state:
    st.session_state.personality_type = None

# Sample data (In production, this would come from your backend/database)
SAMPLE_INTERNSHIPS = [
    {
        "title": "Software Development Intern",
        "company": "Tech Corp",
        "location": "Bangalore, India",
        "type": "Remote",
        "stipend": "₹15,000/month",
        "required_skills": ["Python", "JavaScript", "React", "SQL"],
        "description": "Work on real-world web applications",
        "linkedin_url": "https://linkedin.com/jobs/sample1"
    },
    {
        "title": "Data Science Intern",
        "company": "Analytics Pro",
        "location": "Mumbai, India",
        "type": "Hybrid",
        "stipend": "₹20,000/month",
        "required_skills": ["Python", "Machine Learning", "Statistics", "SQL"],
        "description": "Build ML models for business insights",
        "linkedin_url": "https://linkedin.com/jobs/sample2"
    },
    {
        "title": "HR Management Intern",
        "company": "People First Inc",
        "location": "Delhi, India",
        "type": "On-site",
        "stipend": "₹12,000/month",
        "required_skills": ["Communication", "HR Management", "Recruitment"],
        "description": "Assist in recruitment and employee engagement",
        "linkedin_url": "https://linkedin.com/jobs/sample3"
    },
    {
        "title": "Digital Marketing Intern",
        "company": "Brand Boost",
        "location": "Remote",
        "type": "Remote",
        "stipend": "₹10,000/month",
        "required_skills": ["SEO", "Content Writing", "Social Media", "Analytics"],
        "description": "Manage social media campaigns and content",
        "linkedin_url": "https://linkedin.com/jobs/sample4"
    }
]

COURSE_SKILL_MAP = {
    "Data Structures and Algorithms": ["Python", "Problem Solving", "Algorithms"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React"],
    "Machine Learning": ["Python", "Machine Learning", "Statistics", "NumPy"],
    "Database Management": ["SQL", "Database Design", "MySQL"],
    "Human Resource Management": ["HR Management", "Recruitment", "Communication"],
    "Digital Marketing": ["SEO", "Content Writing", "Social Media", "Analytics"],
    "Business Analytics": ["Excel", "Statistics", "Data Analysis", "SQL"]
}

PSYCHOMETRIC_QUESTIONS = [
    {"q": "I enjoy solving complex logical problems", "trait": "analytical"},
    {"q": "I prefer working in teams rather than alone", "trait": "social"},
    {"q": "I am comfortable with public speaking", "trait": "communication"},
    {"q": "I like working with numbers and data", "trait": "analytical"},
    {"q": "I enjoy creative and artistic tasks", "trait": "creative"},
    {"q": "I am organized and detail-oriented", "trait": "organizational"},
    {"q": "I adapt easily to new technologies", "trait": "technical"},
    {"q": "I enjoy helping and guiding others", "trait": "social"},
    {"q": "I prefer structured tasks with clear guidelines", "trait": "organizational"},
    {"q": "I like experimenting with new ideas", "trait": "creative"}
]

def landing_page():
    st.markdown('<h1 class="main-header">🎓 InternMatch</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Bridge the gap between learning and career opportunities</h3>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Welcome to InternMatch
        
        **For Students:**
        - 🎯 Get personalized internship recommendations based on your courses
        - 🧠 Take psychometric tests to find your career fit
        - 📊 Analyze skill gaps and get learning suggestions
        - 📄 Build professional, role-specific resumes
        
        **For Recruiters:**
        - 📢 Post internship opportunities
        - 🔍 Search and filter qualified candidates
        - 💼 Manage applications efficiently
        - 🎯 Find candidates with the right skill and personality fit
        """)
        
        st.markdown("---")
        
        choice = st.radio("I am a:", ["Student", "Recruiter"], horizontal=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = "login"
                st.session_state.user_type = choice.lower()
                st.rerun()
        
        with col_b:
            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state.page = "signup"
                st.session_state.user_type = choice.lower()
                st.rerun()

def login_page():
    st.markdown('<h1 class="main-header">🔐 Login</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"### Login as {st.session_state.user_type.title()}")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("Login", use_container_width=True):
                # In production, validate with backend
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_data = {"email": email, "name": email.split("@")[0].title()}
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials")
        
        with col_b:
            if st.button("Back", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()

def signup_page():
    st.markdown('<h1 class="main-header">📝 Sign Up</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"### Register as {st.session_state.user_type.title()}")
        
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.session_state.user_type == "student":
            college = st.text_input("College/University")
            degree = st.text_input("Degree")
        else:
            company = st.text_input("Company Name")
            designation = st.text_input("Your Designation")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("Sign Up", use_container_width=True):
                if password == confirm_password and all([name, email, password]):
                    st.session_state.logged_in = True
                    st.session_state.user_data = {"email": email, "name": name}
                    st.success("Registration successful!")
                    st.rerun()
                else:
                    st.error("Please fill all fields and ensure passwords match")
        
        with col_b:
            if st.button("Back", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()

def student_dashboard():
    st.markdown(f'<h1 class="main-header">👋 Welcome, {st.session_state.user_data.get("name", "Student")}!</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 📚 Navigation")
        page = st.radio("Go to:", [
            "Dashboard",
            "Add Courses",
            "Psychometric Test",
            "Browse Internships",
            "Skill Gap Analysis",
            "Resume Builder"
        ])
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()
    
    if page == "Dashboard":
        show_student_dashboard_home()
    elif page == "Add Courses":
        show_add_courses()
    elif page == "Psychometric Test":
        show_psychometric_test()
    elif page == "Browse Internships":
        show_browse_internships()
    elif page == "Skill Gap Analysis":
        show_skill_gap_analysis()
    elif page == "Resume Builder":
        show_resume_builder()

def show_student_dashboard_home():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Courses Completed", len(st.session_state.courses))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Skills Identified", len(st.session_state.skills))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Recommended Internships", len(SAMPLE_INTERNSHIPS))
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Your Skills")
        if st.session_state.skills:
            skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in st.session_state.skills])
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.info("No skills added yet. Add courses to identify your skills!")
    
    with col2:
        st.markdown("### 🧠 Career Personality")
        if st.session_state.psychometric_completed:
            st.success(f"Type: {st.session_state.personality_type}")
        else:
            st.warning("Take the psychometric test to discover your career fit!")
            if st.button("Take Test Now"):
                st.session_state.page = "psychometric"
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 🌟 Top Recommended Internships")
    
    for i, internship in enumerate(SAMPLE_INTERNSHIPS[:3]):
        display_internship_card(internship)

def show_add_courses():
    st.markdown("### 📚 Add Your Completed Courses")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        course = st.selectbox(
            "Select Course",
            options=list(COURSE_SKILL_MAP.keys()),
            key="course_select"
        )
    
    with col2:
        if st.button("➕ Add Course", use_container_width=True):
            if course and course not in st.session_state.courses:
                st.session_state.courses.append(course)
                # Map skills
                new_skills = COURSE_SKILL_MAP[course]
                for skill in new_skills:
                    if skill not in st.session_state.skills:
                        st.session_state.skills.append(skill)
                st.success(f"Added {course}!")
                st.rerun()
            elif course in st.session_state.courses:
                st.warning("Course already added!")
    
    st.markdown("---")
    
    if st.session_state.courses:
        st.markdown("### 📖 Your Courses")
        
        for i, course in enumerate(st.session_state.courses):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{i+1}. {course}**")
                skills = COURSE_SKILL_MAP.get(course, [])
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in skills])
                st.markdown(skills_html, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_{i}"):
                    st.session_state.courses.pop(i)
                    st.rerun()
    else:
        st.info("No courses added yet. Start adding courses to identify your skills!")

def show_psychometric_test():
    st.markdown("### 🧠 Psychometric Test")
    st.markdown("Answer these questions to help us understand your personality and recommend the best-fit internships.")
    
    if st.session_state.psychometric_completed:
        st.success(f"✅ Test completed! Your personality type: **{st.session_state.personality_type}**")
        if st.button("Retake Test"):
            st.session_state.psychometric_completed = False
            st.rerun()
        return
    
    st.markdown("---")
    
    responses = {}
    
    for i, item in enumerate(PSYCHOMETRIC_QUESTIONS):
        st.markdown(f"**{i+1}. {item['q']}**")
        responses[i] = st.slider(
            "Strongly Disagree → Strongly Agree",
            1, 5, 3,
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        st.markdown("---")
    
    if st.button("📊 Submit Test", use_container_width=True):
        # Calculate personality type (simplified)
        trait_scores = {}
        for i, resp in responses.items():
            trait = PSYCHOMETRIC_QUESTIONS[i]["trait"]
            trait_scores[trait] = trait_scores.get(trait, 0) + resp
        
        dominant_trait = max(trait_scores, key=trait_scores.get)
        
        personality_map = {
            "analytical": "Analytical Thinker - Great for Data Science, Research",
            "social": "People Person - Perfect for HR, Management",
            "technical": "Tech Enthusiast - Ideal for Software Development",
            "creative": "Creative Innovator - Suited for Design, Marketing",
            "organizational": "Organized Planner - Excellent for Operations, PM"
        }
        
        st.session_state.personality_type = personality_map.get(dominant_trait, "Balanced Professional")
        st.session_state.psychometric_completed = True
        st.success("Test completed successfully!")
        st.rerun()

def show_browse_internships():
    st.markdown("### 🔍 Browse Internships")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location_filter = st.multiselect("Location", ["Bangalore", "Mumbai", "Delhi", "Remote"])
    
    with col2:
        type_filter = st.multiselect("Type", ["Remote", "On-site", "Hybrid"])
    
    with col3:
        skill_filter = st.multiselect("Skills", list(set([s for skills in COURSE_SKILL_MAP.values() for s in skills])))
    
    st.markdown("---")
    
    # Display internships
    filtered_internships = SAMPLE_INTERNSHIPS.copy()
    
    # Apply filters (simplified)
    if location_filter:
        filtered_internships = [i for i in filtered_internships if any(loc in i["location"] for loc in location_filter)]
    
    if type_filter:
        filtered_internships = [i for i in filtered_internships if i["type"] in type_filter]
    
    if skill_filter:
        filtered_internships = [i for i in filtered_internships if any(s in i["required_skills"] for s in skill_filter)]
    
    st.markdown(f"### Found {len(filtered_internships)} Internships")
    
    for internship in filtered_internships:
        display_internship_card(internship)

def display_internship_card(internship):
    st.markdown('<div class="internship-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### {internship['title']}")
        st.markdown(f"**{internship['company']}** • {internship['location']} • {internship['type']}")
        st.markdown(f"💰 {internship['stipend']}")
        st.markdown(f"_{internship['description']}_")
        
        skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in internship['required_skills']])
        st.markdown(skills_html, unsafe_allow_html=True)
    
    with col2:
        if st.button("Apply on LinkedIn", key=f"apply_{internship['title']}", use_container_width=True):
            st.success("Redirecting to LinkedIn...")
        
        # Match percentage
        if st.session_state.skills:
            matched = len(set(internship['required_skills']) & set(st.session_state.skills))
            total = len(internship['required_skills'])
            match_pct = (matched / total) * 100
            st.metric("Skill Match", f"{match_pct:.0f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_skill_gap_analysis():
    st.markdown("### 📊 Skill Gap Analysis")
    
    if not st.session_state.courses:
        st.warning("Please add courses first to perform skill gap analysis!")
        return
    
    st.markdown("Based on your current skills and trending internships, here are the skill gaps identified:")
    
    st.markdown("---")
    
    # Calculate skill gaps
    all_required_skills = set()
    for internship in SAMPLE_INTERNSHIPS:
        all_required_skills.update(internship['required_skills'])
    
    your_skills = set(st.session_state.skills)
    missing_skills = all_required_skills - your_skills
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Your Skills")
        for skill in your_skills:
            st.markdown(f"- {skill}")
    
    with col2:
        st.markdown("#### ⚠️ Skills to Develop")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"- {skill}")
        else:
            st.success("Great! You have all trending skills!")
    
    st.markdown("---")
    
    if missing_skills:
        st.markdown("### 📚 Recommended Learning Resources")
        
        learning_map = {
            "Python": "Python for Beginners - Coursera",
            "JavaScript": "JavaScript Essentials - Udemy",
            "React": "React Complete Guide - freeCodeCamp",
            "Machine Learning": "ML Specialization - Coursera",
            "SQL": "SQL Masterclass - DataCamp"
        }
        
        for skill in list(missing_skills)[:5]:
            resource = learning_map.get(skill, f"{skill} Tutorial - Online")
            st.info(f"🎓 **{skill}**: {resource}")

def show_resume_builder():
    st.markdown("### 📄 Resume Builder")
    
    st.markdown("Create a professional, role-specific resume based on your profile.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        resume_name = st.text_input("Your Name", value=st.session_state.user_data.get("name", ""))
        resume_email = st.text_input("Email", value=st.session_state.user_data.get("email", ""))
        resume_phone = st.text_input("Phone Number")
        resume_role = st.selectbox("Target Role", [
            "Software Developer",
            "Data Scientist",
            "HR Intern",
            "Marketing Intern",
            "Business Analyst"
        ])
    
    with col2:
        st.markdown("#### Resume Preview")
        st.info("Your resume will highlight skills relevant to the selected role")
    
    st.markdown("---")
    
    st.markdown("#### Professional Summary")
    summary = st.text_area(
        "Write a brief summary",
        value=f"Motivated student with skills in {', '.join(st.session_state.skills[:3])} seeking opportunities in {resume_role}."
    )
    
    st.markdown("#### Projects (Optional)")
    project_name = st.text_input("Project Name")
    project_desc = st.text_area("Project Description")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Generate PDF", use_container_width=True):
            st.success("Resume generated! (In production, this would download a PDF)")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("Resume draft saved!")

def recruiter_dashboard():
    st.markdown(f'<h1 class="main-header">👔 Recruiter Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"### Welcome, {st.session_state.user_data.get('name', 'Recruiter')}!")
    
    with st.sidebar:
        st.markdown("### 📚 Navigation")
        page = st.radio("Go to:", [
            "Dashboard",
            "Post Internship",
            "Search Candidates",
            "Manage Applications"
        ])
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "landing"
            st.rerun()
    
    if page == "Dashboard":
        show_recruiter_dashboard_home()
    elif page == "Post Internship":
        show_post_internship()
    elif page == "Search Candidates":
        show_search_candidates()
    elif page == "Manage Applications":
        show_manage_applications()

def show_recruiter_dashboard_home():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Posted Internships", "5")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Total Applications", "47")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Matched Candidates", "23")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Recent Activity")
    
    st.info("🎯 15 new applications received this week")
    st.success("✅ 3 internships filled successfully")
    st.warning("⚠️ 2 internship postings expiring soon")

def show_post_internship():
    st.markdown("### 📢 Post New Internship")
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title")
        company = st.text_input("Company Name")
        location = st.text_input("Location")
        job_type = st.selectbox("Type", ["Remote", "On-site", "Hybrid"])
    
    with col2:
        stipend = st.text_input("Stipend (e.g., ₹15,000/month)")
        duration = st.text_input("Duration (e.g., 3 months)")
        start_date = st.date_input("Start Date")
        openings = st.number_input("Number of Openings", min_value=1, value=1)
    
    st.markdown("#### Required Skills")
    skills = st.multiselect(
        "Select required skills",
        list(set([s for skills in COURSE_SKILL_MAP.values() for s in skills]))
    )
    
    st.markdown("#### Job Description")
    description = st.text_area("Describe the role and responsibilities", height=150)
    
    if st.button("📤 Post Internship", use_container_width=True):
        if all([job_title, company, location, stipend, skills, description]):
            st.success("✅ Internship posted successfully!")
        else:
            st.error("Please fill all required fields")

def show_search_candidates():
    st.markdown("### 🔍 Search Candidates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        skill_search = st.multiselect("Required Skills", ["Python", "JavaScript", "SQL", "Machine Learning"])
    
    with col2:
        personality_search = st.multiselect("Personality Type", [
            "Analytical Thinker",
            "People Person",
            "Tech Enthusiast",
            "Creative Innovator"
        ])
    
    with col3:
        course_search = st.multiselect("Courses", list(COURSE_SKILL_MAP.keys()))
    
    if st.button("🔎 Search", use_container_width=True):
        st.markdown("---")
        st.markdown("### 👥 Matched Candidates")
        
        # Sample candidates
        candidates = [
            {"name": "Rahul Sharma", "skills": ["Python", "SQL", "Machine Learning"], "match": 95},
            {"name": "Priya Patel", "skills": ["JavaScript", "React", "HTML"], "match": 88},
            {"name": "Amit Kumar", "skills": ["Python", "Django", "SQL"], "match": 85}
        ]
        
        for candidate in candidates:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"#### {candidate['name']}")
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate['skills']])
                st.markdown(skills_html, unsafe_allow_html=True)
            
            with col2:
                st.metric("Match Score", f"{candidate['match']}%")
            
            with col3:
                st.button("View Profile", key=f"view_{candidate['name']}")

def show_manage_applications():
    st.markdown("### 📋 Manage Applications")
    
    tabs = st.tabs(["New Applications", "Shortlisted", "Rejected"])
    
    with tabs[0]:
        st.markdown("#### 🆕 New Applications (12)")
        for i in range(3):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**Candidate {i+1}** - Software Development Intern")
                st.markdown("Applied 2 days ago")
            with col2:
                st.button("✅ Shortlist", key=f"short_{i}")
            with col3:
                st.button("❌ Reject", key=f"reject_{i}")
            st.markdown("---")
    
    with tabs[1]:
        st.markdown("#### ⭐ Shortlisted Candidates (5)")
        st.info("View and contact shortlisted candidates")
    
    with tabs[2]:
        st.markdown("#### 🚫 Rejected Applications (8)")
        st.info("Previously rejected applications")

# Main app logic
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    if not st.session_state.logged_in:
        if st.session_state.page == "landing":
            landing_page()
        elif st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "signup":
            signup_page()
    else:
        if st.session_state.user_type == "student":
            student_dashboard()
        elif st.session_state.user_type == "recruiter":
            recruiter_dashboard()

if __name__ == "__main__":
    main()
