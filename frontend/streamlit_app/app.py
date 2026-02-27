import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# Page config - MUST be first
st.set_page_config(
    page_title="University of Embu - Smart Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for advanced animations and styling
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated Gradient Background - Color Changing Effect */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab, #667eea, #764ba2);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        min-height: 100vh;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism Header */
    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 40px;
        margin: 20px 0 30px 0;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main-header h1 {
        font-size: 3.5em;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: glow 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        0% { text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        50% { text-shadow: 0 0 20px rgba(255,255,255,0.8); }
        100% { text-shadow: 0 0 10px rgba(255,255,255,0.5); }
    }
    
    /* Live Indicator */
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(220, 53, 69, 0.3);
        backdrop-filter: blur(5px);
        padding: 8px 20px;
        border-radius: 50px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        animation: pulse 2s infinite;
    }
    
    .pulse-dot {
        width: 12px;
        height: 12px;
        background: #ff4444;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse-dot 1.5s infinite;
        box-shadow: 0 0 10px #ff4444;
    }
    
    @keyframes pulse-dot {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Metric Cards with Color Transitions */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        margin: 10px 0;
        animation: fadeInUp 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, transparent 70%);
        animation: rotate 10s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2.8em;
        font-weight: 700;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: countUp 2s ease;
    }
    
    /* Portal Preview Cards */
    .portal-preview {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
        animation: float 6s ease-in-out infinite;
    }
    
    .portal-preview:hover {
        transform: translateY(-10px) scale(1.02);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .student-preview {
        border-left: 5px solid #667eea;
    }
    
    .lecturer-preview {
        border-right: 5px solid #764ba2;
    }
    
    .preview-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .preview-icon {
        font-size: 3em;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .preview-title {
        font-size: 1.8em;
        font-weight: 700;
        color: white;
    }
    
    .preview-subtitle {
        color: rgba(255,255,255,0.8);
        font-size: 0.9em;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        color: white;
    }
    
    .info-label {
        opacity: 0.8;
    }
    
    .info-value {
        font-weight: 600;
    }
    
    /* Action Button */
    .portal-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        margin-top: 20px;
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
    }
    
    .portal-action-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Activity Feed */
    .activity-item {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-left: 4px solid;
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 8px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    
    .chart-title {
        font-size: 1.2em;
        font-weight: 600;
        margin-bottom: 15px;
        color: white;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Footer */
    .footer {
        margin-top: 50px;
        padding: 20px;
        color: white;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for real-time data
if "analytics_data" not in st.session_state:
    st.session_state.analytics_data = {
        "total_students": 3250,
        "active_students": 2890,
        "total_staff": 145,
        "total_courses": 78,
        "today_attendance": random.randint(2400, 2800),
        "avg_attendance": 87.5,
        "system_uptime": datetime.now(),
        "verification_success": 98.2,
        "active_sessions": random.randint(18, 32),
        "last_updated": datetime.now()
    }

if "recent_activity" not in st.session_state:
    st.session_state.recent_activity = []

if "attendance_trend" not in st.session_state:
    # Generate 24 hours of data
    hours = [(datetime.now() - timedelta(hours=i)).strftime('%H:00') for i in range(24, 0, -1)]
    st.session_state.attendance_trend = {
        "hours": hours,
        "values": [random.randint(50, 200) for _ in range(24)]
    }

# Update real-time data function
def update_realtime_data():
    st.session_state.analytics_data["today_attendance"] = random.randint(2400, 2800)
    st.session_state.analytics_data["active_sessions"] = random.randint(18, 32)
    st.session_state.analytics_data["verification_success"] = round(98.2 + random.uniform(-0.8, 0.8), 1)
    st.session_state.analytics_data["last_updated"] = datetime.now()
    
    # Add random activity
    activities = [
        ("Salphine Chemos marked attendance - BBIT 401", "success"),
        ("Dr. Isaiah started class - BBIT 403", "info"),
        ("5 students verified - Lab 301", "info"),
        ("Low attendance alert - BBIT 402", "warning"),
        ("Attendance report generated", "info"),
        ("New student enrolled - BBIT 4th Year", "success"),
        ("Dr. Isaiah updated course materials", "info")
    ]
    
    if random.random() > 0.3:
        activity_text, activity_type = random.choice(activities)
        st.session_state.recent_activity.insert(0, {
            'time': datetime.now().strftime('%H:%M:%S'),
            'text': activity_text,
            'type': activity_type
        })
        st.session_state.recent_activity = st.session_state.recent_activity[:8]
    
    # Update trend
    st.session_state.attendance_trend["values"].pop(0)
    st.session_state.attendance_trend["values"].append(random.randint(50, 200))

# Call update function
update_realtime_data()

# Header with live indicator
st.markdown(f"""
<div class="main-header">
    <div class="live-badge">
        <span class="pulse-dot"></span>
        <span>LIVE SYSTEM • REAL-TIME UPDATES • {datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    <h1>🎓 University of Embu</h1>
    <h3>Smart Attendance System with AI-Powered Anti-Spoofing</h3>
    <p style="margin-top: 20px; opacity: 0.9;">{datetime.now().strftime('%A, %B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

attendance_percentage = (st.session_state.analytics_data['today_attendance'] / 
                        st.session_state.analytics_data['total_students']) * 100

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TOTAL STUDENTS</div>
        <div class="metric-value">{st.session_state.analytics_data['total_students']:,}</div>
        <div class="metric-change">↑ 124 this semester</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">TODAY'S ATTENDANCE</div>
        <div class="metric-value">{st.session_state.analytics_data['today_attendance']:,}</div>
        <div class="metric-change">{attendance_percentage:.1f}% of total</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">ACTIVE SESSIONS</div>
        <div class="metric-value">{st.session_state.analytics_data['active_sessions']}</div>
        <div class="metric-change">{st.session_state.analytics_data['total_courses']} total courses</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">VERIFICATION RATE</div>
        <div class="metric-value">{st.session_state.analytics_data['verification_success']}%</div>
        <div class="metric-change">99.9% anti-spoofing</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Real-time Attendance (Last 12 Hours)</div>', unsafe_allow_html=True)
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=st.session_state.attendance_trend["hours"][-12:],
        y=st.session_state.attendance_trend["values"][-12:],
        mode='lines+markers',
        name='Students per hour',
        line=dict(color='#ffffff', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 255, 255, 0.1)'
    ))
    
    fig_trend.update_layout(
        xaxis_title="Time",
        yaxis_title="Number of Students",
        hovermode='x unified',
        showlegend=False,
        height=300,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig_trend, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🔴 Live Activity Feed</div>', unsafe_allow_html=True)
    
    if st.session_state.recent_activity:
        for activity in st.session_state.recent_activity:
            if activity['type'] == 'success':
                border_color = "#4CAF50"
            elif activity['type'] == 'warning':
                border_color = "#FFC107"
            else:
                border_color = "#17a2b8"
            
            st.markdown(f"""
            <div class="activity-item" style="border-left-color: {border_color};">
                <span>{activity['text']}</span>
                <span style="font-size: 0.85em; opacity: 0.8;">{activity['time']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Portal Previews Section
st.markdown("<h2 style='color: white; text-align: center; margin: 40px 0 20px;'>🚀 Portal Previews</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Student Portal Preview
with col1:
    st.markdown("""
    <div class="portal-preview student-preview">
        <div class="preview-header">
            <div class="preview-icon">👨‍🎓</div>
            <div>
                <div class="preview-title">Student Portal</div>
                <div class="preview-subtitle">Salphine Chemos • BBIT 4th Year</div>
            </div>
        </div>
        <div class="info-row">
            <span class="info-label">Student ID:</span>
            <span class="info-value">BBIT-2022-0045</span>
        </div>
        <div class="info-row">
            <span class="info-label">Current GPA:</span>
            <span class="info-value">4.2</span>
        </div>
        <div class="info-row">
            <span class="info-label">Attendance Rate:</span>
            <span class="info-value">92%</span>
        </div>
        <div class="info-row">
            <span class="info-label">Courses Enrolled:</span>
            <span class="info-value">5</span>
        </div>
        <div class="info-row">
            <span class="info-label">Next Class:</span>
            <span class="info-value">BBIT 401 • 9:00 AM</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Open Full Student Portal", key="student_portal_btn", width='stretch'):
        st.switch_page("pages/01_Student_Portal.py")

# Lecturer Portal Preview
with col2:
    st.markdown("""
    <div class="portal-preview lecturer-preview">
        <div class="preview-header">
            <div class="preview-icon">👨‍🏫</div>
            <div>
                <div class="preview-title">Lecturer Portal</div>
                <div class="preview-subtitle">Dr. Isaiah • Senior Lecturer</div>
            </div>
        </div>
        <div class="info-row">
            <span class="info-label">Staff ID:</span>
            <span class="info-value">LEC-2015-0078</span>
        </div>
        <div class="info-row">
            <span class="info-label">Department:</span>
            <span class="info-value">Information Technology</span>
        </div>
        <div class="info-row">
            <span class="info-label">Courses Teaching:</span>
            <span class="info-value">5</span>
        </div>
        <div class="info-row">
            <span class="info-label">Total Students:</span>
            <span class="info-value">200+</span>
        </div>
        <div class="info-row">
            <span class="info-label">Avg. Class Attendance:</span>
            <span class="info-value">87%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Open Full Lecturer Portal", key="lecturer_portal_btn", width='stretch'):
        st.switch_page("pages/02_Lecturer_Portal.py")

# Quick Stats Row
st.markdown("<h2 style='color: white; text-align: center; margin: 40px 0 20px;'>📊 Today's Overview</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card" style="padding: 15px;">
        <div class="metric-label">Classes Today</div>
        <div class="metric-value">24</div>
        <div class="metric-change">Across all departments</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card" style="padding: 15px;">
        <div class="metric-label">Active Lecturers</div>
        <div class="metric-value">45</div>
        <div class="metric-change">78% online now</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card" style="padding: 15px;">
        <div class="metric-label">Pending Verifications</div>
        <div class="metric-value">23</div>
        <div class="metric-change">Processing</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    uptime = datetime.now() - st.session_state.analytics_data['system_uptime']
    hours = uptime.total_seconds() / 3600
    st.markdown(f"""
    <div class="metric-card" style="padding: 15px;">
        <div class="metric-label">System Uptime</div>
        <div class="metric-value">{hours:.1f}h</div>
        <div class="metric-change">99.9% reliability</div>
    </div>
    """, unsafe_allow_html=True)

# Footer with auto-refresh
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<p style="color: white; opacity: 0.8;">© 2026 University of Embu</p>', unsafe_allow_html=True)
with col2:
    st.markdown('<p style="color: white; opacity: 0.8; text-align: center;">Smart Attendance System v3.0</p>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<p style="color: white; opacity: 0.8; text-align: right;">Last Updated: {st.session_state.analytics_data["last_updated"].strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)

# Auto-refresh every 5 seconds using a small rerun
time.sleep(0.1)
st.rerun()

