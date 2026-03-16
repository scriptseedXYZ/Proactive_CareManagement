import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- Configuration ---
st.set_page_config(page_title="CarePredict Prototype", layout="wide", initial_sidebar_state="collapsed")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .patient-header { font-size: 24px; font-weight: bold; margin-bottom: 0px; }
    .patient-sub { color: #666; font-size: 14px; margin-top: -10px; margin-bottom: 15px; }
    .risk-badge { background-color: #ffebee; color: #d32f2f; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; vertical-align: middle; margin-left: 10px;}
    .big-score-circle { border: 3px solid #d32f2f; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: #d32f2f; float: right;}
    .alert-box { border: 1px solid #ffcdd2; background-color: #fff9f9; border-radius: 8px; padding: 15px; margin-bottom: 20px; }
    .alert-title { color: #d32f2f; font-weight: 600; margin-bottom: 10px; font-size: 14px; }
    .alert-tag { border: 1px solid #ef9a9a; color: #d32f2f; padding: 4px 12px; border-radius: 16px; font-size: 12px; background-color: white; margin-right: 8px; display: inline-block; margin-bottom: 5px;}
    .condition-tag { border: 1px solid #e0e0e0; color: #333; padding: 4px 12px; border-radius: 16px; font-size: 12px; background-color: #f5f5f5; margin-right: 8px; display: inline-block; margin-bottom: 5px;}
    .metric-red { color: #d32f2f; font-weight: bold; float: right; }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# --- Mock Data ---
MOCK_PATIENTS = [
    {
        "id": "P-10042", "name": "Margaret Chen", "age": 72, "gender": "F",
        "risk_score": 92, "risk_level": "Critical", "conditions": ["CHF", "Type 2 Diabetes", "CKD Stage 3"],
        "missed_meds": 8, "missed_appts": 3, "ed_visits": 2, "trend": "+14",
        "history": [55, 58, 62, 68, 71, 78, 83, 85, 88, 90, 88, 92],
        "mbr": "MBR-88421"
    },
    {
        "id": "P-10087", "name": "James Rodriguez", "age": 65, "gender": "M",
        "risk_score": 84, "risk_level": "Critical", "conditions": ["COPD", "Hypertension"],
        "missed_meds": 5, "missed_appts": 2, "ed_visits": 1, "trend": "+9",
        "history": [60, 62, 65, 68, 70, 75, 78, 80, 82, 83, 84, 84],
        "mbr": "MBR-88422"
    },
    {
        "id": "P-10156", "name": "Dorothy Williams", "age": 78, "gender": "F",
        "risk_score": 71, "risk_level": "High", "conditions": ["Atrial Fibrillation", "Osteoporosis"],
        "missed_meds": 4, "missed_appts": 1, "ed_visits": 0, "trend": "+6",
        "history": [50, 52, 55, 58, 60, 62, 65, 67, 68, 70, 71, 71],
        "mbr": "MBR-88423"
    }
]

# --- AI / ML Mock Functions ---
def get_ml_risk_prediction(patient):
    prob = min(99, patient['risk_score'] + random.randint(-5, 10))
    return f"**{prob}%** probability of ED visit in next 30 days."

def get_genai_clinical_insight(patient):
    return f"AI Insight: {patient['name']} shows a highly concerning pattern. Immediate outreach is recommended to verify medication access and schedule a telehealth follow-up."

# --- Helper Function for Custom Progress Bars ---
def custom_progress_bar(label, percentage, color, subtext, icon=""):
    html = f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="font-weight: 600; font-size: 14px; color: #333;">{label} {icon}</span>
            <span style="font-weight: 600; font-size: 14px; color: #333;">{percentage}%</span>
        </div>
        <div style="width: 100%; background-color: #f0f0f0; border-radius: 4px; height: 8px;">
            <div style="width: {percentage}%; background-color: {color}; height: 100%; border-radius: 4px;"></div>
        </div>
        <div style="font-size: 12px; color: #666; margin-top: 5px;">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- UI Components ---
def render_dashboard():
    st.title("🛡️ CarePredict")
    st.caption("AI-Powered Risk Intelligence | Model updated 2h ago")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("TOTAL CASELOAD", "8", "2 critical, 2 high", delta_color="off")
    col2.metric("AVG RISK SCORE", "54", "+3 from last month", delta_color="inverse")
    col3.metric("PENDING ACTIONS", "12", "4 patients need attention", delta_color="off")
    col4.metric("OVERDUE FOLLOW-UPS", "3", "Requires immediate outreach", delta_color="inverse")
    
    st.divider()
    
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("Risk Distribution")
        labels, values = ['Critical', 'High', 'Moderate', 'Low'], [2, 2, 2, 2]
        fig = px.pie(values=values, names=labels, hole=0.6, color=labels, 
                     color_discrete_map={'Critical':'#d32f2f', 'High':'#f57c00', 'Moderate':'#fbc02d', 'Low':'#388e3c'})
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
    with chart_col2:
        st.subheader("Caseload Risk Trend")
        months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        fig2 = go.Figure(data=[
            go.Bar(name='Critical', x=months, y=[1, 1, 2, 2, 2, 2], marker_color='#d32f2f'),
            go.Bar(name='High', x=months, y=[1, 2, 2, 2, 3, 2], marker_color='#f57c00'),
            go.Bar(name='Moderate', x=months, y=[3, 2, 2, 2, 1, 2], marker_color='#fbc02d'),
            go.Bar(name='Low', x=months, y=[3, 3, 2, 2, 2, 2], marker_color='#388e3c')
        ])
        fig2.update_layout(barmode='stack', margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Priority Case Queue")
    for p in MOCK_PATIENTS:
        with st.container(border=True):
            cols = st.columns([1, 4, 2, 2, 2, 1])
            cols[0].markdown(f"### 🔴 {p['risk_score']}" if p['risk_level'] == 'Critical' else f"### 🟠 {p['risk_score']}")
            cols[1].markdown(f"**{p['name']}** <span class='risk-badge'>{p['risk_level']}</span><br><span style='font-size:12px; color:#666;'>{p['age']}{p['gender']} • {p['id']} • {', '.join(p['conditions'])}</span>", unsafe_allow_html=True)
            cols[2].metric("Missed Meds", p['missed_meds'])
            cols[3].metric("Missed Appts", p['missed_appts'])
            cols[4].metric("ED Visits", p['ed_visits'])
            
            if cols[5].button("View", key=p['id']):
                st.session_state.selected_patient = p
                st.session_state.page = 'patient_detail'
                st.rerun()

def render_patient_detail():
    p = st.session_state.selected_patient
    
    # Header Area
    col_back, col_space = st.columns([1, 10])
    if col_back.button("←", help="Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.session_state.selected_patient = None
        st.rerun()
        
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.markdown(f"<div class='patient-header'>{p['name']} <span class='risk-badge'>{p['risk_level']}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='patient-sub'>{p['age']}{p['gender']} • {p['id']} • {p['mbr']} • Medicare Advantage</div>", unsafe_allow_html=True)
    with head_col2:
        st.markdown(f"<div class='big-score-circle'>{p['risk_score']}</div>", unsafe_allow_html=True)

    # Action Buttons
    btn_cols = st.columns([1.5, 1.5, 1.5, 1.5, 2, 4])
    btn_cols[0].button("📞 Call Patient", type="primary", use_container_width=True)
    btn_cols[1].button("📅 Schedule Visit", use_container_width=True)
    btn_cols[2].button("💬 Send Message", use_container_width=True)
    btn_cols[3].button("📄 Care Plan", use_container_width=True)
    btn_cols[4].button("👤 Dr. Sarah Williams", use_container_width=True)

    # Active Alerts (With AI insights embedded below tags)
    st.markdown("""
    <div class='alert-box'>
        <div class='alert-title'>⚠️ Active Alerts</div>
        <div class='alert-tag'>CHF exacerbation risk</div>
        <div class='alert-tag'>Medication non-adherence critical</div>
        <div class='alert-tag'>Social isolation flagged</div>
    </div>
    """, unsafe_allow_html=True)
    
    # We still keep the AI models active as requested, just styled differently
    with st.expander("🧠 Assisted AI & ML Insights (Click to Expand)", expanded=True):
        st.markdown(f"**ML Engine:** {get_ml_risk_prediction(p)}")
        st.markdown(f"**GenAI Assessment:** {get_genai_clinical_insight(p)}")

    # Two Column Layout for Breakdown and Trend
    col_left, col_right = st.columns(2)
    
    with col_left:
        with st.container(border=True):
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 20px;'>Risk Factor Breakdown</h4>", unsafe_allow_html=True)
            custom_progress_bar("Medication Adherence", 35, "#f57c00", "Missed 8 of 14 doses this week", "↘")
            custom_progress_bar("Appointment Compliance", 20, "#4caf50", "Missed 3 consecutive cardiology visits", "↘")
            custom_progress_bar("ED Utilization", 85, "#d32f2f", "2 ED visits in past 14 days", "↗")
            custom_progress_bar("Behavioral Signals", 72, "#d32f2f", "Declined refill pickup, not answering calls", "↗")

    with col_right:
        with st.container(border=True):
            st.markdown("<h4 style='font-size: 16px; margin-bottom: 0px;'>12-Month Risk Trend</h4>", unsafe_allow_html=True)
            df = pd.DataFrame({"Month": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], "Score": p['history']})
            fig = px.line(df, x="Month", y="Score", markers=True)
            fig.add_hline(y=85, line_dash="dash", line_color="#d32f2f", annotation_text="Critical Threshold")
            fig.add_hline(y=70, line_dash="dash", line_color="#f57c00", annotation_text="High Risk Threshold")
            fig.update_layout(margin=dict(t=20, b=0, l=0, r=0), height=280, yaxis_range=[0,100], hovermode="x unified")
            fig.update_traces(line_color='#1976d2', marker=dict(size=8, color='#1976d2'))
            st.plotly_chart(fig, use_container_width=True)

    # Bottom Row Cards
    bot_col1, bot_col2, bot_col3 = st.columns(3)
    
    with bot_col1:
        with st.container(border=True):
            st.markdown("<h4 style='font-size: 14px;'>Active Conditions</h4>", unsafe_allow_html=True)
            tags_html = "".join([f"<div class='condition-tag'>{cond}</div>" for cond in p['conditions']])
            st.markdown(tags_html, unsafe_allow_html=True)
            st.write("") # spacing
            
    with bot_col2:
        with st.container(border=True):
            st.markdown("<h4 style='font-size: 14px;'>Contact History</h4>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; margin-bottom:8px;'>Last Contact <span style='float:right; font-weight:600;'>12 days ago</span></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px; margin-bottom:8px;'>Next Appointment <span class='metric-red'>Overdue</span></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size:13px;'>PCP <span style='float:right; font-weight:600;'>Dr. Sarah Williams</span></div>", unsafe_allow_html=True)

    with bot_col3:
        with st.container(border=True):
            st.markdown("<h4 style='font-size: 14px;'>Key Metrics</h4>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px; margin-bottom:8px;'>Missed Medications <span class='metric-red'>{p['missed_meds']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px; margin-bottom:8px;'>Missed Appointments <span class='metric-red'>{p['missed_appts']}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px;'>ED Visits (30d) <span class='metric-red'>{p['ed_visits']}</span></div>", unsafe_allow_html=True)

# --- Router ---
if st.session_state.page == 'dashboard':
    render_dashboard()
elif st.session_state.page == 'patient_detail':
    render_patient_detail()