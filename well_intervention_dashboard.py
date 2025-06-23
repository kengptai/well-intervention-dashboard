# -*- coding: utf-8 -*-

import streamlit as

import pandas as pd

import numpy as np

import plotly.express as px

import plotly.graph_objects as go

from plotly.subplots import make_subplots

from datetime import datetime, timedelta

import warnings

warnings.filterwarnings('ignore')


st.set_page_config(

    page_title="Well Intervention AI Dashboard",

    page_icon="🛢️",

    layout="wide",

    initial_sidebar_state="expanded"

)


st.markdown("""

<style>

    .main-header {

        font-size: 2.5rem;

        font-weight: bold;

        color: #1f4e79;

        text-align: center;

        margin-bottom: 2rem;

    }

    .metric-card {

        background-color: #f0f2f6;

        padding: 1rem;

        border-radius: 0.5rem;

        border-left: 4px solid #1f4e79;

    }

    .success-metric {

        border-left-color: #28a745;

    }

    .warning-metric {

        border-left-color: #ffc107;

    }

    .danger-metric {

        border-left-color: #dc3545;

    }

</style>

""", unsafe_allow_html=True)


@st.cache_data

def load_sample_data():

    np.random.seed(42)

    n_records = 500

    well_data = {

        'well_id': [f'WELL_{i:03d}' for i in range(1, n_records + 1)],

        'field': np.random.choice(['North Sea Alpha', 'North Sea Beta', 'North Sea Gamma'], n_records),

        'intervention_type': np.random.choice(['Wireline', 'Coiled Tubing', 'Workover', 'ESP Install'], n_records),

        'well_age_years': np.random.normal(15, 8, n_records).clip(1, 40),

        'depth_ft': np.random.normal(12000, 3000, n_records).clip(5000, 25000),

        'pressure_psi': np.random.normal(4500, 1200, n_records).clip(1000, 8000),

        'temperature_f': np.random.normal(180, 40, n_records).clip(80, 300),

        'water_cut_percent': np.random.beta(2, 5, n_records) * 100,

        'last_intervention_days': np.random.exponential(365, n_records).clip(30, 2000),

        'tool_condition_score': np.random.normal(7.5, 1.5, n_records).clip(1, 10),

        'weather_condition': np.random.choice(['Good', 'Moderate', 'Poor'], n_records, p=[0.6, 0.3, 0.1]),

        'crew_experience_years': np.random.normal(12, 5, n_records).clip(2, 30),

        'intervention_date': [datetime.now() - timedelta(days=int(x)) for x in np.random.exponential(180, n_records)],

    }

    success_prob = (

        0.9 -

        (well_data['well_age_years'] - 10) * 0.01 +

        (well_data['tool_condition_score'] - 5) * 0.05 +

        (well_data['crew_experience_years'] - 10) * 0.01 +

        np.where(well_data['weather_condition'] == 'Poor', -0.15, 0) +

        np.where(well_data['intervention_type'] == 'Workover', -0.1, 0) +

        np.random.normal(0, 0.1, n_records)

    ).clip(0.1, 0.95)

    well_data['success_probability'] = success_prob

    well_data['predicted_success'] = success_prob > 0.7

    well_data['actual_success'] = np.random.binomial(1, success_prob, n_records).astype(bool)

    base_npt = np.where(well_data['actual_success'],

                       np.random.exponential(8, n_records),

                       np.random.exponential(24, n_records))

    well_data['predicted_npt_hours'] = base_npt.clip(0, 72)

    base_cost = 50000 + well_data['depth_ft'] * 2 + well_data['predicted_npt_hours'] * 5000

    well_data['estimated_cost_usd'] = base_cost + np.random.normal(0, 10000, n_records)

    return pd.DataFrame(well_data)


df = load_sample_data()


st.markdown('<h1 class="main-header">🛢️ Well Intervention AI Dashboard</h1>', unsafe_allow_html=True)

st.markdown("**Predictive Analytics for Smarter, Safer Well Interventions**")


# Sidebar for filters

st.sidebar.header("🔧 Intervention Filters")

selected_fields = st.sidebar.multiselect("Select Fields", df['field'].unique(), default=df['field'].unique())

selected_types = st.sidebar.multiselect("Intervention Types", df['intervention_type'].unique(), default=df['intervention_type'].unique())

success_threshold = st.sidebar.slider("Success Probability Threshold", 0.0, 1.0, 0.7, 0.05)


filtered_df = df[

    (df['field'].isin(selected_fields)) & 

    (df['intervention_type'].isin(selected_types))

]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown('<div class="metric-card success-metric">', unsafe_allow_html=True)

    high_success_count = len(filtered_df[filtered_df['success_probability'] >= success_threshold])

    st.metric("High Success Probability", f"{high_success_count}", f"{high_success_count/len(filtered_df)*100:.1f}%")

    st.markdown('</div>', unsafe_allow_html=True)


with col2:

    st.markdown('<div class="metric-card warning-metric">', unsafe_allow_html=True)

    avg_npt = filtered_df['predicted_npt_hours'].mean()

    st.metric("Avg Predicted NPT", f"{avg_npt:.1f} hrs", f"${avg_npt*5000:,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)


with col3:

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)

    avg_cost = filtered_df['estimated_cost_usd'].mean()

    st.metric("Avg Intervention Cost", f"${avg_cost:,.0f}", f"±${filtered_df['estimated_cost_usd'].std():,.0f}")

    st.markdown('</div>', unsafe_allow_html=True)


with col4:

    st.markdown('<div class="metric-card danger-metric">', unsafe_allow_html=True)

    risk_count = len(filtered_df[filtered_df['success_probability'] < 0.5])

    st.metric("High Risk Interventions", f"{risk_count}", f"{risk_count/len(filtered_df)*100:.1f}%")

    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("---")


col1, col2 = st.columns(2)


with col1:

    st.subheader("📊 Success Probability Distribution")

    fig_hist = px.histogram(

        filtered_df, 

        x='success_probability', 

        nbins=20,

        title="Distribution of Intervention Success Probabilities",

        color_discrete_sequence=['#1f4e79']

    )

    fig_hist.add_vline(x=success_threshold, line_dash="dash", line_color="red", 

                      annotation_text=f"Threshold: {success_threshold}")

    st.plotly_chart(fig_hist, use_container_width=True)


with col2:

    st.subheader("⚠️ Risk Factors Analysis")

    risk_factors = filtered_df.groupby('intervention_type').agg({

        'success_probability': 'mean',

        'predicted_npt_hours': 'mean',

        'estimated_cost_usd': 'mean'

    }).round(2)

    fig_risk = px.scatter(

        risk_factors.reset_index(),

        x='predicted_npt_hours',

        y='success_probability',

        size='estimated_cost_usd',

        color='intervention_type',

        title="Risk vs NPT by Intervention Type",

        labels={'predicted_npt_hours': 'Predicted NPT (hours)', 

                'success_probability': 'Success Probability'}

    )

    st.plotly_chart(fig_risk, use_container_width=True)


col1, col2 = st.columns(2)


with col1:

    st.subheader("📈 Intervention Timeline")

    timeline_data = filtered_df.groupby(filtered_df['intervention_date'].dt.date).size().reset_index()

    timeline_data.columns = ['date', 'count']

    fig_timeline = px.line(

        timeline_data,

        x='date',

        y='count',

        title="Interventions Over Time",

        markers=True

    )

    st.plotly_chart(fig_timeline, use_container_width=True)


with col2:

    st.subheader("🎯 Well Performance Factors")

    fig_factors = make_subplots(

        rows=2, cols=2,

        subplot_titles=('Well Age vs Success', 'Tool Condition vs Success', 

                       'Crew Experience vs Success', 'Weather Impact'),

        specs=[[{"secondary_y": False}, {"secondary_y": False}],

               [{"secondary_y": False}, {"secondary_y": False}]]

    )

    fig_factors.add_trace(

        go.Scatter(x=filtered_df['well_age_years'], y=filtered_df['success_probability'],

                  mode='markers', name='Age vs Success', opacity=0.6),

        row=1, col=1

    )

    fig_factors.add_trace(

        go.Scatter(x=filtered_df['tool_condition_score'], y=filtered_df['success_probability'],

                  mode='markers', name='Tool vs Success', opacity=0.6),

        row=1, col=2

    )

    fig_factors.add_trace(

        go.Scatter(x=filtered_df['crew_experience_years'], y=filtered_df['success_probability'],

                  mode='markers', name='Experience vs Success', opacity=0.6),

        row=2, col=1

    )

    weather_impact = filtered_df.groupby('weather_condition')['success_probability'].mean()

    fig_factors.add_trace(

        go.Bar(x=weather_impact.index, y=weather_impact.values, name='Weather Impact'),

        row=2, col=2

    )

    fig_factors.update_layout(height=500, showlegend=False, title_text="Performance Factor Analysis")

    st.plotly_chart(fig_factors, use_container_width=True)


st.markdown("---")

st.subheader("🎯 Intervention Planning Assistant")


col1, col2 = st.columns([1, 2])


with col1:

    st.markdown("**Plan New Intervention**")

    new_well_field = st.selectbox("Field", df['field'].unique())

    new_intervention_type = st.selectbox("Intervention Type", df['intervention_type'].unique())

    new_well_age = st.slider("Well Age (years)", 1, 40, 15)

    new_depth = st.slider("Depth (ft)", 5000, 25000, 12000, 500)

    new_tool_condition = st.slider("Tool Condition Score", 1.0, 10.0, 7.5, 0.5)

    new_crew_experience = st.slider("Crew Experience (years)", 2, 30, 12)

    new_weather = st.selectbox("Weather Condition", ['Good', 'Moderate', 'Poor'])

    if st.button("🔮 Predict Intervention Outcome", type="primary"):

        base_success = 0.8

        age_factor = max(0, (15 - new_well_age) * 0.01)

        tool_factor = (new_tool_condition - 5) * 0.05

        crew_factor = (new_crew_experience - 10) * 0.01

        weather_factor = {'Good': 0, 'Moderate': -0.05, 'Poor': -0.15}[new_weather]

        type_factor = {'Workover': -0.1, 'Wireline': 0.05, 'Coiled Tubing': 0, 'ESP Install': -0.05}[new_intervention_type]

        predicted_success = min(0.95, max(0.1, base_success + age_factor + tool_factor + crew_factor + weather_factor + type_factor))

        predicted_npt = max(2, 12 - (predicted_success - 0.5) * 20 + np.random.normal(0, 2))

        predicted_cost = 50000 + new_depth * 2 + predicted_npt * 5000

        st.session_state.prediction_results = {

            'success': predicted_success,

            'npt': predicted_npt,

            'cost': predicted_cost

        }


with col2:

    if 'prediction_results' in st.session_state:

        results = st.session_state.prediction_results

        st.markdown("**🎯 Prediction Results**")

        fig_gauge = go.Figure(go.Indicator(

            mode = "gauge+number+delta",

            value = results['success'] * 100,

            domain = {'x': [0, 1], 'y': [0, 1]},

            title = {'text': "Success Probability (%)"},

            delta = {'reference': 70},

            gauge = {

                'axis': {'range': [None, 100]},

                'bar': {'color': "darkblue"},

                'steps': [

                    {'range': [0, 50], 'color': "lightgray"},

                    {'range': [50, 70], 'color': "yellow"},

                    {'range': [70, 100], 'color': "lightgreen"}],

                'threshold': {

                    'line': {'color': "red", 'width': 4},

                    'thickness': 0.75,

                    'value': 70}}))

        fig_gauge.update_layout(height=300)

        st.plotly_chart(fig_gauge, use_container_width=True)

        col_a, col_b = st.columns(2)

        with col_a:

            st.metric("Predicted NPT", f"{results['npt']:.1f} hours")

        with col_b:

            st.metric("Estimated Cost", f"${results['cost']:,.0f}")

        st.markdown("**💡 AI Recommendations:**")

        if results['success'] > 0.8:

            st.success("✅ High probability of success. Proceed with confidence.")

        elif results['success'] > 0.6:

            st.warning("⚠️ Moderate risk. Consider additional precautions.")

        else:

            st.error("🚨 High risk intervention. Review plan and consider alternatives.")

        recommendations = []

        if new_tool_condition < 6:

            recommendations.append("🔧 Consider upgrading tool condition before intervention")

        if new_weather == 'Poor':

            recommendations.append("🌦️ Weather conditions may impact success - consider postponing")

        if new_crew_experience < 8:

            recommendations.append("👥 Consider adding experienced crew member")

        if new_well_age > 20:

            recommendations.append("⏰ Older well - extra caution with wellbore integrity")

        for rec in recommendations:

            st.info(rec)


st.markdown("---")

st.subheader("📋 Intervention Records")


col1, col2, col3 = st.columns(3)

with col1:

    show_high_risk = st.checkbox("Show High Risk Only (< 50% success)")

with col2:

    show_recent = st.checkbox("Show Recent Only (last 90 days)")

with col3:

    sort_by = st.selectbox("Sort by", ['intervention_date', 'success_probability', 'predicted_npt_hours', 'estimated_cost_usd'])


display_df = filtered_df.copy()

if show_high_risk:

    display_df = display_df[display_df['success_probability'] < 0.5]

if show_recent:

    recent_date = datetime.now() - timedelta(days=90)

    display_df = display_df[display_df['intervention_date'] >= recent_date]


display_df = display_df.sort_values(sort_by, ascending=False)


display_columns = [

    'well_id', 'field', 'intervention_type', 'success_probability', 

    'predicted_npt_hours', 'estimated_cost_usd', 'intervention_date'

]


formatted_df = display_df[display_columns].copy()

formatted_df['success_probability'] = formatted_df['success_probability'].apply(lambda x: f"{x:.1%}")

formatted_df['predicted_npt_hours'] = formatted_df['predicted_npt_hours'].apply(lambda x: f"{x:.1f}")

formatted_df['estimated_cost_usd'] = formatted_df['estimated_cost_usd'].apply(lambda x: f"${x:,.0f}")

formatted_df['intervention_date'] = formatted_df['intervention_date'].dt.strftime('%Y-%m-%d')


st.dataframe(

    formatted_df,

    use_container_width=True,

    column_config={

        "well_id": "Well ID",

        "field": "Field",

        "intervention_type": "Type",

        "success_probability": "Success %",

        "predicted_npt_hours": "NPT (hrs)",

        "estimated_cost_usd": "Cost",

        "intervention_date": "Date"

    }

)


st.markdown("---")

st.markdown("""

<div style='text-align: center; color: #666; padding: 20px;'>

    <p><strong>Well Intervention AI Dashboard</strong> | Powered by 25 years of North Sea expertise + AI</p>

    <p>🛢️ Predictive Analytics • 📊 Real-time Insights • 🎯 Optimized Planning</p>

</div>

""", unsafe_allow_html=True)


