
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Well Intervention Planning System",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .status-ok {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-critical {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation
@st.cache_data
def generate_sample_data():
    # Well data
    wells_data = {
        'Well_ID': ['Well_A', 'Well_B', 'Well_C', 'Well_D', 'Well_E', 'Well_F'],
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Alpha', 'Platform_Gamma', 'Platform_Beta', 'Platform_Gamma'],
        'Well_Type': ['Production', 'Injection', 'Production', 'Production', 'Injection', 'Production'],
        'Status': ['Active', 'Active', 'Maintenance', 'Active', 'Shutdown', 'Active'],
        'Last_Intervention': ['2024-12-10', '2024-11-15', '2025-01-05', '2024-10-20', '2024-09-30', '2025-01-12'],
        'Next_PM_Due': ['2025-07-01', '2025-06-15', '2025-08-01', '2025-05-20', '2025-04-30', '2025-08-12'],
        'Master_Valve': ['Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Pass'],
        'Swab_Valve': ['Fail', 'Pass', 'Pass', 'Pass', 'Fail', 'Pass'],
        'Wing_Valve': ['Pass', 'Pass', 'Pass', 'Fail', 'Pass', 'Pass'],
        'Integrity_Issues': ['Swab leak', 'None', 'Master valve stuck', 'Wing valve leak', 'Swab leak', 'None'],
        'Priority': ['High', 'Low', 'Critical', 'Medium', 'High', 'Low']
    }
    
    # Tools and equipment data
    tools_data = {
        'Tool_Equipment': ['Wireline Unit', 'Coiled Tubing', 'Wellhead Control Panel', 'Subsea Tree', 'Slickline Tools', 
                          'Snubbing Unit', 'Pumping Unit', 'BOP Stack', 'Workover Rig', 'Logging Tools'],
        'Category': ['Intervention', 'Intervention', 'Surface Equipment', 'Subsea Equipment', 'Intervention',
                    'Intervention', 'Stimulation', 'Safety Equipment', 'Heavy Equipment', 'Logging'],
        'Description': ['For logging & intervention operations', 'For cleanouts, acidizing, etc.', 
                       'Surface safety system control', 'Subsea well control system', 'Simple mechanical jobs',
                       'High pressure intervention', 'Fluid pumping operations', 'Blowout prevention',
                       'Heavy workover operations', 'Formation evaluation'],
        'Status': ['Available', 'In Use', 'Available', 'Maintenance', 'Available', 
                  'Available', 'In Use', 'Available', 'Scheduled', 'Available'],
        'Next_Maintenance': ['2025-03-15', '2025-04-20', '2025-02-28', '2025-02-10', '2025-05-01',
                           '2025-03-30', '2025-04-15', '2025-02-25', '2025-06-01', '2025-03-10']
    }
    
    # Platform bed space data
    bed_space_data = {
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Gamma'],
        'Total_Beds': [20, 15, 25],
        'Occupied_Beds': [12, 5, 18],
        'Available_Beds': [8, 10, 7],
        'Forecast_Change': ['+2 next week', '-3 next week', '+1 next week']
    }
    
    # Work disciplines data
    disciplines_data = {
        'Discipline': ['Well Services', 'Subsea Engineering', 'Production Technology', 'Logistics & Marine', 
                      'HSE', 'Instrumentation & Controls', 'Drilling', 'Completions'],
        'Personnel_Required': [15, 8, 12, 6, 4, 10, 20, 14],
        'Current_Available': [12, 8, 10, 5, 4, 8, 18, 12],
        'Certification_Level': ['Level 3', 'Level 4', 'Level 3', 'Level 2', 'Level 5', 'Level 3', 'Level 4', 'Level 3']
    }
    
    return pd.DataFrame(wells_data), pd.DataFrame(tools_data), pd.DataFrame(bed_space_data), pd.DataFrame(disciplines_data)

# Load data
wells_df, tools_df, bed_space_df, disciplines_df = generate_sample_data()

# Sidebar navigation
st.sidebar.title("🛢️ Navigation")
page = st.sidebar.selectbox("Select Page", [
    "Dashboard", "Wells Management", "Scheduling & Planning", "Tools & Equipment", 
    "Logistics", "Work Disciplines", "Well History", "Integrity Management"
])

# Main header
st.markdown('<h1 class="main-header">Well Intervention Planning System</h1>', unsafe_allow_html=True)

if page == "Dashboard":
    st.header("📊 Executive Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Active Wells</h3>
            <h2>4</h2>
            <p>Out of 6 total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Overdue PMs</h3>
            <h2>2</h2>
            <p>Require attention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Critical Issues</h3>
            <h2>1</h2>
            <p>Well C - Master valve</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Available Beds</h3>
            <h2>25</h2>
            <p>Across all platforms</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Well Status Distribution")
        status_counts = wells_df['Status'].value_counts()
        fig_pie = px.pie(values=status_counts.values, names=status_counts.index, 
                        color_discrete_sequence=['#2E8B57', '#FF6347', '#4682B4', '#DAA520'])
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Platform Bed Space Utilization")
        fig_bar = px.bar(bed_space_df, x='Platform', y=['Occupied_Beds', 'Available_Beds'],
                        title="Bed Space by Platform", barmode='stack')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Recent activities
    st.subheader("🔔 Recent Activities & Alerts")
    activities = [
        {"Date": "2025-01-15", "Activity": "Well C - Master valve failure detected", "Priority": "Critical"},
        {"Date": "2025-01-14", "Activity": "Coiled tubing unit mobilized to Platform Beta", "Priority": "Medium"},
        {"Date": "2025-01-13", "Activity": "Well A - Swab valve test failed", "Priority": "High"},
        {"Date": "2025-01-12", "Activity": "Platform Alpha - 2 additional beds available", "Priority": "Low"}
    ]
    
    for activity in activities:
        priority_class = f"status-{'critical' if activity['Priority'] == 'Critical' else 'warning' if activity['Priority'] == 'High' else 'ok'}"
        st.markdown(f"""
        <div style="border-left: 4px solid #1f4e79; padding: 10px; margin: 10px 0; background-color: #f8f9fa;">
            <strong>{activity['Date']}</strong> - {activity['Activity']} 
            <span class="{priority_class}">{activity['Priority']}</span>
        </div>
        """, unsafe_allow_html=True)

elif page == "Wells Management":
    st.header("🏭 Wells Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        platform_filter = st.selectbox("Filter by Platform", ["All"] + list(wells_df['Platform'].unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(wells_df['Status'].unique()))
    with col3:
        priority_filter = st.selectbox("Filter by Priority", ["All"] + list(wells_df['Priority'].unique()))
    
    # Apply filters
    filtered_df = wells_df.copy()
    if platform_filter != "All":
        filtered_df = filtered_df[filtered_df['Platform'] == platform_filter]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    if priority_filter != "All":
        filtered_df = filtered_df[filtered_df['Priority'] == priority_filter]
    
    # Wells table with expandable details
    st.subheader("Wells Overview")
    
    for idx, well in filtered_df.iterrows():
        with st.expander(f"🔧 {well['Well_ID']} - {well['Platform']} ({well['Status']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Well Type:** {well['Well_Type']}")
                st.write(f"**Last Intervention:** {well['Last_Intervention']}")
                st.write(f"**Next PM Due:** {well['Next_PM_Due']}")
                st.write(f"**Priority:** {well['Priority']}")
            
            with col2:
                st.write("**Valve Test Results:**")
                st.write(f"• Master Valve: {well['Master_Valve']}")
                st.write(f"• Swab Valve: {well['Swab_Valve']}")
                st.write(f"• Wing Valve: {well['Wing_Valve']}")
                
                if well['Integrity_Issues'] != 'None':
                    st.error(f"⚠️ Integrity Issue: {well['Integrity_Issues']}")
            
            col3, col4, col5 = st.columns(3)
            with col3:
                if st.button(f"Schedule Maintenance - {well['Well_ID']}", key=f"schedule_{well['Well_ID']}"):
                    st.success(f"Maintenance scheduled for {well['Well_ID']}")
            with col4:
                if st.button(f"View History - {well['Well_ID']}", key=f"history_{well['Well_ID']}"):
                    st.info(f"Opening history for {well['Well_ID']}")
            with col5:
                if st.button(f"Generate Report - {well['Well_ID']}", key=f"report_{well['Well_ID']}"):
                    st.info(f"Generating report for {well['Well_ID']}")

elif page == "Scheduling & Planning":
    st.header("📅 Scheduling & Work Planning")
    
    # Gantt chart simulation
    st.subheader("Work Schedule - Gantt Chart View")
    
    # Sample scheduling data
    schedule_data = {
        'Task': ['Well A - PM', 'Well B - Intervention', 'Well C - Repair', 'Platform Alpha - Shutdown', 'Well D - Testing'],
        'Start': ['2025-02-01', '2025-02-05', '2025-02-10', '2025-02-15', '2025-02-20'],
        'End': ['2025-02-03', '2025-02-08', '2025-02-14', '2025-02-18', '2025-02-22'],
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Alpha', 'Platform_Alpha', 'Platform_Gamma'],
        'Status': ['Planned', 'In Progress', 'Planned', 'Scheduled', 'Planned']
    }
    
    schedule_df = pd.DataFrame(schedule_data)
    schedule_df['Start'] = pd.to_datetime(schedule_df['Start'])
    schedule_df['End'] = pd.to_datetime(schedule_df['End'])
    
    fig_gantt = px.timeline(schedule_df, x_start="Start", x_end="End", y="Task", 
                           color="Platform", title="Work Schedule Timeline")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    # Shutdown maintenance plan
    st.subheader("🔧 Shutdown Maintenance Forward Plan")
    
    shutdown_data = {
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Gamma'],
        'Next_Shutdown': ['2025-04-15', '2025-06-20', '2025-08-10'],
        'Duration_Days': [5, 7, 4],
        'Planned_Work': ['Compressor overhaul, Valve testing', 'Turbine maintenance, Safety systems', 'Electrical upgrades, Piping'],
        'Status': ['Planned', 'Scheduled', 'Planning']
    }
    
    shutdown_df = pd.DataFrame(shutdown_data)
    st.dataframe(shutdown_df, use_container_width=True)
    
    # Work windows
    st.subheader("⏰ Available Work Windows")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Weather Windows (Next 14 days):**")
        weather_windows = [
            "Feb 1-3: Excellent (Wave height <1m)",
            "Feb 4-6: Good (Wave height 1-2m)",
            "Feb 7-9: Poor (Wave height >3m)",
            "Feb 10-12: Excellent (Wave height <1m)",
            "Feb 13-14: Good (Wave height 1-2m)"
        ]
        for window in weather_windows:
            st.write(f"• {window}")
    
    with col2:
        st.write("**Operational Windows:**")
        op_windows = [
            "Platform Alpha: 24/7 operations",
            "Platform Beta: Daylight only (06:00-18:00)",
            "Platform Gamma: Limited access (Maintenance mode)"
        ]
        for window in op_windows:
            st.write(f"• {window}")

elif page == "Tools & Equipment":
    st.header("🔧 Tools & Equipment Management")
    
    # Equipment status overview
    col1, col2, col3 = st.columns(3)
    with col1:
        available_count = len(tools_df[tools_df['Status'] == 'Available'])
        st.metric("Available Equipment", available_count, delta=2)
    with col2:
        in_use_count = len(tools_df[tools_df['Status'] == 'In Use'])
        st.metric("Equipment In Use", in_use_count, delta=-1)
    with col3:
        maintenance_count = len(tools_df[tools_df['Status'] == 'Maintenance'])
        st.metric("Under Maintenance", maintenance_count, delta=0)
    
    # Equipment table with links
    st.subheader("Equipment Inventory")
    
    # Add information links
    info_links = {
        'Wireline Unit': 'https://petrowiki.org/Wireline_operations',
        'Coiled Tubing': 'https://petrowiki.org/Coiled_tubing_operations',
        'Wellhead Control Panel': 'https://en.wikipedia.org/wiki/Wellhead',
        'Subsea Tree': 'https://petrowiki.org/Subsea_trees',
        'Slickline Tools': 'https://petrowiki.org/Slickline_operations',
        'Snubbing Unit': 'https://petrowiki.org/Snubbing',
        'Pumping Unit': 'https://petrowiki.org/Artificial_lift',
        'BOP Stack': 'https://petrowiki.org/Blowout_preventers',
        'Workover Rig': 'https://petrowiki.org/Workover_operations',
        'Logging Tools': 'https://petrowiki.org/Well_logging'
    }
    
    # Enhanced tools display
    for idx, tool in tools_df.iterrows():
        with st.expander(f"🛠️ {tool['Tool_Equipment']} - {tool['Status']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Category:** {tool['Category']}")
                st.write(f"**Description:** {tool['Description']}")
                st.write(f"**Status:** {tool['Status']}")
            
            with col2:
                st.write(f"**Next Maintenance:** {tool['Next_Maintenance']}")
                if tool['Tool_Equipment'] in info_links:
                    st.markdown(f"[📖 Technical Information]({info_links[tool['Tool_Equipment']]})")
            
            with col3:
                if st.button(f"Schedule Use - {tool['Tool_Equipment']}", key=f"use_{idx}"):
                    st.success(f"Usage scheduled for {tool['Tool_Equipment']}")
                if st.button(f"Maintenance Log - {tool['Tool_Equipment']}", key=f"maint_{idx}"):
                    st.info(f"Opening maintenance log for {tool['Tool_Equipment']}")

elif page == "Logistics":
    st.header("🚁 Logistics & Marine Operations")
    
    # Logistics overview
    st.subheader("Logistics Requirements Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personnel Transport Schedule:**")
        transport_schedule = [
            "Feb 1: Helicopter to Platform Alpha (6 personnel)",
            "Feb 2: Supply vessel to Platform Beta (Equipment)",
            "Feb 3: Helicopter to Platform Gamma (4 personnel)",
            "Feb 4: Crew change - All platforms",
            "Feb 5: Emergency standby helicopter"
        ]
        for item in transport_schedule:
            st.write(f"• {item}")
    
    with col2:
        st.write("**Supply Requirements:**")
        supply_reqs = [
            "Chemicals: 500L acid, 200L inhibitor",
            "Spares: Valve seats, O-rings, gaskets",
            "Consumables: Lubricants, cleaning agents",
            "Safety equipment: Gas detectors, PPE",
            "Tools: Torque wrenches, pressure gauges"
        ]
        for item in supply_reqs:
            st.write(f"• {item}")
    
    # Bed space tracker
    st.subheader("🛏️ Platform Bed Space Tracker")
    
    fig_beds = px.bar(bed_space_df, x='Platform', y=['Occupied_Beds', 'Available_Beds'],
                     title="Current Bed Space Utilization", barmode='stack',
                     color_discrete_map={'Occupied_Beds': '#FF6B6B', 'Available_Beds': '#4ECDC4'})
    st.plotly_chart(fig_beds, use_container_width=True)
    
    # Detailed bed space table
    st.dataframe(bed_space_df, use_container_width=True)
    
    # Marine weather conditions
    st.subheader("🌊 Marine Conditions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Wave Height", "1.2m", delta="-0.3m")
    with col2:
        st.metric("Wind Speed", "15 knots", delta="2 knots")
    with col3:
        st.metric("Visibility", "8 km", delta="Good")

elif page == "Work Disciplines":
    st.header("👥 Work Disciplines & Personnel")
    
    # Personnel overview
    st.subheader("Personnel Requirements vs Availability")
    
    fig_personnel = px.bar(disciplines_df, x='Discipline', y=['Personnel_Required', 'Current_Available'],
                          title="Personnel Requirements by Discipline", barmode='group',
                          color_discrete_map={'Personnel_Required': '#FF9999', 'Current_Available': '#66B2FF'})
    fig_personnel.update_xaxes(tickangle=45)
    st.plotly_chart(fig_personnel, use_container_width=True)
    
    # Detailed disciplines table
    st.subheader("Discipline Details")
    
    for idx, discipline in disciplines_df.iterrows():
        with st.expander(f"👨‍🔧 {discipline['Discipline']} - {discipline['Certification_Level']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Required Personnel:** {discipline['Personnel_Required']}")
                st.write(f"**Currently Available:** {discipline['Current_Available']}")
                shortage = discipline['Personnel_Required'] - discipline['Current_Available']
                if shortage > 0:
                    st.error(f"**Shortage:** {shortage} personnel")
                else:
                    st.success("**Status:** Fully staffed")
            
            with col2:
                st.write(f"**Certification Level:** {discipline['Certification_Level']}")
                st.write("**Key Responsibilities:**")
                responsibilities = {
                    'Well Services': ['Wireline operations', 'Coiled tubing', 'Well testing'],
                    'Subsea Engineering': ['Tree maintenance', 'Umbilical repair', 'ROV operations'],
                    'Production Technology': ['Process optimization', 'Flow assurance', 'Facility operations'],
                    'Logistics & Marine': ['Supply coordination', 'Personnel transport', 'Marine operations'],
                    'HSE': ['Safety oversight', 'Environmental compliance', 'Risk assessment'],
                    'Instrumentation & Controls': ['Control system maintenance', 'Calibration', 'Automation'],
                 