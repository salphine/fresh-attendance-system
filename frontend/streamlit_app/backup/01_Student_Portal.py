import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# Page config
st.set_page_config(
    page_title="Salphine Chemos - Student Portal",
    page_icon="?????",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
    
    /* Student profile header */
    .profile-header {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border-left: 5px solid #667eea;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* Status badges */
    .badge-success {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .badge-info {
        background: linear-gradient(135deg, #17a2b8 0%, #6c757d 100%);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Metric cards */
    .metric-small {
        background: white;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-bottom: 3px solid #667eea;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        color: #667eea;
        margin: 5px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #666;
        text-transform: uppercase;
    }
    
    /* Attendance progress */
    .progress-bar {
        background: #f0f0f0;
        border-radius: 10px;
        height: 10px;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        height: 10px;
        transition: width 1s ease;
    }
    
    /* Course list */
    .course-item {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s;
    }
    
    .course-item:hover {
        transform: translateX(5px);
        background: #e9ecef;
    }
    
    /* Camera container */
    .camera-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 2px dashed #667eea;
        margin: 20px 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "attendance_marked" not in st.session_state:
    st.session_state.attendance_marked = False
if "verification_score" not in st.session_state:
    st.session_state.verification_score = 0
if "current_time" not in st.session_state:
    st.session_state.current_time = datetime.now()
if "selected_semester" not in st.session_state:
    st.session_state.selected_semester = "Semester 2, 2026"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# Student Information
STUDENT_NAME = "Salphine Chemos"
STUDENT_ID = "BBIT-2022-0045"
STUDENT_EMAIL = "salphine.chemos@students.embu.ac.ke"
STUDENT_PROGRAM = "Bachelor of Business Information Technology (BBIT)"
STUDENT_YEAR = "4th Year"
STUDENT_SEMESTER = "Semester 2"
STUDENT_REG_DATE = "September 2022"
STUDENT_PROFILE_PIC = "https://ui-avatars.com/api/?name=Salphine+Chemos&size=150&background=667eea&color=fff&bold=true"

# Sample course data
courses = [
    {"code": "BBIT 401", "name": "Enterprise Systems", "lecturer": "Dr. Omondi", "attendance": 92, "total_classes": 28, "attended": 26, "schedule": "Mon 9-11 AM", "room": "Lab 301"},
    {"code": "BBIT 402", "name": "IT Project Management", "lecturer": "Prof. Kamau", "attendance": 88, "total_classes": 25, "attended": 22, "schedule": "Tue 2-4 PM", "room": "Hall A"},
    {"code": "BBIT 403", "name": "Data Science & Analytics", "lecturer": "Dr. Mwangi", "attendance": 95, "total_classes": 22, "attended": 21, "schedule": "Wed 10-12 AM", "room": "Comp Lab"},
    {"code": "BBIT 404", "name": "Cybersecurity", "lecturer": "Dr. Akinyi", "attendance": 85, "total_classes": 20, "attended": 17, "schedule": "Thu 1-3 PM", "room": "Lab 205"},
    {"code": "BBIT 405", "name": "Mobile Development", "lecturer": "Mr. Otieno", "attendance": 90, "total_classes": 24, "attended": 22, "schedule": "Fri 9-11 AM", "room": "Lab 302"},
]

# Sidebar Navigation
with st.sidebar:
    st.markdown("### ????? Student Portal")
    st.markdown("---")
    
    # Student profile summary
    st.markdown(f"""
    <div style="text-align: center; padding: 15px;">
        <img src="{STUDENT_PROFILE_PIC}" style="border-radius: 50%; margin-bottom: 10px; border: 3px solid white;">
        <h3 style="color: white; margin: 5px 0;">{STUDENT_NAME}</h3>
        <p style="color: #e0e0e0; font-size: 0.9em;">{STUDENT_ID}</p>
        <p style="color: #e0e0e0; font-size: 0.9em;">{STUDENT_YEAR} • {STUDENT_SEMESTER}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation options
    nav_options = {
        "Dashboard": "??",
        "Mark Attendance": "??",
        "My Courses": "??",
        "Attendance History": "??",
        "Timetable": "?",
        "Profile": "??",
        "Settings": "??"
    }
    
    for option, icon in nav_options.items():
        if st.button(f"{icon} {option}", key=f"nav_{option}", width='stretch'):
            st.session_state.active_tab = option
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### ?? Quick Stats")
    overall_attendance = int(np.mean([c["attendance"] for c in courses]))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-small">
            <div class="metric-label">Attendance</div>
            <div class="metric-value">{overall_attendance}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-small">
            <div class="metric-label">Courses</div>
            <div class="metric-value">{len(courses)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Current time
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: white; padding: 10px;">
        <p style="font-size: 1.2em;">{datetime.now().strftime('%H:%M:%S')}</p>
        <p style="font-size: 0.9em;">{datetime.now().strftime('%A, %d %B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
st.markdown(f"""
<div class="profile-header">
    <div style="display: flex; align-items: center; gap: 20px;">
        <img src="{STUDENT_PROFILE_PIC}" style="width: 80px; border-radius: 50%; border: 3px solid #667eea;">
        <div>
            <h1 style="color: #333; margin: 0;">{STUDENT_NAME}</h1>
            <p style="color: #666; margin: 5px 0;">{STUDENT_ID} • {STUDENT_PROGRAM}</p>
            <p style="color: #666; margin: 5px 0;">{STUDENT_EMAIL}</p>
        </div>
        <div style="margin-left: auto;">
            <span class="badge-success">?? Active</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# DASHBOARD TAB
if st.session_state.active_tab == "Dashboard":
    st.markdown("## ?? Dashboard Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4 style="color: #666;">Overall Attendance</h4>
            <h1 style="color: #667eea; font-size: 3em;">92%</h1>
            <p style="color: #28a745;">? 3% from last semester</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4 style="color: #666;">Classes Attended</h4>
            <h1 style="color: #667eea; font-size: 3em;">108</h1>
            <p style="color: #666;">out of 119 total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4 style="color: #666;">Current GPA</h4>
            <h1 style="color: #667eea; font-size: 3em;">4.2</h1>
            <p style="color: #28a745;">? 0.3</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h4 style="color: #666;">Days Until Finals</h4>
            <h1 style="color: #667eea; font-size: 3em;">24</h1>
            <p style="color: #ffc107;">Prepare well!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("?? Attendance by Course")
        
        # Create bar chart
        course_names = [c["code"] for c in courses]
        attendance_values = [c["attendance"] for c in courses]
        
        fig = px.bar(
            x=course_names,
            y=attendance_values,
            color=attendance_values,
            color_continuous_scale=['#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1', '#5f27cd'],
            labels={'x': 'Course', 'y': 'Attendance %'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("?? Weekly Attendance Trend")
        
        # Generate weekly data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        weekly_attendance = [random.randint(85, 98) for _ in range(5)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=days,
            y=weekly_attendance,
            mode='lines+markers',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            showlegend=False,
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Today's schedule
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("?? Today's Schedule")
    
    today = datetime.now().strftime('%A')
    today_schedule = [c for c in courses if today[:3] in c["schedule"]]
    
    if today_schedule:
        for course in today_schedule:
            st.markdown(f"""
            <div class="course-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0;">{course['code']} - {course['name']}</h4>
                        <p style="margin: 5px 0; color: #666;">{course['lecturer']} • {course['room']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-weight: 600; color: #667eea;">{course['schedule']}</p>
                        <span class="badge-info">Upcoming</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No classes scheduled for today")
    st.markdown('</div>', unsafe_allow_html=True)

# MARK ATTENDANCE TAB
elif st.session_state.active_tab == "Mark Attendance":
    st.markdown("## ?? Mark Attendance")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="camera-container">', unsafe_allow_html=True)
        st.markdown("#### ?? Face Recognition Camera")
        
        # Camera input
        img_file = st.camera_input("Position your face clearly")
        
        if img_file is not None and not st.session_state.attendance_marked:
            with st.spinner("Verifying identity..."):
                time.sleep(2)
                # Simulate face verification
                st.session_state.verification_score = random.randint(85, 99)
                st.session_state.attendance_marked = True
                st.balloons()
        
        if st.session_state.attendance_marked:
            st.success(f"? Verified! Confidence: {st.session_state.verification_score}%")
            
            if st.button("Mark Another Class", width='stretch'):
                st.session_state.attendance_marked = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown("""
        <div class="card">
            <h4>?? Instructions:</h4>
            <ol style="color: #666;">
                <li>Position your face clearly in the camera</li>
                <li>Ensure good lighting</li>
                <li>Remove glasses if possible</li>
                <li>Wait for verification (2-3 seconds)</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("?? Today's Classes")
        
        today = datetime.now().strftime('%A')
        today_courses = [c for c in courses if today[:3] in c["schedule"]]
        
        for course in today_courses:
            status = "? Completed" if course["attended"] > 20 else "? Pending"
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4 style="margin: 0;">{course['code']}</h4>
                <p style="margin: 5px 0;">{course['name']}</p>
                <p style="margin: 5px 0;">? {course['schedule']}</p>
                <p style="margin: 5px 0;">?? {course['room']}</p>
                <p style="margin: 5px 0;">Status: {status}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Liveness score gauge
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("?? Liveness Score")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=st.session_state.verification_score if st.session_state.verification_score > 0 else 95,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 50], 'color': "#ff6b6b"},
                    {'range': [50, 75], 'color': "#feca57"},
                    {'range': [75, 100], 'color': "#1dd1a1"}
                ]
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

# MY COURSES TAB
elif st.session_state.active_tab == "My Courses":
    st.markdown("## ?? My Courses - 4th Year BBIT")
    
    # Semester selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        semester = st.selectbox("Select Semester", ["Semester 2, 2026", "Semester 1, 2026", "Semester 2, 2025"])
    with col2:
        st.markdown(f"<br><span class='badge-success'>GPA: 4.2</span>", unsafe_allow_html=True)
    
    # Display courses in a grid
    for i in range(0, len(courses), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(courses):
                course = courses[i + j]
                with cols[j]:
                    progress = (course["attended"] / course["total_classes"]) * 100
                    st.markdown(f"""
                    <div class="card">
                        <h3>{course['code']}</h3>
                        <h4>{course['name']}</h4>
                        <p style="color: #666;">????? {course['lecturer']}</p>
                        <p style="color: #666;">?? {course['schedule']}</p>
                        <p style="color: #666;">?? {course['room']}</p>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {progress}%;"></div>
                        </div>
                        <p style="text-align: right;">Attendance: {course['attended']}/{course['total_classes']} ({course['attendance']}%)</p>
                    </div>
                    """, unsafe_allow_html=True)

# ATTENDANCE HISTORY TAB
elif st.session_state.active_tab == "Attendance History":
    st.markdown("## ?? Attendance History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_course = st.selectbox("Filter by Course", ["All"] + [c["code"] for c in courses])
    with col2:
        filter_month = st.selectbox("Filter by Month", ["All", "January", "February", "March", "April", "May", "June"])
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "Present", "Absent", "Late"])
    
    # Generate sample attendance data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    attendance_data = []
    for date in dates:
        for course in courses[:3]:  # Show last 3 courses
            status = np.random.choice(['Present', 'Present', 'Present', 'Present', 'Absent', 'Late'], p=[0.6, 0.2, 0.1, 0.05, 0.03, 0.02])
            attendance_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Course': course['code'],
                'Course Name': course['name'],
                'Status': status,
                'Time': f"{np.random.randint(8, 11)}:{np.random.randint(10, 59)} AM",
                'Confidence': f"{np.random.randint(85, 99)}%"
            })
    
    df = pd.DataFrame(attendance_data)
    
    # Apply filters
    if filter_course != "All":
        df = df[df['Course'] == filter_course]
    if filter_status != "All":
        df = df[df['Status'] == filter_status]
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Classes", len(df))
    with col2:
        present = len(df[df['Status'] == 'Present'])
        st.metric("Present", present, f"{(present/len(df)*100):.1f}%" if len(df) > 0 else "0%")
    with col3:
        absent = len(df[df['Status'] == 'Absent'])
        st.metric("Absent", absent)
    with col4:
        late = len(df[df['Status'] == 'Late'])
        st.metric("Late", late)
    
    # Display table
    st.dataframe(df, width='stretch', hide_index=True)
    
    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="?? Download Attendance Report",
        data=csv,
        file_name=f"attendance_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# TIMETABLE TAB
elif st.session_state.active_tab == "Timetable":
    st.markdown("## ? Weekly Timetable - BBIT 4th Year")
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Create timetable grid
    for day in days:
        with st.expander(f"?? {day}", expanded=True):
            day_courses = [c for c in courses if day[:3] in c["schedule"]]
            if day_courses:
                for course in day_courses:
                    st.markdown(f"""
                    <div class="course-item">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <h4>{course['code']} - {course['name']}</h4>
                                <p>????? {course['lecturer']} • ?? {course['room']}</p>
                            </div>
                            <div style="text-align: right;">
                                <h4 style="color: #667eea;">{course['schedule']}</h4>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No classes scheduled for {day}")

# PROFILE TAB
elif st.session_state.active_tab == "Profile":
    st.markdown("## ?? Student Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <img src="{STUDENT_PROFILE_PIC}" style="width: 150px; border-radius: 50%; margin: 20px auto;">
            <h2>{STUDENT_NAME}</h2>
            <p style="color: #666;">{STUDENT_ID}</p>
            <span class="badge-success">Active Student</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("?? Personal Information")
        
        info_data = {
            "Full Name": STUDENT_NAME,
            "Student ID": STUDENT_ID,
            "Email": STUDENT_EMAIL,
            "Program": STUDENT_PROGRAM,
            "Year of Study": STUDENT_YEAR,
            "Current Semester": STUDENT_SEMESTER,
            "Registration Date": STUDENT_REG_DATE,
            "Supervisor": "Dr. Omondi - Department of IT"
        }
        
        for key, value in info_data.items():
            st.markdown(f"""
            <div style="display: flex; padding: 8px 0; border-bottom: 1px solid #eee;">
                <div style="width: 150px; font-weight: 600;">{key}:</div>
                <div>{value}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# SETTINGS TAB
elif st.session_state.active_tab == "Settings":
    st.markdown("## ?? Settings")
    
    tabs = st.tabs(["Account", "Notifications", "Privacy", "Appearance"])
    
    with tabs[0]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Account Settings")
        st.checkbox("Enable Two-Factor Authentication", value=True)
        st.checkbox("Remember Me on this device", value=True)
        st.button("Change Password", width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Notification Preferences")
        st.checkbox("Email notifications for attendance", value=True)
        st.checkbox("SMS alerts for low attendance", value=False)
        st.checkbox("Push notifications for class reminders", value=True)
        st.select_slider("Notification frequency", options=["Daily", "Weekly", "Monthly"], value="Weekly")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Privacy Settings")
        st.checkbox("Share attendance data with lecturers", value=True)
        st.checkbox("Make profile visible to classmates", value=True)
        st.checkbox("Allow face data storage", value=True)
        st.info("Your face data is encrypted and stored securely")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Appearance")
        st.selectbox("Theme", ["Light", "Dark", "System Default"])
        st.selectbox("Language", ["English", "Swahili", "French"])
        st.slider("Font Size", 12, 24, 16)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Save All Settings", width='stretch'):
        st.success("Settings saved successfully!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("© 2026 University of Embu")
with col2:
    st.caption(f"Student ID: {STUDENT_ID}")
with col3:
    st.caption(f"Last Login: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
