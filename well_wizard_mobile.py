import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
from datetime import timedelta

# Mobile-optimized page config
st.set_page_config(
    page_title="Well Wizard Mobile",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar on mobile
)

# Mobile-optimized CSS
st.markdown("""
<style>
    .main-header {
        font-size: 1.8rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .mobile-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    .status-ok {
        background-color: #28a745;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem 0;
    }
    .status-warning {
        background-color: #ffc107;
        color: #212529;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem 0;
    }
    .status-critical {
        background-color: #dc3545;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        margin: 0.25rem 0;
    }
    .big-button {
        background-color: #007bff;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        border: none;
        width: 100%;
    }
    .emergency-button {
        background-color: #dc3545;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: bold;
        margin: 1rem 0;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sample mobile data
@st.cache_data
def generate_mobile_data():
    current_jobs = pd.DataFrame({
        'Job_ID': ['JOB001', 'JOB002', 'JOB003'],
        'Well': ['Well_A', 'Well_C', 'Well_D'],
        'Task': ['Swab Valve Repair', 'Master Valve Replacement', 'Wing Valve Maintenance'],
        'Status': ['In Progress', 'Scheduled', 'Completed'],
        'Priority': ['High', 'Critical', 'Medium'],
        'Assigned_To': ['John Smith', 'Sarah Johnson', 'Mike Wilson'],
        'Progress': [65, 0, 100],
        'ETA': ['2 hours', '4 hours', 'Completed']
    })
    
    alerts = pd.DataFrame({
        'Time': ['08:30', '07:15', '06:45'],
        'Well': ['Well_C', 'Well_A', 'Well_H'],
        'Alert': ['Master valve failure', 'Swab valve leak', 'Pressure anomaly'],
        'Priority': ['Critical', 'High', 'Medium']
    })
    
    return current_jobs, alerts

current_jobs, alerts = generate_mobile_data()

# Header
st.markdown('<h1 class="main-header">📱 Well Wizard Mobile</h1>', unsafe_allow_html=True)

# Navigation tabs (mobile-friendly)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📋 Jobs", "🚨 Alerts", "📊 Status", "⚙️ Tools"])

# HOME TAB
with tab1:
    st.subheader("🏠 Field Operations Dashboard")
    
    # Quick stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="mobile-card"><h3>Active Jobs</h3><h2>3</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="mobile-card"><h3>Critical Alerts</h3><h2>1</h2></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="mobile-card"><h3>Tools Available</h3><h2>12</h2></div>', unsafe_allow_html=True)
        st.markdown('<div class="mobile-card"><h3>Personnel On Site</h3><h2>8</h2></div>', unsafe_allow_html=True)
    
    # Emergency button
    st.markdown("---")
    if st.button("🚨 EMERGENCY SHUTDOWN", key="emergency", help="Initiate emergency procedures"):
        st.error("🚨 EMERGENCY PROCEDURES INITIATED")
        st.write("- All operations halted")
        st.write("- Safety team notified")
        st.write("- Control room alerted")
        st.write("Contact: Emergency Hotline +1-800-EMERGENCY")
    
    # Quick actions
    st.subheader("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Update Job Status", key="update_job"):
            st.success("Job status update form opened")
        
        if st.button("📷 Photo Report", key="photo_report"):
            st.info("Camera opened for documentation")
    
    with col2:
        if st.button("📞 Call Control Room", key="call_control"):
            st.info("Connecting to control room...")
        
        if st.button("🔧 Request Tools", key="request_tools"):
            st.success("Tool request submitted")

# JOBS TAB
with tab2:
    st.subheader("📋 Current Jobs")
    
    # Job cards (mobile-friendly)
    for _, job in current_jobs.iterrows():
        with st.expander(f"{job['Job_ID']} - {job['Well']} ({job['Status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Task:** {job['Task']}")
                st.write(f"**Assigned:** {job['Assigned_To']}")
                st.write(f"**Priority:** {job['Priority']}")
            
            with col2:
                st.write(f"**Status:** {job['Status']}")
                st.write(f"**Progress:** {job['Progress']}%")
                st.write(f"**ETA:** {job['ETA']}")
            
            # Progress bar
            if job['Status'] != 'Completed':
                st.progress(job['Progress'] / 100)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Update", key=f"update_{job['Job_ID']}"):
                    st.success(f"Updating {job['Job_ID']}")
            with col2:
                if st.button("📷 Photo", key=f"photo_{job['Job_ID']}"):
                    st.info(f"Photo capture for {job['Job_ID']}")
            with col3:
                if st.button("📞 Call", key=f"call_{job['Job_ID']}"):
                    st.info(f"Calling supervisor for {job['Job_ID']}")

# ALERTS TAB
with tab3:
    st.subheader("🚨 Active Alerts")
    
    # Alert cards
    for _, alert in alerts.iterrows():
        priority_class = f"status-{alert['Priority'].lower()}"
        
        st.markdown(f"""
        <div class="{priority_class}">
            <strong>{alert['Time']}</strong> - {alert['Well']}<br>
            {alert['Alert']}<br>
            Priority: {alert['Priority']}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons for each alert
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Acknowledge", key=f"ack_{alert['Well']}"):
                st.success(f"Alert acknowledged for {alert['Well']}")
        with col2:
            if st.button("🔧 Respond", key=f"respond_{alert['Well']}"):
                st.info(f"Response initiated for {alert['Well']}")
        with col3:
            if st.button("📞 Escalate", key=f"escalate_{alert['Well']}"):
                st.warning(f"Alert escalated for {alert['Well']}")
        
        st.markdown("---")

# STATUS TAB
with tab4:
    st.subheader("📊 Real-Time Status")
    
    # Well status
    st.write("**Well Status Overview**")
    well_status = pd.DataFrame({
        'Well': ['Well_A', 'Well_B', 'Well_C', 'Well_D'],
        'Status': ['Active', 'Active', 'Maintenance', 'Active'],
        'Pressure': ['2150 psi', '2200 psi', 'Shut-in', '2180 psi'],
        'Flow_Rate': ['1200 bbl/d', '1350 bbl/d', '0 bbl/d', '1100 bbl/d']
    })
    
    for _, well in well_status.iterrows():
        status_color = "status-ok" if well['Status'] == 'Active' else "status-warning"
        st.markdown(f"""
        <div class="{status_color}">
            <strong>{well['Well']}</strong> - {well['Status']}<br>
            Pressure: {well['Pressure']} | Flow: {well['Flow_Rate']}
        </div>
        """, unsafe_allow_html=True)
    
    # Weather conditions
    st.write("**Current Conditions**")
    st.markdown("""
    <div class="mobile-card">
        <strong>Weather & Marine</strong><br>
        Wave Height: 1.2m | Wind: 15 knots<br>
        Visibility: 8km | Sea State: Slight
    </div>
    """, unsafe_allow_html=True)

# TOOLS TAB
with tab5:
    st.subheader("⚙️ Tools & Equipment")
    
    # Tool status
    tools_status = pd.DataFrame({
        'Tool': ['Wireline Unit', 'Coiled Tubing', 'BOP Stack', 'Pumping Unit', 'Crane'],
        'Status': ['Available', 'In Use', 'Available', 'In Use', 'Available'],
        'Location': ['Deck A', 'Well C', 'Deck B', 'Well A', 'Deck C'],
        'Next_PM': ['15 days', '30 days', '5 days', '20 days', '10 days']
    })
    
    for _, tool in tools_status.iterrows():
        status_color = "status-ok" if tool['Status'] == 'Available' else "status-warning"
        
        with st.expander(f"{tool['Tool']} - {tool['Status']}"):
            st.markdown(f"""
            <div class="{status_color}">
                <strong>{tool['Tool']}</strong><br>
                Status: {tool['Status']}<br>
                Location: {tool['Location']}<br>
                Next PM: {tool['Next_PM']}
            </div>
            """, unsafe_allow_html=True)
            
            # Tool action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Request", key=f"req_{tool['Tool']}"):
                    st.success(f"Request submitted for {tool['Tool']}")
            with col2:
                if st.button("📍 Locate", key=f"loc_{tool['Tool']}"):
                    st.info(f"Location: {tool['Location']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 10px; font-size: 0.9rem;">
    📱 Well Wizard Mobile v1.0<br>
    Emergency: +1-800-EMERGENCY | Support: help@wellwizard.com
</div>
""", unsafe_allow_html=True)