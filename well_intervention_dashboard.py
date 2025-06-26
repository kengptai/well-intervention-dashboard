import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import datetime

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
    bed_space_data = {
        'Platform': ['Platform_Alpha', 'Platform_Beta', 'Platform_Gamma'],
        'Total_Beds': [20, 15, 25],
        'Occupied_Beds': [12, 5, 18],
        'Available_Beds': [8, 10, 7],
        'Forecast_Change': ['+2 next week', '-3 next week', '+1 next week']
    }
    disciplines_data = {
        'Discipline': ['Well Services', 'Subsea Engineering', 'Production Technology', 'Logistics & Marine', 
                      'HSE', 'Instrumentation & Controls', 'Drilling', 'Completions'],
        'Personnel_Required': [15, 8, 12, 6, 4, 10, 20, 14],
        'Current_Available': [12, 8, 10, 5, 4, 8, 18, 12],
        'Certification_Level': ['Level 3', 'Level 4', 'Level 3', 'Level 2', 'Level 5', 'Level 3', 'Level 4', 'Level 3']
    }
    return pd.DataFrame(wells_data), pd.DataFrame(tools_data), pd.DataFrame(bed_space_data), pd.DataFrame(disciplines_data)

wells_df, tools_df, bed_space_df, disciplines_df = generate_sample_data()

# Sidebar navigation
st.sidebar.title("🛢️ Navigation")
page = st.sidebar.selectbox("Select Page", [
    "Dashboard", "Wells Management", "Scheduling & Planning", "Tools & Equipment", 
    "Logistics", "Work Disciplines", "Well History", "Integrity Management"
])

st.markdown('<h1 class="main-header">Well Intervention Planning System</h1>', unsafe_allow_html=True)

# (The rest of your app code goes here: all the page logic, charts, tables, etc.)
# For brevity, you can paste the rest of your app code here as needed.

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>Well Intervention Planning System v2.0 | Powered by Streamlit</p>
    <p>For support, contact: engineering@company.com | Last updated: 2025-01-24</p>
</div>
""", unsafe_allow_html=True)