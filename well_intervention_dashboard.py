Here's the **complete, full code** for your Well Wizard app with the sidebar updated to include "Well-Wizard Training Field" instead of rigs:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
from datetime import timedelta

# Set page config
st.set_page_config(
    page_title="Well Wizard - Intervention Planning System",
    page_icon="🧙‍♂️",
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
    .training-card {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sample data generation
@st.cache_data
def generate_sample_data():
    wells_data = {
        'Well_ID': ['Well_A', 'Well_B', 'Well_C', 'Well_D', 'Well_E', 'Well_F', 'Well_G', 'Well_H'],
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Alpha', 'Platform_Gamma', 'Platform_Beta', 'Platform_Gamma', 'Platform_Alpha', 'Platform_Beta'],
        'Well_Type': ['Production', 'Injection', 'Production', 'Production', 'Injection', 'Production', 'Production', 'Injection'],
        'Status': ['Active', 'Active', 'Maintenance', 'Active', 'Shutdown', 'Active', 'Active', 'Maintenance'],
        'Last_Intervention': ['2024-12-10', '2024-11-15', '2025-01-05', '2024-10-20', '2024-09-30', '2025-01-12', '2024-11-25', '2025-01-08'],
        'Next_PM_Due': ['2025-07-01', '2025-06-15', '2025-08-01', '2025-05-20', '2025-04-30', '2025-08-12', '2025-06-30', '2025-07-15'],
        'Master_Valve': ['Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Pass', 'Pass', 'Fail'],
        'Swab_Valve': ['Fail', 'Pass', 'Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Pass'],
        'Wing_Valve': ['Pass', 'Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Fail', 'Pass'],
        'Integrity_Issues': ['Swab leak', 'None', 'Master valve stuck', 'Wing valve leak', 'Swab leak', 'None', 'Wing valve leak', 'Master valve stuck'],
        'Priority': ['High', 'Low', 'Critical', 'Medium', 'High', 'Low', 'Medium', 'Critical'],
        'Production_Rate': [1200, 0, 800, 1500, 0, 1100, 1300, 0],
        'Water_Cut': [25, 0, 45, 15, 0, 30, 20, 0]
    }
    
    tools_data = {
        'Tool_Equipment': ['Wireline Unit', 'Coiled Tubing', 'Wellhead Control Panel', 'Subsea Tree', 'Slickline Tools', 
                          'Snubbing Unit', 'Pumping Unit', 'BOP Stack', 'Workover Rig', 'Logging Tools',
                          'Pressure Testing Unit', 'Chemical Injection Skid', 'Nitrogen Unit', 'Crane', 'ROV'],
        'Category': ['Intervention', 'Intervention', 'Surface Equipment', 'Subsea Equipment', 'Intervention',
                    'Intervention', 'Stimulation', 'Safety Equipment', 'Heavy Equipment', 'Logging',
                    'Testing', 'Chemical', 'Gas Services', 'Lifting', 'Subsea'],
        'Description': ['For logging & intervention operations', 'For cleanouts, acidizing, etc.', 
                       'Surface safety system control', 'Subsea well control system', 'Simple mechanical jobs',
                       'High pressure intervention', 'Fluid pumping operations', 'Blowout prevention',
                       'Heavy workover operations', 'Formation evaluation', 'Pressure integrity testing',
                       'Chemical treatment delivery', 'Nitrogen services', 'Heavy lifting operations', 'Subsea operations'],
        'Status': ['Available', 'In Use', 'Available', 'Maintenance', 'Available', 
                  'Available', 'In Use', 'Available', 'Scheduled', 'Available',
                  'Available', 'In Use', 'Available', 'Available', 'Maintenance'],
        'Next_Maintenance': ['2025-03-15', '2025-04-20', '2025-02-28', '2025-02-10', '2025-05-01',
                           '2025-03-30', '2025-04-15', '2025-02-25', '2025-06-01', '2025-03-10',
                           '2025-04-05', '2025-03-20', '2025-05-15', '2025-04-10', '2025-02-15']
    }
    
    bed_space_data = {
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Gamma'],
        'Total_Beds': [20, 15, 25],
        'Occupied_Beds': [12, 5, 18],
        'Available_Beds': [8, 10, 7],
        'Forecast_Change': ['+2 next week', '-3 next week', '+1 next week']
    }
    
    disciplines_data = {
        'Discipline': ['Well Services', 'Subsea Engineering', 'Production Technology', 'Logistics & Marine', 
                      'HSE', 'Instrumentation & Controls', 'Drilling', 'Completions', 'Reservoir Engineering', 'Facilities'],
        'Personnel_Required': [15, 8, 12, 6, 4, 10, 20, 14, 5, 8],
        'Current_Available': [12, 8, 10, 5, 4, 8, 18, 12, 5, 6],
        'Certification_Level': ['Level 3', 'Level 4', 'Level 3', 'Level 2', 'Level 5', 'Level 3', 'Level 4', 'Level 3', 'Level 4', 'Level 2']
    }
    
    return pd.DataFrame(wells_data), pd.DataFrame(tools_data), pd.DataFrame(bed_space_data), pd.DataFrame(disciplines_data)

wells_df, tools_df, bed_space_df, disciplines_df = generate_sample_data()

# Sidebar navigation
st.sidebar.title("🧙‍♂️ Well Wizard Navigation")
page = st.sidebar.selectbox("Select Page", [
    "Dashboard",
    "Wells Management",
    "Scheduling & Planning",
    "Tools & Equipment",
    "Logistics",
    "Work Disciplines",
    "Well History",
    "Integrity Management",
    "Well-Wizard Training Field"
])

st.markdown('<h1 class="main-header">🧙‍♂️ Well Wizard - Intervention Planning System</h1>', unsafe_allow_html=True)

# Dashboard Page
if page == "Dashboard":
    st.header("📊 Executive Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Active Wells</h3><h2>6</h2></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card"><h3>Critical Issues</h3><h2>2</h2></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card"><h3>Scheduled Jobs</h3><h2>4</h2></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card"><h3>Available Tools</h3><h2>9</h2></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Well Status Distribution")
        status_counts = wells_df['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, 
                    color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c', '#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Priority Distribution")
        priority_counts = wells_df['Priority'].value_counts()
        fig = px.bar(x=priority_counts.index, y=priority_counts.values,
                    color=priority_counts.index,
                    color_discrete_map={'Critical': '#e74c3c', 'High': '#f39c12', 'Medium': '#f1c40f', 'Low': '#2ecc71'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Alerts
    st.subheader("🚨 Recent Alerts")
    alerts = [
        {"Time": "2025-01-24 08:30", "Well": "Well_C", "Alert": "Master valve failure detected", "Priority": "Critical"},
        {"Time": "2025-01-24 07:15", "Well": "Well_A", "Alert": "Swab valve leak identified", "Priority": "High"},
        {"Time": "2025-01-23 16:45", "Well": "Well_H", "Alert": "Master valve stuck", "Priority": "Critical"},
        {"Time": "2025-01-23 14:20", "Well": "Well_D", "Alert": "Wing valve leak", "Priority": "Medium"}
    ]
    
    for alert in alerts:
        priority_class = f"status-{alert['Priority'].lower()}" if alert['Priority'].lower() in ['critical', 'warning'] else "status-ok"
        st.markdown(f"""
        <div style="border-left: 4px solid #3498db; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
            <strong>{alert['Time']}</strong> - {alert['Well']}: {alert['Alert']} 
            <span class="{priority_class}">{alert['Priority']}</span>
        </div>
        """, unsafe_allow_html=True)

# Wells Management Page
elif page == "Wells Management":
    st.header("🛢️ Wells Management")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        platform_filter = st.selectbox("Filter by Platform", ["All"] + list(wells_df['Platform'].unique()))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All"] + list(wells_df['Status'].unique()))
    with col3:
        priority_filter = st.selectbox("Filter by Priority", ["All"] + list(wells_df['Priority'].unique()))
    
    # Apply filters
    filtered_wells = wells_df.copy()
    if platform_filter != "All":
        filtered_wells = filtered_wells[filtered_wells['Platform'] == platform_filter]
    if status_filter != "All":
        filtered_wells = filtered_wells[filtered_wells['Status'] == status_filter]
    if priority_filter != "All":
        filtered_wells = filtered_wells[filtered_wells['Priority'] == priority_filter]
    
    # Wells table
    st.subheader("Wells Overview")
    st.dataframe(filtered_wells, use_container_width=True)
    
    # Well details expander
    st.subheader("Well Details")
    selected_well = st.selectbox("Select Well for Details", wells_df['Well_ID'].tolist())
    
    if selected_well:
        well_data = wells_df[wells_df['Well_ID'] == selected_well].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Platform:** {well_data['Platform']}")
            st.write(f"**Well Type:** {well_data['Well_Type']}")
            st.write(f"**Status:** {well_data['Status']}")
            st.write(f"**Priority:** {well_data['Priority']}")
        
        with col2:
            st.write(f"**Last Intervention:** {well_data['Last_Intervention']}")
            st.write(f"**Next PM Due:** {well_data['Next_PM_Due']}")
            st.write(f"**Production Rate:** {well_data['Production_Rate']} bbl/day")
            st.write(f"**Water Cut:** {well_data['Water_Cut']}%")

# Scheduling & Planning Page
elif page == "Scheduling & Planning":
    st.header("📅 Scheduling & Planning")
    
    # Gantt Chart simulation
    st.subheader("Work Schedule - Next 30 Days")
    
    # Generate sample schedule data
    schedule_data = []
    start_date = datetime.datetime.now()
    
    jobs = [
        {"Well": "Well_A", "Job": "Swab Valve Repair", "Duration": 3, "Priority": "High"},
        {"Well": "Well_C", "Job": "Master Valve Replacement", "Duration": 5, "Priority": "Critical"},
        {"Well": "Well_D", "Job": "Wing Valve Maintenance", "Duration": 2, "Priority": "Medium"},
        {"Well": "Well_E", "Job": "Routine PM", "Duration": 1, "Priority": "Low"},
        {"Well": "Well_H", "Job": "Master Valve Repair", "Duration": 4, "Priority": "Critical"}
    ]
    
    for i, job in enumerate(jobs):
        start = start_date + timedelta(days=i*2)
        end = start + timedelta(days=job["Duration"])
        schedule_data.append({
            "Task": f"{job['Well']} - {job['Job']}",
            "Start": start,
            "Finish": end,
            "Priority": job["Priority"]
        })
    
    # Create Gantt chart
    fig = go.Figure()
    
    colors = {"Critical": "#e74c3c", "High": "#f39c12", "Medium": "#f1c40f", "Low": "#2ecc71"}
    
    for i, task in enumerate(schedule_data):
        fig.add_trace(go.Scatter(
            x=[task["Start"], task["Finish"]],
            y=[i, i],
            mode='lines',
            line=dict(color=colors[task["Priority"]], width=20),
            name=task["Task"],
            showlegend=False
        ))
    
    fig.update_layout(
        title="Work Schedule Gantt Chart",
        xaxis_title="Date",
        yaxis_title="Tasks",
        yaxis=dict(tickmode='array', tickvals=list(range(len(schedule_data))), 
                  ticktext=[task["Task"] for task in schedule_data]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Work windows
    st.subheader("Available Work Windows")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Platform Alpha**")
        st.write("- Weather Window: 5 days (Good)")
        st.write("- Production Shutdown: Available")
        st.write("- Crew Availability: 85%")
    
    with col2:
        st.write("**Platform Beta**")
        st.write("- Weather Window: 3 days (Marginal)")
        st.write("- Production Shutdown: Restricted")
        st.write("- Crew Availability: 70%")

# Tools & Equipment Page
elif page == "Tools & Equipment":
    st.header("🔧 Tools & Equipment Management")
    
    # Equipment status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_count = len(tools_df[tools_df['Status'] == 'Available'])
        st.metric("Available Equipment", available_count)
    
    with col2:
        in_use_count = len(tools_df[tools_df['Status'] == 'In Use'])
        st.metric("Equipment In Use", in_use_count)
    
    with col3:
        maintenance_count = len(tools_df[tools_df['Status'] == 'Maintenance'])
        st.metric("Under Maintenance", maintenance_count)
    
    # Equipment table
    st.subheader("Equipment Inventory")
    
    # Category filter
    category_filter = st.selectbox("Filter by Category", ["All"] + list(tools_df['Category'].unique()))
    
    filtered_tools = tools_df.copy()
    if category_filter != "All":
        filtered_tools = filtered_tools[filtered_tools['Category'] == category_filter]
    
    st.dataframe(filtered_tools, use_container_width=True)
    
    # Equipment status chart
    st.subheader("Equipment Status Distribution")
    status_counts = tools_df['Status'].value_counts()
    fig = px.bar(x=status_counts.index, y=status_counts.values,
                color=status_counts.index,
                color_discrete_map={'Available': '#2ecc71', 'In Use': '#f39c12', 'Maintenance': '#e74c3c', 'Scheduled': '#3498db'})
    st.plotly_chart(fig, use_container_width=True)

# Logistics Page
elif page == "Logistics":
    st.header("🚁 Logistics & Marine Operations")
    
    # Bed space management
    st.subheader("Accommodation Status")
    
    for _, platform in bed_space_df.iterrows():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{platform['Platform']}**")
        with col2:
            st.metric("Total Beds", platform['Total_Beds'])
        with col3:
            st.metric("Occupied", platform['Occupied_Beds'])
        with col4:
            st.metric("Available", platform['Available_Beds'])
        
        # Progress bar for occupancy
        occupancy_rate = platform['Occupied_Beds'] / platform['Total_Beds']
        st.progress(occupancy_rate)
        st.write(f"Occupancy: {occupancy_rate:.1%} | {platform['Forecast_Change']}")
        st.write("---")
    
    # Weather and marine conditions
    st.subheader("🌊 Marine & Weather Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Conditions**")
        st.write("- Wave Height: 1.2m")
        st.write("- Wind Speed: 15 knots")
        st.write("- Visibility: 8 km")
        st.write("- Sea State: Slight")
        
    with col2:
        st.write("**7-Day Forecast**")
        st.write("- Day 1-3: Good conditions")
        st.write("- Day 4-5: Marginal (2.5m waves)")
        st.write("- Day 6-7: Poor (3.5m waves)")
        st.write("- Recommended work window: Next 3 days")
    
    # Helicopter schedule
    st.subheader("🚁 Helicopter Schedule")
    heli_schedule = pd.DataFrame({
        'Flight': ['H1-Morning', 'H1-Afternoon', 'H2-Morning', 'H2-Afternoon'],
        'Route': ['Shore-Alpha-Beta', 'Beta-Alpha-Shore', 'Shore-Gamma', 'Gamma-Shore'],
        'Capacity': ['12/14', '8/14', '10/12', '6/12'],
        'Status': ['On Time', 'Delayed 30min', 'On Time', 'On Time']
    })
    st.dataframe(heli_schedule, use_container_width=True)

# Work Disciplines Page
elif page == "Work Disciplines":
    st.header("👷 Work Disciplines & Personnel")
    
    # Personnel overview
    st.subheader("Personnel Availability by Discipline")
    
    # Calculate availability percentage
    disciplines_df['Availability_%'] = (disciplines_df['Current_Available'] / disciplines_df['Personnel_Required'] * 100).round(1)
    
    # Display as metrics
    for _, discipline in disciplines_df.iterrows():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{discipline['Discipline']}**")
        with col2:
            st.metric("Required", discipline['Personnel_Required'])
        with col3:
            st.metric("Available", discipline['Current_Available'])
        with col4:
            availability = discipline['Availability_%']
            color = "🟢" if availability >= 90 else "🟡" if availability >= 70 else "🔴"
            st.metric("Availability", f"{availability}% {color}")
        
        st.write(f"Certification Level: {discipline['Certification_Level']}")
        st.write("---")
    
    # Skills matrix
    st.subheader("Skills & Certifications Matrix")
    skills_data = pd.DataFrame({
        'Personnel': ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'Tom Davis'],
        'Well Control': ['Level 4', 'Level 3', 'Level 4', 'Level 2', 'Level 3'],
        'Subsea': ['Level 3', 'Level 4', 'Level 2', 'Level 4', 'Level 1'],
        'HSE': ['Level 5', 'Level 4', 'Level 3', 'Level 5', 'Level 4'],
        'Availability': ['Available', 'On Job', 'Available', 'Training', 'Available']
    })
    st.dataframe(skills_data, use_container_width=True)

# Well History Page
elif page == "Well History":
    st.header("📋 Well History & Documentation")
    
    # Select well for history
    selected_well = st.selectbox("Select Well", wells_df['Well_ID'].tolist())
    
    if selected_well:
        st.subheader(f"History for {selected_well}")
        
        # Intervention history
        intervention_history = pd.DataFrame({
            'Date': ['2025-01-12', '2024-11-15', '2024-08-22', '2024-05-10', '2024-02-18'],
            'Intervention_Type': ['Valve Maintenance', 'Routine PM', 'Valve Replacement', 'Logging Run', 'Stimulation'],
            'Duration_Days': [2, 1, 4, 1, 3],
            'Cost_USD': [45000, 15000, 85000, 25000, 120000],
            'Outcome': ['Successful', 'Successful', 'Successful', 'Successful', 'Partial Success'],
            'Notes': ['Swab valve repaired', 'Standard PM completed', 'Master valve replaced', 'Production log acquired', 'Acid treatment - partial response']
        })
        
        st.dataframe(intervention_history, use_container_width=True)
        
        # Production trend
        st.subheader("Production Trend")
        dates = pd.date_range(start='2024-01-01', end='2025-01-24', freq='W')
        production = 1200 + np.random.normal(0, 100, len(dates))
        production = np.maximum(production, 0)  # Ensure non-negative
        
        fig = px.line(x=dates, y=production, title=f"{selected_well} Production History")
        fig.update_xaxis(title="Date")
        fig.update_yaxis(title="Production Rate (bbl/day)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Documents
        st.subheader("Related Documents")
        documents = [
            "Well Completion Report.pdf",
            "Last Intervention Report.pdf",
            "Valve Test Certificates.pdf",
            "Production Data.xlsx",
            "Well Schematic.dwg"
        ]
        
        for doc in documents:
            st.write(f"📄 {doc}")

# Integrity Management Page
elif page == "Integrity Management":
    st.header("🔍 Integrity Management")
    
    # Valve test status
    st.subheader("Valve Test Status")
    
    valve_tests = wells_df[['Well_ID', 'Master_Valve', 'Swab_Valve', 'Wing_Valve', 'Integrity_Issues']].copy()
    
    # Color code the valve status
    def color_valve_status(val):
        if val == 'Pass':
            return 'background-color: #d4edda; color: #155724'
        elif val == 'Fail':
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    styled_valve_tests = valve_tests.style.applymap(color_valve_status, subset=['Master_Valve', 'Swab_Valve', 'Wing_Valve'])
    st.dataframe(styled_valve_tests, use_container_width=True)
    
    # Integrity issues summary
    st.subheader("🚨 Active Integrity Issues")
    
    issues = wells_df[wells_df['Integrity_Issues'] != 'None'][['Well_ID', 'Integrity_Issues', 'Priority']].copy()
    
    for _, issue in issues.iterrows():
        priority_color = {"Critical": "#e74c3c", "High": "#f39c12", "Medium": "#f1c40f", "Low": "#2ecc71"}
        st.markdown(f"""
        <div style="border-left: 4px solid {priority_color[issue['Priority']]}; padding: 10px; margin: 5px 0; background-color: #f8f9fa;">
            <strong>{issue['Well_ID']}</strong>: {issue['Integrity_Issues']} 
            <span style="background-color: {priority_color[issue['Priority']]}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.8em;">{issue['Priority']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Preventive maintenance schedule
    st.subheader("📅 Preventive Maintenance Schedule")
    
    pm_schedule = wells_df[['Well_ID', 'Next_PM_Due', 'Status']].copy()
    pm_schedule['Days_Until_PM'] = (pd.to_datetime(pm_schedule['Next_PM_Due']) - datetime.datetime.now()).dt.days
    pm_schedule = pm_schedule.sort_values('Days_Until_PM')
    
    st.dataframe(pm_schedule, use_container_width=True)

# Well-Wizard Training Field Page
elif page == "Well-Wizard Training Field":
    st.header("🧑‍🏫 Well-Wizard Training Field")
    
    st.markdown('<div class="training-card"><h2>Welcome to the Well-Wizard Training Field!</h2><p>Enhance your well intervention skills with interactive training modules, quizzes, and simulations.</p></div>', unsafe_allow_html=True)
    
    # Training modules
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📚 Training Modules")
        
        modules = [
            "Well Control Fundamentals",
            "Valve Testing Procedures",
            "Intervention Planning",
            "Safety Protocols",
            "Equipment Operation",
            "Emergency Response"
        ]
        
        for module in modules:
            if st.button(f"Start: {module}"):
                st.success(f"Starting {module} training module...")
                st.info("This would launch an interactive training session in a full implementation.")
    
    with col2:
        st.subheader("🧠 Quick Quiz")
        
        st.write("**Question 1:** What is the maximum allowable pressure for a standard wellhead valve test?")
        q1_answer = st.radio("Select answer:", ["1000 psi", "1500 psi", "2000 psi", "2500 psi"], key="q1")
        
        st.write("**Question 2:** How often should master valve testing be performed?")
        q2_answer = st.radio("Select answer:", ["Monthly", "Quarterly", "Semi-annually", "Annually"], key="q2")
        
        if st.button("Submit Quiz"):
            score = 0
            if q1_answer == "1500 psi":
                score += 1
            if q2_answer == "Semi-annually":
                score += 1
            
            st.write(f"Your score: {score}/2")
            if score == 2:
                st.success("Perfect! You have excellent knowledge of well control procedures.")
            elif score == 1:
                st.warning("Good job! Review the training materials for areas of improvement.")
            else:
                st.error("Please review the training modules and try again.")
    
    # Simulation section
    st.subheader("🎮 Well Intervention Simulator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Scenario 1: Valve Failure**")
        if st.button("Start Simulation 1"):
            st.info("Simulating valve failure scenario...")
            st.write("A master valve has failed during routine testing. What is your response?")
    
    with col2:
        st.write("**Scenario 2: Emergency Shutdown**")
        if st.button("Start Simulation 2"):
            st.info("Simulating emergency shutdown...")
            st.write("Pressure anomaly detected. Initiate emergency procedures.")
    
    with col3:
        st.write("**Scenario 3: Equipment Malfunction**")
        if st.button("Start Simulation 3"):
            st.info("Simulating equipment malfunction...")
            st.write("Wireline unit malfunction during intervention. Assess and respond.")
    
    # Progress tracking
    st.subheader("📈 Your Training Progress")
    
    progress_data = {
        'Module': ['Well Control', 'Valve Testing', 'Safety Protocols', 'Equipment Operation'],
        'Progress': [85, 92, 78, 65],
        'Status': ['In Progress', 'Completed', 'In Progress', 'Not Started']
    }
    
    progress_df = pd.DataFrame(progress_data)
    
    for _, row in progress_df.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{row['Module']}**")
            st.progress(row['Progress'] / 100)
        with col2:
            st.write(f"{row['Progress']}%")
        with col3:
            status_color = {"Completed": "🟢", "In Progress": "🟡", "Not Started": "🔴"}
            st.write(f"{status_color.get(row['Status'], '⚪')} {row['Status']}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🧙‍♂️ Well Wizard - Intervention Planning System v3.0 | Powered by Streamlit</p>
    <p>For support, contact: engineering@company.com | Last updated: 2025-01-24</p>
</div>
""", unsafe_allow_html=True)
```

---

## **How to Upload This to GitHub:**

1. **Copy the entire code above.**
2. **Go to your GitHub repository.**
3. **Click on `well_intervention_app.py` (or whatever your main file is called).**
4. **Click the pencil icon (✏️) to edit.**
5. **Delete all the old code and paste this new code.**
6. **Scroll down and click "Commit changes".**
7. **Wait 1-2 minutes for Streamlit Cloud to update.**

**Your app will now have the "Well-Wizard Training Field" page with interactive training modules, quizzes, and simulations!**