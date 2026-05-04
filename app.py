import streamlit as st

st.set_page_config(
    page_title="AI Crop System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- REMOVE HEADER + DEPLOY + MENU ----------
st.markdown("""
<style>

/* 🔥 Remove full top header */
header {visibility: hidden;}

/* 🔥 Remove deploy + 3-dot menu */
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {display: none !important;}

/* 🔥 Remove top spacing */
.block-container {
    padding-top: 0rem !important;
}

/* 🔥 Keep same background */
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0b1f33 100%);
}

</style>
""", unsafe_allow_html=True)


# ---------- YOUR ORIGINAL UI (UNCHANGED) ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #07111f 0%, #0b1f33 100%);
}

section[data-testid="stSidebar"] {
    background: #101827;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 58px;
    font-weight: 800;
    color: white;
    margin-bottom: 10px;
}

.subtitle-box {
    background: rgba(255,255,255,0.06);
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 20px;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}

.metric-title {
    font-size: 18px;
    color: #d1d5db;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------- Header ----------
st.markdown(
    '<div class="main-title">🌾 AI Powered Crop Yield and Optimization System</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="subtitle-box">
    <h3 style="color:white;">AI-Based Agricultural  Support System</h3>
    <p style="color:#d1d5db; font-size:18px;">
        Welcome to the modern agri-tech dashboard for crop yield prediction,
        optimization, fertilizer planning, irrigation strategy, and historical analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- KPI Cards ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🤖 AI Modules</div>
        <div class="metric-value">8+</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">📊 Dashboard Pages</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🎯 System Type</div>
        <div class="metric-value">ML + Optimization</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.subheader("🧭 Navigation Guide")
st.write("Use the sidebar to move between Input Form, AI Results, and Historical Analytics.")