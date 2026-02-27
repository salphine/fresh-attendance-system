import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import calendar

# Page config
st.set_page_config(
    page_title="Dr. Isaiah - Lecturer Portal",
    page_icon="?????",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional gradient background */
    .stApp {
        background: linear-gradient(145deg, #1a2639 0%, #2c3e50 100%);
    }
    
    /* Lecturer header */
    .lecturer-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        color: white;
        animation: slideDown 0.5s ease;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Card styling */
    .prof-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .prof-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    /* Metric cards */
    .metric-prof {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .metric-prof h3 {
        font-size: 2.5em;
        margin: 10px 0;
        font-weight: 700;
    }
    
    /* Course cards */
    .course-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 10px 0;
        transition: transform 0.2s;
    }
    
    .course-card:hover {
        transform: translateX(5px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Status badges */
    .badge-primary {
        background: #667eea;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    .badge-success {
        background: #10b981;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    .badge-warning {
        background: #f59e0b;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    .badge-danger {
        background: #ef4444;
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    /* Table styling */
    .data-table {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
    }
    
    /* Progress bar */
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        height: 8px;
        margin: 10px 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        height: 8px;
        transition: width 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
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
if "selected_semester" not in st.session_state:
    st.session_state.selected_semester = "Semester 2, 2026"
if "selected_course" not in st.session_state:
    st.session_state.selected_course = "All Courses"
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"
if "date_range" not in st.session_state:
    st.session_state.date_range = "This Week"

# Lecturer Information
LECTURER_NAME = "Dr. Isaiah"
LECTURER_TITLE = "Senior Lecturer - Department of Information Technology"
LECTURER_ID = "LEC-2015-0078"
LECTURER_EMAIL = "drisaiah@embu.ac.ke"
LECTURER_OFFICE = "Room 305, IT Building"
LECTURER_PHONE = "+254 712 345 678"
LECTURER_PROFILE_PIC = "https://ui-avatars.com/api/?name=Dr+Isaiah&size=150&background=2c3e50&color=fff&bold=true"

# Course data
courses = [
    {
        "code": "BBIT 401",
        "name": "Enterprise Systems",
        "students": 45,
        "schedule": "Mon 9-11 AM",
        "room": "Lab 301",
        "attendance_rate": 87,
        "total_classes": 28,
        "completed": 22,
        "assignments": 3,
        "department": "IT"
    },
    {
        "code": "BBIT 402",
        "name": "IT Project Management",
        "students": 38,
        "schedule": "Tue 2-4 PM",
        "room": "Hall A",
        "attendance_rate": 82,
        "total_classes": 25,
        "completed": 20,
        "assignments": 4,
        "department": "IT"
    },
    {
        "code": "BBIT 403",
        "name": "Data Science & Analytics",
        "students": 42,
        "schedule": "Wed 10-12 AM",
        "room": "Comp Lab",
        "attendance_rate": 91,
        "total_classes": 22,
        "completed": 18,
        "assignments": 2,
        "department": "IT"
    },
    {
        "code": "BBIT 404",
        "name": "Cybersecurity",
        "students": 35,
        "schedule": "Thu 1-3 PM",
        "room": "Lab 205",
        "attendance_rate": 79,
        "total_classes": 20,
        "completed": 15,
        "assignments": 3,
        "department": "IT"
    },
    {
        "code": "BBIT 405",
        "name": "Mobile Development",
        "students": 40,
        "schedule": "Fri 9-11 AM",
        "room": "Lab 302",
        "attendance_rate": 88,
        "total_classes": 24,
        "completed": 20,
        "assignments": 3,
        "department": "IT"
    }
]

# Generate student data for each course
def generate_students_for_course(course_code, num_students):
    students = []
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", 
                   "David", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
                   "Daniel", "Lisa", "Matthew", "Margaret", "Anthony", "Betty", "Mark", "Sandra", "Donald", "Ashley"]
    last_names = ["Kimani", "Odhiambo", "Mwangi", "Akinyi", "Kipchoge", "Achieng", "Otieno", "Wanjiku", "Kiprop", "Chebet",
                  "Omondi", "Njeri", "Kemboi", "Atieno", "Kiprotich", "Jeruto", "Ochieng", "Wambui", "Kipyegon", "Jepchirchir"]
    
    for i in range(num_students):
        attendance = random.randint(65, 100)
        students.append({
            "id": f"BBIT-2022-{1000 + i:04d}",
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "course": course_code,
            "attendance": attendance,
            "assignments_completed": random.randint(2, 4),
            "total_assignments": 4,
            "last_attendance": (datetime.now() - timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d'),
            "status": "Active" if attendance > 75 else "At Risk" if attendance > 60 else "Critical"
        })
    return sorted(students, key=lambda x: x["name"])

# Generate all students
all_students = []
for course in courses:
    all_students.extend(generate_students_for_course(course["code"], course["students"]))

# Sidebar Navigation
with st.sidebar:
    st.markdown("### ????? Lecturer Portal")
    st.markdown("---")
    
    # Lecturer profile summary
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <img src="{LECTURER_PROFILE_PIC}" style="width: 100px; border-radius: 50%; margin-bottom: 15px; border: 3px solid white;">
        <h3 style="color: white; margin: 5px 0;">{LECTURER_NAME}</h3>
        <p style="color: #e0e0e0; font-size: 0.9em;">{LECTURER_TITLE}</p>
        <p style="color: #e0e0e0; font-size: 0.9em;">{LECTURER_ID}</p>
        <span class="badge-primary">?? {len(courses)} Courses</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation options
    nav_options = {
        "Dashboard": "??",
        "Course Management": "??",
        "Attendance Monitor": "??",
        "Student Analytics": "??",
        "Grade Book": "??",
        "Schedule": "?",
        "Reports": "??",
        "Profile": "??",
        "Settings": "??"
    }
    
    for option, icon in nav_options.items():
        if st.button(f"{icon} {option}", key=f"nav_{option}", width='stretch'):
            st.session_state.active_tab = option
    
    st.markdown("---")
    
    # Quick filters
    st.markdown("### ?? Quick Filters")
    st.session_state.selected_semester = st.selectbox(
        "Semester",
        ["Semester 2, 2026", "Semester 1, 2026", "Semester 2, 2025"]
    )
    
    st.session_state.selected_course = st.selectbox(
        "Course",
        ["All Courses"] + [c["code"] for c in courses]
    )
    
    # Current time
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: white; padding: 10px;">
        <p style="font-size: 1.2em;">{datetime.now().strftime('%H:%M:%S')}</p>
        <p style="font-size: 0.9em;">{datetime.now().strftime('%A, %d %B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

# Main content - Header
st.markdown(f"""
<div class="lecturer-header">
    <div style="display: flex; align-items: center; gap: 20px;">
        <img src="{LECTURER_PROFILE_PIC}" style="width: 80px; border-radius: 50%; border: 3px solid white;">
        <div>
            <h1 style="margin: 0;">{LECTURER_NAME}</h1>
            <p style="margin: 5px 0; opacity: 0.9;">{LECTURER_TITLE}</p>
            <p style="margin: 5px 0; opacity: 0.9;">{LECTURER_EMAIL} | {LECTURER_OFFICE}</p>
        </div>
        <div style="margin-left: auto;">
            <span class="badge-success">?? Online</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# DASHBOARD TAB
if st.session_state.active_tab == "Dashboard":
    st.markdown("## ?? Lecturer Dashboard")
    
    # Key metrics
    total_students = sum(c["students"] for c in courses)
    avg_attendance = int(np.mean([c["attendance_rate"] for c in courses]))
    total_classes = sum(c["completed"] for c in courses)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-prof">
            <p>Total Students</p>
            <h3>{total_students}</h3>
            <p style="font-size: 0.9em;">Across {len(courses)} courses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-prof">
            <p>Avg. Attendance</p>
            <h3>{avg_attendance}%</h3>
            <p style="font-size: 0.9em;">? 2.3% from last semester</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-prof">
            <p>Classes Completed</p>
            <h3>{total_classes}</h3>
            <p style="font-size: 0.9em;">out of 119 total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-prof">
            <p>Active Courses</p>
            <h3>{len(courses)}</h3>
            <p style="font-size: 0.9em;">This semester</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Attendance by Course")
        
        fig = px.bar(
            x=[c["code"] for c in courses],
            y=[c["attendance_rate"] for c in courses],
            color=[c["attendance_rate"] for c in courses],
            color_continuous_scale='viridis',
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
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Student Distribution")
        
        fig = px.pie(
            values=[c["students"] for c in courses],
            names=[c["code"] for c in courses],
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350
        )
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Today's schedule
    st.markdown('<div class="prof-card">', unsafe_allow_html=True)
    st.subheader("?? Today's Schedule")
    
    today = datetime.now().strftime('%A')
    today_courses = [c for c in courses if today[:3] in c["schedule"]]
    
    if today_courses:
        cols = st.columns(len(today_courses))
        for i, course in enumerate(today_courses):
            with cols[i]:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center;">
                    <h4>{course['code']}</h4>
                    <p>{course['name']}</p>
                    <p style="color: #667eea; font-weight: 600;">{course['schedule']}</p>
                    <p>?? {course['room']}</p>
                    <p>?? {course['students']} students</p>
                    <span class="badge-primary">Upcoming</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No classes scheduled for today")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<div class="prof-card">', unsafe_allow_html=True)
    st.subheader("?? Recent Activity")
    
    activities = [
        ("?? Grade submitted - BBIT 401", "2 hours ago"),
        ("? Attendance recorded - BBIT 403", "3 hours ago"),
        ("?? Report generated - Weekly Summary", "5 hours ago"),
        ("?? Announcement posted - BBIT 402", "1 day ago"),
        ("?? Assignment created - BBIT 405", "2 days ago")
    ]
    
    for activity, time in activities:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
            <span>{activity}</span>
            <span style="color: #666;">{time}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# COURSE MANAGEMENT TAB
elif st.session_state.active_tab == "Course Management":
    st.markdown("## ?? Course Management")
    
    # Filter courses
    if st.session_state.selected_course != "All Courses":
        filtered_courses = [c for c in courses if c["code"] == st.session_state.selected_course]
    else:
        filtered_courses = courses
    
    for course in filtered_courses:
        with st.expander(f"?? {course['code']} - {course['name']}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Students", course["students"])
            with col2:
                st.metric("Attendance Rate", f"{course['attendance_rate']}%")
            with col3:
                st.metric("Classes Completed", f"{course['completed']}/{course['total_classes']}")
            with col4:
                st.metric("Assignments", course["assignments"])
            
            # Course actions
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.button("?? Take Attendance", key=f"att_{course['code']}", width='stretch')
            with col2:
                st.button("?? View Analytics", key=f"ana_{course['code']}", width='stretch')
            with col3:
                st.button("?? Student List", key=f"list_{course['code']}", width='stretch')
            with col4:
                st.button("?? Upload Materials", key=f"mat_{course['code']}", width='stretch')
            with col5:
                st.button("?? Announce", key=f"ann_{course['code']}", width='stretch')
            
            # Quick stats
            st.markdown("#### ?? Quick Stats")
            col1, col2 = st.columns(2)
            
            with col1:
                # Weekly attendance trend
                days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
                weekly_data = [random.randint(70, 95) for _ in range(5)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=days,
                    y=weekly_data,
                    mode='lines+markers',
                    line=dict(color='#667eea', width=2)
                ))
                fig.update_layout(
                    title="Weekly Attendance Trend",
                    height=250,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                # Grade distribution
                grades = ['A', 'B', 'C', 'D', 'F']
                grade_counts = [random.randint(5, 15) for _ in range(5)]
                
                fig = px.pie(
                    values=grade_counts,
                    names=grades,
                    title="Grade Distribution",
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                fig.update_layout(height=250)
                st.plotly_chart(fig, width='stretch')

# ATTENDANCE MONITOR TAB
elif st.session_state.active_tab == "Attendance Monitor":
    st.markdown("## ?? Live Attendance Monitor")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_course = st.selectbox("Select Course", [c["code"] for c in courses])
    with col2:
        selected_date = st.date_input("Select Date", datetime.now())
    with col3:
        show_filter = st.selectbox("Show", ["All Students", "Present Only", "Absent Only"])
    
    # Get students for selected course
    course_students = [s for s in all_students if s["course"] == selected_course]
    
    # Generate attendance for selected date
    for student in course_students:
        student["present_today"] = random.choice([True, False]) if show_filter == "All Students" else (
            True if show_filter == "Present Only" else False
        )
    
    # Apply filter
    if show_filter == "Present Only":
        filtered_students = [s for s in course_students if s["present_today"]]
    elif show_filter == "Absent Only":
        filtered_students = [s for s in course_students if not s["present_today"]]
    else:
        filtered_students = course_students
    
    # Summary stats
    total = len(course_students)
    present = len([s for s in course_students if s.get("present_today", False)])
    absent = total - present
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", total)
    with col2:
        st.metric("Present", present, f"{(present/total*100):.1f}%" if total > 0 else "0%")
    with col3:
        st.metric("Absent", absent)
    with col4:
        st.metric("Attendance Rate", f"{(present/total*100):.1f}%" if total > 0 else "0%")
    
    # Attendance table
    st.markdown('<div class="data-table">', unsafe_allow_html=True)
    
    # Create DataFrame
    df_display = pd.DataFrame(filtered_students)
    if not df_display.empty:
        df_display = df_display[["id", "name", "attendance", "status", "last_attendance"]]
        df_display.columns = ["Student ID", "Name", "Overall %", "Status", "Last Attendance"]
        
        # Color code status
        def color_status(val):
            if val == "Active":
                return "background-color: #d4edda; color: #155724"
            elif val == "At Risk":
                return "background-color: #fff3cd; color: #856404"
            else:
                return "background-color: #f8d7da; color: #721c24"
        
        st.dataframe(
            df_display.style.applymap(color_status, subset=["Status"]),
            width='stretch',
            hide_index=True
        )
    else:
        st.info("No students match the selected filter")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("?? Download Attendance List", width='stretch'):
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="?? Click to Download",
                data=csv,
                file_name=f"attendance_{selected_course}_{selected_date}.csv",
                mime="text/csv"
            )
    with col2:
        st.button("?? Notify Absent Students", width='stretch')
    with col3:
        st.button("?? Generate Report", width='stretch')

# STUDENT ANALYTICS TAB
elif st.session_state.active_tab == "Student Analytics":
    st.markdown("## ?? Student Performance Analytics")
    
    # Course selector
    selected_course_analytics = st.selectbox(
        "Select Course for Detailed Analytics",
        ["All Courses"] + [c["code"] for c in courses]
    )
    
    if selected_course_analytics == "All Courses":
        analytics_students = all_students
    else:
        analytics_students = [s for s in all_students if s["course"] == selected_course_analytics]
    
    # Performance distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Attendance Distribution")
        
        attendance_ranges = ["90-100%", "75-89%", "60-74%", "Below 60%"]
        range_counts = [
            len([s for s in analytics_students if s["attendance"] >= 90]),
            len([s for s in analytics_students if 75 <= s["attendance"] < 90]),
            len([s for s in analytics_students if 60 <= s["attendance"] < 75]),
            len([s for s in analytics_students if s["attendance"] < 60])
        ]
        
        fig = px.bar(
            x=attendance_ranges,
            y=range_counts,
            color=range_counts,
            color_continuous_scale='viridis',
            labels={'x': 'Attendance Range', 'y': 'Number of Students'}
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Student Status Overview")
        
        status_counts = {
            "Active": len([s for s in analytics_students if s["status"] == "Active"]),
            "At Risk": len([s for s in analytics_students if s["status"] == "At Risk"]),
            "Critical": len([s for s in analytics_students if s["status"] == "Critical"])
        }
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444']
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Top and bottom performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Top Performers")
        
        top_students = sorted(analytics_students, key=lambda x: x["attendance"], reverse=True)[:5]
        for i, student in enumerate(top_students, 1):
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px; background: {'#f8f9fa' if i%2==0 else 'white'}; border-radius: 5px;">
                <span>{i}. {student['name']}</span>
                <span style="color: #10b981; font-weight: 600;">{student['attendance']}%</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Students Needing Attention")
        
        at_risk = [s for s in analytics_students if s["status"] in ["At Risk", "Critical"]]
        at_risk = sorted(at_risk, key=lambda x: x["attendance"])[:5]
        
        if at_risk:
            for i, student in enumerate(at_risk, 1):
                color = "#f59e0b" if student["status"] == "At Risk" else "#ef4444"
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 8px; background: {'#f8f9fa' if i%2==0 else 'white'}; border-radius: 5px;">
                    <span>{i}. {student['name']}</span>
                    <span style="color: {color}; font-weight: 600;">{student['attendance']}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No students at risk!")
        st.markdown('</div>', unsafe_allow_html=True)

# GRADE BOOK TAB
elif st.session_state.active_tab == "Grade Book":
    st.markdown("## ?? Grade Book")
    
    # Course selection
    grade_course = st.selectbox("Select Course", [c["code"] for c in courses])
    
    # Assignment types
    col1, col2 = st.columns([2, 1])
    with col1:
        assignment_type = st.selectbox("Assignment Type", ["Assignments", "Mid-Term Exam", "Final Exam", "Projects", "Total"])
    with col2:
        st.metric("Average Score", f"{random.randint(65, 85)}%")
    
    # Grade table
    course_students = [s for s in all_students if s["course"] == grade_course]
    
    grade_data = []
    for student in course_students:
        grade_data.append({
            "Student ID": student["id"],
            "Student Name": student["name"],
            "Assignment 1": random.randint(60, 100),
            "Assignment 2": random.randint(60, 100),
            "Assignment 3": random.randint(60, 100),
            "Mid-Term": random.randint(50, 100),
            "Project": random.randint(60, 100),
            "Final Exam": random.randint(50, 100),
            "Total": 0
        })
    
    # Calculate totals
    for g in grade_data:
        g["Total"] = int((g["Assignment 1"] + g["Assignment 2"] + g["Assignment 3"] + 
                          g["Mid-Term"] + g["Project"] + g["Final Exam"]) / 6)
    
    df_grades = pd.DataFrame(grade_data)
    st.dataframe(df_grades, width='stretch', hide_index=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("?? Export as CSV", width='stretch'):
            csv = df_grades.to_csv(index=False)
            st.download_button("Download CSV", csv, f"grades_{grade_course}.csv", "text/csv")
    with col2:
        st.button("?? Upload Grades", width='stretch')
    with col3:
        st.button("?? Publish to Students", width='stretch')

# SCHEDULE TAB
elif st.session_state.active_tab == "Schedule":
    st.markdown("## ? Weekly Schedule")
    
    # Week selector
    col1, col2 = st.columns(2)
    with col1:
        week = st.selectbox("Week", [f"Week {i}" for i in range(1, 15)])
    with col2:
        st.metric("Total Hours", "14 hours/week")
    
    # Schedule grid
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    for day in days:
        with st.expander(f"?? {day}", expanded=True):
            day_courses = [c for c in courses if day[:3] in c["schedule"]]
            if day_courses:
                for course in day_courses:
                    st.markdown(f"""
                    <div class="course-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <h4>{course['code']} - {course['name']}</h4>
                                <p>?? {course['room']} | ?? {course['students']} students</p>
                            </div>
                            <div style="text-align: right;">
                                <h4 style="color: #667eea;">{course['schedule']}</h4>
                                <span class="badge-primary">2 hours</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No classes scheduled for {day}")

# REPORTS TAB
elif st.session_state.active_tab == "Reports":
    st.markdown("## ?? Generate Reports")
    
    # Report type selection
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Attendance Summary", "Grade Analysis", "Student Performance", "Course Analytics", "Department Report"]
        )
    with col2:
        report_format = st.selectbox("Format", ["PDF", "Excel", "CSV", "HTML"])
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Generate button
    if st.button("?? Generate Report", width='stretch'):
        with st.spinner("Generating report..."):
            time.sleep(2)
            st.success("Report generated successfully!")
            
            # Preview
            st.markdown('<div class="prof-card">', unsafe_allow_html=True)
            st.subheader(f"?? {report_type} Preview")
            
            # Sample preview data
            preview_data = pd.DataFrame({
                "Course": [c["code"] for c in courses],
                "Students": [c["students"] for c in courses],
                "Avg Attendance": [c["attendance_rate"] for c in courses],
                "Classes Completed": [c["completed"] for c in courses],
                "Assignments": [c["assignments"] for c in courses]
            })
            st.dataframe(preview_data, width='stretch', hide_index=True)
            
            st.markdown(f"**Date Range:** {start_date} to {end_date}")
            st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Download button
            csv = preview_data.to_csv(index=False)
            st.download_button(
                "?? Download Report",
                csv,
                f"{report_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
            st.markdown('</div>', unsafe_allow_html=True)

# PROFILE TAB
elif st.session_state.active_tab == "Profile":
    st.markdown("## ?? Lecturer Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="prof-card" style="text-align: center;">
            <img src="{LECTURER_PROFILE_PIC}" style="width: 150px; border-radius: 50%; margin: 20px auto;">
            <h2>{LECTURER_NAME}</h2>
            <p style="color: #666;">{LECTURER_TITLE}</p>
            <p style="color: #666;">{LECTURER_ID}</p>
            <span class="badge-success">Verified</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("?? Professional Information")
        
        info_data = {
            "Full Name": LECTURER_NAME,
            "Staff ID": LECTURER_ID,
            "Title": LECTURER_TITLE,
            "Department": "Information Technology",
            "Email": LECTURER_EMAIL,
            "Office": LECTURER_OFFICE,
            "Phone": LECTURER_PHONE,
            "Joined": "September 2015",
            "Qualifications": "PhD in Computer Science, MSc in IT, BSc in CS",
            "Research Areas": "Machine Learning, Data Science, Cybersecurity",
            "Publications": "25+ peer-reviewed papers",
            "Courses": f"{len(courses)} courses this semester"
        }
        
        for key, value in info_data.items():
            st.markdown(f"""
            <div style="display: flex; padding: 8px 0; border-bottom: 1px solid #eee;">
                <div style="width: 150px; font-weight: 600;">{key}:</div>
                <div>{value}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Edit profile button
        if st.button("?? Edit Profile", width='stretch'):
            st.info("Profile editing would be implemented here")

# SETTINGS TAB
elif st.session_state.active_tab == "Settings":
    st.markdown("## ?? Settings")
    
    tabs = st.tabs(["Account", "Notifications", "Course Preferences", "Privacy", "Appearance"])
    
    with tabs[0]:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("Account Settings")
        st.text_input("Email", value=LECTURER_EMAIL)
        st.text_input("Phone", value=LECTURER_PHONE)
        st.checkbox("Enable Two-Factor Authentication", value=True)
        st.checkbox("Auto-save grade entries", value=True)
        st.button("Change Password", width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("Notification Preferences")
        st.checkbox("Email notifications for attendance submissions", value=True)
        st.checkbox("SMS alerts for low attendance students", value=True)
        st.checkbox("Push notifications for class reminders", value=True)
        st.checkbox("Weekly summary reports", value=False)
        st.select_slider("Notification frequency", options=["Real-time", "Daily", "Weekly"], value="Real-time")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("Course Preferences")
        st.multiselect("Default courses to show", [c["code"] for c in courses], default=[c["code"] for c in courses])
        st.selectbox("Default grade scale", ["A-F (Standard)", "Percentage", "Pass/Fail"])
        st.checkbox("Auto-calculate final grades", value=True)
        st.checkbox("Show student photos in attendance list", value=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("Privacy Settings")
        st.checkbox("Make profile visible to students", value=True)
        st.checkbox("Share research interests publicly", value=True)
        st.checkbox("Allow students to book office hours online", value=True)
        st.checkbox("Display email to students", value=True)
        st.info("Your data is protected and encrypted")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[4]:
        st.markdown('<div class="prof-card">', unsafe_allow_html=True)
        st.subheader("Appearance")
        st.selectbox("Theme", ["Light", "Dark", "Professional (Default)"])
        st.selectbox("Color scheme", ["Purple", "Blue", "Green", "Orange"])
        st.slider("Font Size", 12, 20, 14)
        st.checkbox("Compact mode", value=False)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("?? Save All Settings", width='stretch'):
        st.success("Settings saved successfully!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"© 2026 University of Embu - {LECTURER_NAME}")
with col2:
    st.caption(f"Staff ID: {LECTURER_ID}")
with col3:
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
