import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database.db import create_tables, get_records


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


st.title("📊 Historical Analytics")

create_tables()
records = get_records()

if records:
    df = pd.DataFrame(
        records,
        columns=[
            "ID",
            "Farmer Name",
            "Crop",
            "Predicted Yield",
            "Estimated Profit"
        ]
    )

    st.dataframe(df)

    st.subheader("📈 Profit Trend")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Estimated Profit"], marker="o")
    ax.set_xlabel("Record Index")
    ax.set_ylabel("Profit")
    ax.set_title("Profit Trend Over Time")
    st.pyplot(fig)

    st.subheader("🌾 Crop Frequency")
    crop_counts = df["Crop"].value_counts()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.bar(crop_counts.index, crop_counts.values)
    ax2.set_xlabel("Crop")
    ax2.set_ylabel("Count")
    ax2.set_title("Most Recommended Crops")
    st.pyplot(fig2)

else:
    st.info("No historical data available yet")