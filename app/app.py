import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.set_page_config(page_title="SmartMetro AI", layout="wide")

# Load model
model = joblib.load("models/model.pkl")
le_day = joblib.load("models/le_day.pkl")
le_crowd = joblib.load("models/le_crowd.pkl")

# -----------------------------
# HEADER
# -----------------------------
st.title("🚆 SmartMetro AI")
st.caption("AI-powered metro crowd prediction & smart travel suggestions")

st.divider()

# -----------------------------
# INPUT SECTION
# -----------------------------
st.subheader("🎯 Plan Your Travel")

col1, col2 = st.columns(2)

with col1:
    hour = st.slider("Select Travel Time", 5, 23, 9)

with col2:
    day_type = st.radio("Day Type", ["Weekday", "Weekend"], horizontal=True)

st.divider()

# -----------------------------
# PREDICTION
# -----------------------------
day_encoded = le_day.transform([day_type])[0]
input_data = np.array([[hour, day_encoded]])
prediction = model.predict(input_data)
crowd = le_crowd.inverse_transform(prediction)[0]

# -----------------------------
# RESULT SECTION
# -----------------------------
col1, col2 = st.columns(2)

# Crowd Result
with col1:
    st.subheader("🚦 Crowd Status")

    if crowd == "High":
        st.error("🔴 High Crowd")
        st.write("Avoid peak hours. Try before 8 AM or after 10:30 AM.")
    elif crowd == "Medium":
        st.warning("🟡 Medium Crowd")
        st.write("Moderate rush. Slight adjustment can help.")
    else:
        st.success("🟢 Low Crowd")
        st.write("Best time to travel.")

# Pricing
with col2:
    st.subheader("Fare Suggestion")

    base_price = 30

    if crowd == "High":
        price = base_price + 10
        st.error(f"Peak Fare: ₹{price}")
    elif crowd == "Medium":
        price = base_price
        st.info(f"Normal Fare: ₹{price}")
    else:
        price = base_price - 5
        st.success(f"Discount Fare: ₹{price}")

st.divider()

# -----------------------------
# CHART SECTION
# -----------------------------
st.subheader("📊 Crowd Trend (Full Day)")

hours = list(range(5, 24))
mapping = {"Low": 1, "Medium": 2, "High": 3}
crowd_numeric = []

for h in hours:
    day_encoded = le_day.transform([day_type])[0]
    pred = model.predict([[h, day_encoded]])
    level = le_crowd.inverse_transform(pred)[0]
    crowd_numeric.append(mapping[level])

df = pd.DataFrame({
    "Hour": hours,
    "Crowd Level": crowd_numeric
})

st.line_chart(df.set_index("Hour"))

st.caption("1 = Low | 2 = Medium | 3 = High")

st.divider()

# -----------------------------
# INFO SECTION
# -----------------------------
with st.expander("📌 About this system"):
    st.write("""
    - Predicts metro crowd using AI  
    - Suggests better travel time  
    - Recommends smart pricing  
    """)

# Footer
st.caption("🚀 Built for Smart Urban Mobility")
