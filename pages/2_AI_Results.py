import streamlit as st
from database.db import create_tables, insert_record
from src.predict_model import predict_crop_yield
from src.farmer_advisor import farmer_based_recommendation
from src.recommendation import recommend_seed_and_month
from src.market_price import estimate_profit
from src.fertilizer_optimizer import fertilizer_recommendation
from src.irrigation_optimizer import irrigation_plan

st.markdown("""
<style>

/* Remove header */
header {visibility: hidden;}

/* Remove deploy + 3 dot */
[data-testid="stToolbar"] {display: none !important;}
#MainMenu {display: none !important;}

/* Remove top gap */
.block-container {
    padding-top: 0rem !important;
}

/* Keep background same */
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0b1f33 100%);
}

</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Results Dashboard")

st.markdown("""
<style>
.card {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
.metric {
    font-size: 22px;
    font-weight: bold;
    color: #22c55e;
}
.label {
    color: #9ca3af;
    font-size: 14px;
}
.section-title {
    font-size: 20px;
    margin-top: 25px;
    margin-bottom: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB Setup
# =========================
create_tables()

# =========================
# Check Input
# =========================
if "input_data" not in st.session_state:
    st.warning("Please fill input form first")
    st.stop()

data = st.session_state["input_data"]

# =========================
# Crop Recommendation
# =========================
crop = farmer_based_recommendation(
    data["irrigation"],
    data["budget"]
)

# =========================
# Seed Recommendation
# =========================
ranked_seeds, month = recommend_seed_and_month(
    crop,
    data["season"],
    data["ph"],
    data["irrigation"],
    data["budget"]
)

# =========================
# Yield Prediction
# =========================
predicted_yield = predict_crop_yield(
    data["rainfall"],
    data["humidity"],
    data["sunshine"],
    data["nitrogen"],
    data["phosphorus"],
    data["potassium"],
    data["ph"]
)

# =========================
# ✅ FIXED PROFIT CALL (IMPORTANT)
# =========================
profit, revenue, cost, total_tons, total_quintal, price_data, components, cost_per_acre = estimate_profit(
    predicted_yield,
    data["land_size"],
    crop,
    data["season"],
    data["state"],
    data["city"]
)

# =========================
# Optimization Modules
# =========================
fertilizer = fertilizer_recommendation(
    crop,
    data["nitrogen"],
    data["phosphorus"],
    data["potassium"],
    data["ph"],
    data["moisture"]
)

irrigation_advice = irrigation_plan(
    data["rainfall"],
    data["sunshine"],
    data["moisture"],
    crop
)

# =========================
# DISPLAY RESULTS
# =========================
st.success(f"🌾 Recommended Crop: {crop}")

# =========================
# 🌱 Seed Display
# =========================
labels = ["🥇", "🥈", "🥉"]

def get_label(score):
    if score >= 6:
        return "High"
    elif score >= 4:
        return "Medium"
    else:
        return "Low"

st.markdown('<div class="section-title">🌱 Top Seed Recommendations</div>', unsafe_allow_html=True)

for item in ranked_seeds:
    label = get_label(item["score"])

    st.markdown(f"""
    <div class="card">
        <div class="metric">{item['seed']}</div>
        <div class="label">Confidence: {label}</div>
    </div>
    """, unsafe_allow_html=True)

st.info(f"📅 Best Month: {month}")

# =========================
# 📈 Yield Section
# =========================
st.subheader("📈 Yield Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="label">Yield</div>
        <div class="metric">{predicted_yield:.2f} tons/acre</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="label">Production</div>
        <div class="metric">{total_quintal:.0f} quintals</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="label">Profit</div>
        <div class="metric">₹{profit:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 🏪 Market Section
# =========================
st.markdown('<div class="section-title">🏪 Market Insights</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

#st.markdown('<div class="section-title">🏪 Market Price Analysis</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

def market_card(title, value):
    return f"""
    <div class="card">
        <div class="label">{title}</div>
        <div class="metric">₹{value}</div>
    </div>
    """

with col1:
    st.markdown(market_card("Min Price", price_data['min']), unsafe_allow_html=True)

with col2:
    st.markdown(market_card("Max Price", price_data['max']), unsafe_allow_html=True)

with col3:
    st.markdown(market_card("Modal Price", price_data['modal']), unsafe_allow_html=True)
# =========================
# 💸 Cost Breakdown
# =========================
st.markdown('<div class="section-title">💸 Required Cost (per acre)</div>', unsafe_allow_html=True)

for k, v in components.items():
    st.markdown(f"""
    <div class="card">
        <div class="label">{k.capitalize()}</div>
        <div class="metric">₹{v}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <div class="label">Total Cost per Acre</div>
    <div class="metric">₹{cost_per_acre}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 💰 Financial Summary
# =========================
st.subheader("💵 Financial Summary")

st.info(f"Revenue: ₹{revenue:,.2f}")
st.info(f"Total Cost: ₹{cost:,.2f}")
st.success(f"Net Profit: ₹{profit:,.2f}")

# =========================
# 🌱 Other Modules
# =========================
st.markdown('<div class="section-title">💧 Irrigation Plan</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
    <div class="metric">{irrigation_advice}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# 🧪 Fertilizer
# =========================
st.subheader("🧪 Fertilizer Recommendation")

for f in fertilizer:
    if "low" in f.lower() or "acidic" in f.lower() or "alkaline" in f.lower():
        st.warning(f"⚠ {f}")
    elif "sufficient" in f.lower() or "good" in f.lower():
        st.info(f"✔ {f}")
    else:
        st.success(f"✔ {f}")

# =========================
# 💾 Save Record
# =========================
if st.button("💾 Save Record"):
    insert_record((
        data["farmer_name"],
        crop,
        predicted_yield,
        profit
    ))
    st.success("Saved to historical database")