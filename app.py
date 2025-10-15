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
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = True
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'education' not in st.session_state:
    st.session_state.education = []
if 'application_status' not in st.session_state:
    st.session_state.application_status = {}

# Custom CSS for styling with theme support
def apply_theme():
    if st.session_state.dark_mode:
        bg_color = "#0a1929"
        card_bg = "#1a2332"
        text_color = "#e0e0e0"
        border_color = "#2d3748"
        accent_color = "#3b82f6"
    else:
        bg_color = "#fafafa"
        card_bg = "#ffffff"
        text_color = "#1a1a1a"
        border_color = "#e0e0e0"
        accent_color = "#1f77b4"
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
        }}
        .main-header {{
            font-size: 2.5rem;
            font-weight: bold;
            color: {accent_color};
            text-align: center;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            padding: 1.5rem;
            border-radius: 1rem;
            background-color: {card_bg};
            border: 2px solid {border_color};
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .metric-value {{
            font-size: 3rem;
            font-weight: bold;
            color: {accent_color};
            margin: 0.5rem 0;
        }}
        .metric-label {{
            font-size: 1.1rem;
            color: {text_color};
            font-weight: 500;
        }}
        .internship-card {{
            padding: 1.5rem;
            border-radius: 0.5rem;
            background-color: {card_bg};
            border: 1px solid {border_color};
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .skill-badge {{
            display: inline-block;
            padding: 0.3rem 0.8rem;
            margin: 0.2rem;
            border-radius: 1rem;
            background-color: #e3f2fd;
            color: #1976d2;
            font-size: 0.9rem;
        }}
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 999;
        }}
        .candidate-card {{
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: {card_bg};
            border: 1px solid {border_color};
            margin-bottom: 1rem;
        }}
        .candidate-card.greyed {{
            opacity: 0.5;
            background-color: #f5f5f5;
        }}
        .status-message {{
            color: #666;
            font-style: italic;
            margin-top: 0.5rem;
        }}
        </style>
    """, unsafe_allow_html=True)

apply_theme()

# Sample data
SAMPLE_INTERNSHIPS = [
    {
        "id": 1,
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
        "id": 2,
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
        "id": 3,
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
        "id": 4,
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

SAMPLE_CANDIDATES = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "skills": ["Python", "SQL", "Machine Learning"],
        "courses": ["Machine Learning", "Database Management"],
        "personality": "Analytical Thinker",
        "match": 95,
        "resume_url": "resume1.pdf"
    },
    {
        "id": 2,
        "name": "Priya Patel",
        "email": "priya@example.com",
        "skills": ["JavaScript", "React", "HTML"],
        "courses": ["Web Development"],
        "personality": "Creative Innovator",
        "match": 88,
        "resume_url": "resume2.pdf"
    },
    {
        "id": 3,
        "name": "Amit Kumar",
        "email": "amit@example.com",
        "skills": ["Python", "Django", "SQL"],
        "courses": ["Web Development", "Database Management"],
        "personality": "Tech Enthusiast",
        "match": 85,
        "resume_url": "resume3.pdf"
    }
]

def recalculate_skills():
    """Recalculate skills based on current courses"""
    new_skills = []
    for course in st.session_state.courses:
        if course in COURSE_SKILL_MAP:
            new_skills.extend(COURSE_SKILL_MAP[course])
    st.session_state.skills = list(set(new_skills))

def get_recommended_internships():
    """Get internships matching student's skills"""
    if not st.session_state.skills:
        return SAMPLE_INTERNSHIPS
    
    recommendations = []
    for internship in SAMPLE_INTERNSHIPS:
        matched_skills = set(internship['required_skills']) & set(st.session_state.skills)
        if matched_skills:
            recommendations.append(internship)
    
    return recommendations if recommendations else SAMPLE_INTERNSHIPS

def theme_toggle():
    """Theme toggle button"""
    col1, col2 = st.columns([6, 1])
    with col2:
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(theme_icon, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

def landing_page():
    theme_toggle()
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
    theme_toggle()
    st.markdown('<h1 class="main-header">🔐 Login</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"### Login as {st.session_state.user_type.title()}")
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("Login", use_container_width=True):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_data = {
                        "email": email,
                        "name": email.split("@")[0].title(),
                        "phone": "",
                        "dob": None,
                        "linkedin": "",
                        "photo": None
                    }
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials")
        
        with col_b:
            if st.button("Back", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()

def signup_page():
    theme_toggle()
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
                    st.session_state.user_data = {
                        "email": email,
                        "name": name,
                        "phone": "",
                        "dob": None,
                        "linkedin": "",
                        "photo": None
                    }
                    st.success("Registration successful!")
                    st.rerun()
                else:
                    st.error("Please fill all fields and ensure passwords match")
        
        with col_b:
            if st.button("Back", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()

def student_dashboard():
    theme_toggle()
    st.markdown(f'<h1 class="main-header">👋 Welcome, {st.session_state.user_data.get("name", "Student")}!</h1>', unsafe_allow_html=True)
    
    # Sidebar toggle button
    if st.button("☰ Toggle Navigation" if st.session_state.sidebar_visible else "☰ Show Navigation"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()
    
    # Sidebar navigation
    if st.session_state.sidebar_visible:
        with st.sidebar:
            st.markdown("### 📚 Navigation")
            page = st.radio("Go to:", [
                "Dashboard",
                "Add Courses",
                "Psychometric Test",
                "Browse Internships",
                "Skill Gap Analysis",
                "Resume Builder",
                "Personal Settings"
            ])
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.page = "landing"
                st.rerun()
    else:
        page = "Dashboard"
    
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
    elif page == "Personal Settings":
        show_personal_settings()

def show_student_dashboard_home():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Courses Completed</div>
            <div class="metric-value">{len(st.session_state.courses)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Skills Identified</div>
            <div class="metric-value">{len(st.session_state.skills)}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        recommended = len(get_recommended_internships())
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Recommended Internships</div>
            <div class="metric-value">{recommended}</div>
        </div>
        ''', unsafe_allow_html=True)
    
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
    
    st.markdown("---")
    st.markdown("### 🌟 Top Recommended Internships")
    
    recommended_internships = get_recommended_internships()
    for internship in recommended_internships[:3]:
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
                recalculate_skills()
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
                    recalculate_skills()
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location_filter = st.multiselect("Location", ["Bangalore", "Mumbai", "Delhi", "Remote"])
    
    with col2:
        type_filter = st.multiselect("Type", ["Remote", "On-site", "Hybrid"])
    
    with col3:
        skill_filter = st.multiselect("Skills", list(set([s for skills in COURSE_SKILL_MAP.values() for s in skills])))
    
    st.markdown("---")
    
    filtered_internships = get_recommended_internships()
    
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
        if st.button("Apply on LinkedIn", key=f"apply_{internship['id']}", use_container_width=True):
            st.success("Redirecting to LinkedIn...")
        
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
    
    st.markdown("Select an internship to compare your skills:")
    
    internship_options = {f"{i['title']} - {i['company']}": i for i in SAMPLE_INTERNSHIPS}
    selected_internship_name = st.selectbox("Choose Internship", list(internship_options.keys()))
    selected_internship = internship_options[selected_internship_name]
    
    st.markdown("---")
    
    st.markdown(f"### Analysis for: {selected_internship['title']}")
    
    your_skills = set(st.session_state.skills)
    required_skills = set(selected_internship['required_skills'])
    
    matched_skills = your_skills & required_skills
    missing_skills = required_skills - your_skills
    extra_skills = your_skills - required_skills
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Matched Skills</div>
            <div class="metric-value" style="color: #4caf50;">{len(matched_skills)}</div>
        </div>
        ''', unsafe_allow_html=True)
        if matched_skills:
            for skill in matched_skills:
                st.markdown(f"✅ {skill}")
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Skills to Learn</div>
            <div class="metric-value" style="color: #ff9800;">{len(missing_skills)}</div>
        </div>
        ''', unsafe_allow_html=True)
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"⚠️ {skill}")
        else:
            st.success("You have all required skills!")
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Additional Skills</div>
            <div class="metric-value" style="color: #2196f3;">{len(extra_skills)}</div>
        </div>
        ''', unsafe_allow_html=True)
        if extra_skills:
            for skill in extra_skills:
                st.markdown(f"➕ {skill}")
    
    match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0
    st.markdown(f"### Overall Match: {match_percentage:.0f}%")
    st.progress(match_percentage / 100)
    
    if missing_skills:
        st.markdown("---")
        st.markdown("### 📚 Recommended Learning Resources")
        
        learning_map = {
            "Python": "Python for Beginners - Coursera",
            "JavaScript": "JavaScript Essentials - Udemy",
            "React": "React Complete Guide - freeCodeCamp",
            "Machine Learning": "ML Specialization - Coursera",
            "SQL": "SQL Masterclass - DataCamp",
            "SEO": "SEO Fundamentals - Moz Academy",
            "Content Writing": "Content Writing Masterclass - Udemy",
            "Social Media": "Social Media Marketing - HubSpot",
            "Analytics": "Google Analytics Course - Google",
            "HR Management": "HR Management Basics - Coursera"
        }
        
        for skill in missing_skills:
            resource = learning_map.get(skill, f"{skill} Tutorial - Online")
            st.info(f"🎓 **{skill}**: {resource}")

def show_resume_builder():
    st.markdown("### 📄 Resume Builder")
    
    st.markdown("Create a professional, role-specific resume based on your profile.")
    
    resume_type = st.selectbox("Select Resume Type", [
        "Technical Position (Software, Data Science)",
        "Managerial Position (PM, Operations)",
        "Creative Position (Design, Marketing)",
        "HR/Communication Position"
    ])
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Personal Information")
        resume_name = st.text_input("Full Name", value=st.session_state.user_data.get("name", ""))
        resume_email = st.text_input("Email", value=st.session_state.user_data.get("email", ""))
        resume_phone = st.text_input("Phone Number", value=st.session_state.user_data.get("phone", ""))
        resume_linkedin = st.text_input("LinkedIn Profile", value=st.session_state.user_data.get("linkedin", ""))
    
    with col2:
        st.markdown("#### Resume Preview")
        st.info("Your resume will highlight skills relevant to the selected position type")
    
    st.markdown("---")
    
    st.markdown("#### Education Details")
    
    col1, col2 = st.columns(2)
    with col1:
        edu_degree = st.text_input("Degree (e.g., B.Tech in Computer Science)")
        edu_college = st.text_input("College/University")
    
    with col2:
        edu_year = st.text_input("Year of Completion (e.g., 2024)")
        edu_marks = st.text_input("Marks/CGPA (e.g., 8.5/10)")
    
    if st.button("➕ Add Education", key="add_edu"):
        if edu_degree and edu_college:
            st.session_state.education.append({
                "degree": edu_degree,
                "college": edu_college,
                "year": edu_year,
                "marks": edu_marks
            })
            st.success("Education added!")
            st.rerun()
    
    if st.session_state.education:
        st.markdown("#### Your Education")
        for i, edu in enumerate(st.session_state.education):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{edu['degree']}** - {edu['college']}")
                st.markdown(f"Year: {edu['year']} | Marks: {edu['marks']}")
            with col2:
                if st.button("🗑️", key=f"del_edu_{i}"):
                    st.session_state.education.pop(i)
                    st.rerun()
    
    st.markdown("---")
    
    st.markdown("#### Projects")
    
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name")
        project_desc = st.text_area("Project Description", height=100)
    
    with col2:
        project_tags = st.multiselect("Project Tags", [
            "Technical",
            "Social",
            "Art",
            "Management",
            "Research",
            "Creative"
        ])
        project_skills = st.multiselect("Skills Used", st.session_state.skills)
    
    if st.button("➕ Add Project", key="add_project"):
        if project_name and project_desc:
            st.session_state.projects.append({
                "name": project_name,
                "description": project_desc,
                "tags": project_tags,
                "skills": project_skills
            })
            st.success("Project added!")
            st.rerun()
    
    if st.session_state.projects:
        st.markdown("#### Your Projects")
        for i, proj in enumerate(st.session_state.projects):
            with st.expander(f"{proj['name']}"):
                st.markdown(f"**Description:** {proj['description']}")
                if proj['tags']:
                    tags_html = "".join([f'<span class="skill-badge">{tag}</span>' for tag in proj['tags']])
                    st.markdown(f"**Tags:** {tags_html}", unsafe_allow_html=True)
                if proj['skills']:
                    skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in proj['skills']])
                    st.markdown(f"**Skills:** {skills_html}", unsafe_allow_html=True)
                if st.button("🗑️ Remove", key=f"del_proj_{i}"):
                    st.session_state.projects.pop(i)
                    st.rerun()
    
    st.markdown("---")
    
    st.markdown("#### Professional Summary")
    summary = st.text_area(
        "Write a brief summary (will be customized based on resume type)",
        value=f"Motivated student with skills in {', '.join(st.session_state.skills[:3])} seeking opportunities.",
        height=100
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Generate PDF", use_container_width=True):
            st.success(f"Resume generated for {resume_type}! (In production, this would download a PDF)")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("Resume draft saved!")
    
    with col3:
        if st.button("👁️ Preview", use_container_width=True):
            show_resume_preview(resume_name, resume_email, resume_phone, resume_linkedin, 
                              resume_type, summary)

def show_resume_preview(name, email, phone, linkedin, resume_type, summary):
    """Show resume preview in a modal-like expander"""
    with st.expander("📄 Resume Preview", expanded=True):
        st.markdown(f"### {name}")
        st.markdown(f"📧 {email} | 📱 {phone} | 🔗 {linkedin}")
        st.markdown("---")
        
        st.markdown("#### Professional Summary")
        st.markdown(summary)
        st.markdown("---")
        
        if st.session_state.education:
            st.markdown("#### Education")
            for edu in st.session_state.education:
                st.markdown(f"**{edu['degree']}**")
                st.markdown(f"{edu['college']} | {edu['year']} | CGPA: {edu['marks']}")
            st.markdown("---")
        
        st.markdown("#### Skills")
        # Filter skills based on resume type
        if "Technical" in resume_type:
            relevant_skills = [s for s in st.session_state.skills if s in ["Python", "JavaScript", "SQL", "React", "Machine Learning"]]
        elif "Creative" in resume_type:
            relevant_skills = [s for s in st.session_state.skills if s in ["SEO", "Content Writing", "Social Media", "Analytics"]]
        elif "HR" in resume_type:
            relevant_skills = [s for s in st.session_state.skills if s in ["Communication", "HR Management", "Recruitment"]]
        else:
            relevant_skills = st.session_state.skills
        
        skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in relevant_skills])
        st.markdown(skills_html, unsafe_allow_html=True)
        st.markdown("---")
        
        if st.session_state.projects:
            st.markdown("#### Projects")
            # Filter projects based on resume type
            for proj in st.session_state.projects:
                if "Technical" in resume_type and "Technical" in proj['tags']:
                    st.markdown(f"**{proj['name']}**")
                    st.markdown(proj['description'])
                    st.markdown("")
                elif "Creative" in resume_type and ("Creative" in proj['tags'] or "Art" in proj['tags']):
                    st.markdown(f"**{proj['name']}**")
                    st.markdown(proj['description'])
                    st.markdown("")
                elif "Managerial" in resume_type and "Management" in proj['tags']:
                    st.markdown(f"**{proj['name']}**")
                    st.markdown(proj['description'])
                    st.markdown("")

def show_personal_settings():
    st.markdown("### ⚙️ Personal Settings")
    st.markdown("Manage your personal information and account settings")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Basic Information")
        new_name = st.text_input("Full Name", value=st.session_state.user_data.get("name", ""))
        new_email = st.text_input("Email", value=st.session_state.user_data.get("email", ""))
        new_phone = st.text_input("Contact Number", value=st.session_state.user_data.get("phone", ""))
        new_dob = st.date_input("Date of Birth", value=st.session_state.user_data.get("dob"))
    
    with col2:
        st.markdown("#### Professional Information")
        new_linkedin = st.text_input("LinkedIn Profile", value=st.session_state.user_data.get("linkedin", ""))
        new_photo = st.file_uploader("Upload Photograph", type=["jpg", "png", "jpeg"])
        resume_pdf = st.file_uploader("Upload Resume PDF", type=["pdf"])
    
    st.markdown("---")
    
    st.markdown("#### Change Password")
    col1, col2 = st.columns(2)
    with col1:
        old_password = st.text_input("Current Password", type="password")
    with col2:
        new_password = st.text_input("New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Changes", use_container_width=True):
            st.session_state.user_data["name"] = new_name
            st.session_state.user_data["email"] = new_email
            st.session_state.user_data["phone"] = new_phone
            st.session_state.user_data["dob"] = new_dob
            st.session_state.user_data["linkedin"] = new_linkedin
            if new_photo:
                st.session_state.user_data["photo"] = new_photo
            st.success("✅ Settings saved successfully!")
    
    with col2:
        if st.button("🔑 Update Password", use_container_width=True):
            if new_password == confirm_new_password and old_password:
                st.success("✅ Password updated successfully!")
            else:
                st.error("❌ Passwords don't match or current password is incorrect")
    
    with col3:
        if st.button("🗑️ Delete Account", use_container_width=True):
            st.warning("⚠️ This action cannot be undone!")

def recruiter_dashboard():
    theme_toggle()
    st.markdown(f'<h1 class="main-header">👔 Recruiter Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f"### Welcome, {st.session_state.user_data.get('name', 'Recruiter')}!")
    
    # Sidebar toggle button
    if st.button("☰ Toggle Navigation" if st.session_state.sidebar_visible else "☰ Show Navigation"):
        st.session_state.sidebar_visible = not st.session_state.sidebar_visible
        st.rerun()
    
    if st.session_state.sidebar_visible:
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
    else:
        page = "Dashboard"
    
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
        st.markdown('''
        <div class="metric-card">
            <div class="metric-label">Posted Internships</div>
            <div class="metric-value">5</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-label">Total Applications</div>
            <div class="metric-value">47</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-label">Matched Candidates</div>
            <div class="metric-value">23</div>
        </div>
        ''', unsafe_allow_html=True)
    
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
        
        for candidate in SAMPLE_CANDIDATES:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"#### {candidate['name']}")
                st.markdown(f"📧 {candidate['email']}")
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate['skills']])
                st.markdown(skills_html, unsafe_allow_html=True)
                st.markdown(f"**Personality:** {candidate['personality']}")
            
            with col2:
                st.metric("Match Score", f"{candidate['match']}%")
            
            with col3:
                if st.button("👁️ View Profile", key=f"view_{candidate['id']}", use_container_width=True):
                    show_candidate_profile(candidate)
            
            st.markdown("---")

def show_candidate_profile(candidate):
    """Display candidate profile in an expander"""
    with st.expander(f"📋 Profile: {candidate['name']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Personal Information")
            st.markdown(f"**Name:** {candidate['name']}")
            st.markdown(f"**Email:** {candidate['email']}")
            st.markdown(f"**Personality Type:** {candidate['personality']}")
        
        with col2:
            st.markdown("#### Academic Background")
            st.markdown("**Courses Completed:**")
            for course in candidate['courses']:
                st.markdown(f"- {course}")
        
        st.markdown("---")
        st.markdown("#### Skills")
        skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate['skills']])
        st.markdown(skills_html, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Resume", key=f"download_{candidate['id']}", use_container_width=True):
                st.success("Resume downloaded!")
        with col2:
            if st.button("📧 Contact Candidate", key=f"contact_{candidate['id']}", use_container_width=True):
                st.success("Email sent to candidate!")

def show_manage_applications():
    st.markdown("### 📋 Manage Applications")
    
    tabs = st.tabs(["New Applications", "Shortlisted", "Rejected"])
    
    with tabs[0]:
        st.markdown("#### 🆕 New Applications (12)")
        
        for i, candidate in enumerate(SAMPLE_CANDIDATES):
            candidate_id = f"new_{candidate['id']}"
            status = st.session_state.application_status.get(candidate_id, "pending")
            
            if status == "pending":
                st.markdown('<div class="candidate-card">', unsafe_allow_html=True)
            else:
                st.markdown('<div class="candidate-card greyed">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{candidate['name']}** - Software Development Intern")
                st.markdown("Applied 2 days ago")
                skills_html = "".join([f'<span class="skill-badge">{skill}</span>' for skill in candidate['skills'][:3]])
                st.markdown(skills_html, unsafe_allow_html=True)
            
            if status == "pending":
                with col2:
                    if st.button("👁️ View", key=f"view_app_{candidate_id}", use_container_width=True):
                        show_candidate_profile(candidate)
                
                with col3:
                    if st.button("✅ Shortlist", key=f"short_{candidate_id}", use_container_width=True):
                        st.session_state.application_status[candidate_id] = "shortlisted"
                        st.rerun()
                
                with col4:
                    if st.button("❌ Reject", key=f"reject_{candidate_id}", use_container_width=True):
                        st.session_state.application_status[candidate_id] = "rejected"
                        st.rerun()
            else:
                with col2:
                    st.markdown("")
                with col3:
                    if status == "shortlisted":
                        st.markdown('<div class="status-message">✅ Added to shortlist</div>', unsafe_allow_html=True)
                    elif status == "rejected":
                        st.markdown('<div class="status-message">❌ Rejected for now</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")
    
    with tabs[1]:
        st.markdown("#### ⭐ Shortlisted Candidates")
        
        shortlisted = [k for k, v in st.session_state.application_status.items() if v == "shortlisted"]
        
        if shortlisted:
            st.markdown(f"**Total Shortlisted: {len(shortlisted)}**")
            
            for candidate in SAMPLE_CANDIDATES[:len(shortlisted)]:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{candidate['name']}**")
                    st.markdown(f"📧 {candidate['email']} | Match: {candidate['match']}%")
                with col2:
                    if st.button("📥 View CV", key=f"cv_short_{candidate['id']}", use_container_width=True):
                        st.success("Viewing CV...")
                st.markdown("---")
        else:
            st.info("No shortlisted candidates yet")
    
    with tabs[2]:
        st.markdown("#### 🚫 Rejected Applications")
        
        rejected = [k for k, v in st.session_state.application_status.items() if v == "rejected"]
        
        if rejected:
            st.markdown(f"**Total Rejected: {len(rejected)}**")
            st.info("Previously rejected applications are archived here")
        else:
            st.info("No rejected applications yet")

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
