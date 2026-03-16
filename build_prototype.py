import os

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def main():
    base_dir = "carepredict_prototype"
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "src"), exist_ok=True)

    # 1. requirements.txt
    reqs = """
streamlit
pandas
plotly
    """
    create_file(os.path.join(base_dir, "requirements.txt"), reqs)

    # 2. README.md
    readme = """
# CarePredict Prototype

This is a workable prototype designed for stakeholder demonstrations. It features a clickable UI built with Streamlit, showcasing patient risk distributions and detailed AI-generated clinical insights.

## Running the Prototype
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run app.py`

## Future Architecture Integration
* **Data Streams:** Mocked data can be replaced by actual data streams (e.g., AWS S3 or AWS Glue) by modifying `src/data_streams.py`.
* **AI Logic:** The placeholder ML and GenAI functions in `app.py` can be routed directly to your RAG pipeline via `src/rag_pipeline.py`.
    """
    create_file(os.path.join(base_dir, "README.md"), readme)

    # 3. app.py (The main Streamlit application)
    app_code = """
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# --- Configuration ---
st.set_page_config(page_title="CarePredict Prototype", layout="wide", initial_sidebar_state="collapsed")

# --- State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None

# --- Mock Data ---
MOCK_PATIENTS = [
    {
        "id": "P-10042", "name": "Margaret Chen", "age": 72, "gender": "F",
        "risk_score": 92, "risk_level": "Critical", "conditions": "CHF, Type 2 Diabetes, CKD Stage 3",
        "missed_meds": 8, "missed_appts": 3, "ed_visits": 2, "trend": "+14",
        "history": [55, 58, 62, 68, 71, 78, 83, 85, 88, 90, 88, 92]
    },
    {
        "id": "P-10087", "name": "James Rodriguez", "age": 65, "gender": "M",
        "risk_score": 84, "risk_level": "Critical", "conditions": "COPD, Hypertension",
        "missed_meds": 5, "missed_appts": 2, "ed_visits": 1, "trend": "+9",
        "history": [60, 62, 65, 68, 70, 75, 78, 80, 82, 83, 84, 84]
    },
    {
        "id": "P-10156", "name": "Dorothy Williams", "age": 78, "gender": "F",
        "risk_score": 71, "risk_level": "High", "conditions": "Atrial Fibrillation, Osteoporosis",
        "missed_meds": 4, "missed_appts": 1, "ed_visits": 0, "trend": "+6",
        "history": [50, 52, 55, 58, 60, 62, 65, 67, 68, 70, 71, 71]
    }
]

# --- AI / ML Mock Functions ---
def get_ml_risk_prediction(patient):
    prob = min(99, patient['risk_score'] + random.randint(-5, 10))
    return f"**{prob}%** probability of ED visit in the next 30 days based on recent adherence drop."

def get_genai_clinical_insight(patient):
    insights = {
        "Critical": f"AI Insight: {patient['name']} shows a highly concerning pattern. The combination of {patient['missed_meds']} missed medications and {patient['ed_visits']} recent ED visits strongly suggests an exacerbation of {patient['conditions'].split(',')[0]}. Immediate outreach is recommended.",
        "High": f"AI Insight: Moderate deterioration detected for {patient['name']}. Missed appointments indicate a potential barrier to care. Recommend a check-in call.",
    }
    return insights.get(patient['risk_level'], "Routine monitoring recommended.")

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
            cols[1].markdown(f"**{p['name']}** `{p['risk_level']}`  \\n{p['age']}{p['gender']} • {p['id']} • {p['conditions']}")
            cols[2].metric("Missed Meds", p['missed_meds'])
            cols[3].metric("Missed Appts", p['missed_appts'])
            cols[4].metric("ED Visits", p['ed_visits'])
            
            if cols[5].button("View", key=p['id']):
                st.session_state.selected_patient = p
                st.session_state.page = 'patient_detail'
                st.rerun()

def render_patient_detail():
    p = st.session_state.selected_patient
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.session_state.selected_patient = None
        st.rerun()

    st.title(f"{p['name']} `{p['risk_level']}`")
    st.caption(f"{p['age']}{p['gender']} • {p['id']} • Medicare Advantage")
    st.markdown("---")
    
    st.subheader("🧠 AI / ML Patient Insights")
    ml_col, ai_col = st.columns([1, 2])
    with ml_col:
        st.info(f"**ML Prediction:** {get_ml_risk_prediction(p)}")
    with ai_col:
        st.warning(get_genai_clinical_insight(p))
        
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Risk Factor Breakdown")
        st.progress(35, text="Medication Adherence (Missed 8 of 14 doses)")
        st.progress(85, text="ED Utilization (2 ED visits in past 14 days)")

    with col2:
        st.subheader("12-Month Risk Trend")
        df = pd.DataFrame({"Month": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], "Score": p['history']})
        fig = px.line(df, x="Month", y="Score", markers=True)
        fig.add_hline(y=85, line_dash="dash", line_color="red")
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
        st.plotly_chart(fig, use_container_width=True)

# --- Router ---
if st.session_state.page == 'dashboard':
    render_dashboard()
elif st.session_state.page == 'patient_detail':
    render_patient_detail()
    """
    create_file(os.path.join(base_dir, "app.py"), app_code)

    # 4. Placeholder logic files for Gen AI architecture
    create_file(os.path.join(base_dir, "src", "rag_pipeline.py"), "# Placeholder for connecting to the vector database and LLM generation.")
    create_file(os.path.join(base_dir, "src", "data_streams.py"), "# Placeholder for AWS data stream ingestion and parsing.")

    print(f"✅ Success! Your prototype package has been generated in the '{base_dir}' directory.")
    print(f"Navigate to it using: cd {base_dir}")
    print(f"Then run: streamlit run app.py")

if __name__ == "__main__":
    main()