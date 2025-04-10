import streamlit as st
import sqlite3
import requests
import pandas as pd
from PIL import Image

# Soil type mapping
SOIL_TYPES = {
    0: "Sandy",
    1: "Clay",
    2: "Silty",
    3: "Loamy"
}

st.set_page_config(page_title="Smart Farming Advisor", layout="centered")
st.title("🌾 Smart Farming Crop Advisor")

# --- Soil Image Upload and Detection ---
st.subheader("📷 Upload a Soil Image for Live Type Detection")
uploaded_image = st.file_uploader("Upload soil image (jpg/png)", type=["jpg", "jpeg", "png"])

predicted_soil = None
if uploaded_image:
    files = {"file": uploaded_image.getvalue()}
    try:
        response = requests.post("http://127.0.0.1:8000/predict_soil/", files=files)
        if response.status_code == 200:
            predicted_soil = response.json()["soil_type"]
            st.success(f"🔍 Detected Soil Type: **{SOIL_TYPES[predicted_soil]}**")
        else:
            st.error("❌ Failed to detect soil type.")
    except Exception as e:
        st.error(f"⚠️ Error calling backend: {e}")
else:
    st.warning("📸 Please upload a soil image before submitting the form.")

# --- Input form for farmer details (no soil type dropdown) ---
if predicted_soil is not None:
    with st.form("farmer_input"):
        name = st.text_input("Farmer Name")
        location = st.text_input("Location")
        rainfall = st.number_input("Rainfall (mm)", min_value=0)
        temp = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0)
        submitted = st.form_submit_button("Get Recommendation")

        if submitted:
            try:
                conn = sqlite3.connect("farming.db")
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO farmers (name, location, soil_type, rainfall, temperature)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, location, int(predicted_soil), float(rainfall), float(temp)))
                conn.commit()

                farmer_id = cursor.lastrowid
                conn.close()

                response = requests.get(f"http://127.0.0.1:8000/recommend/{farmer_id}")
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Recommended Crop for {data['name']}: 🌿 **{data['recommendation']}**")
                else:
                    st.error("❌ Error from backend. Is FastAPI server running?")

            except Exception as e:
                st.error(f"⚠️ An error occurred: {e}")

# --- Market Trends Section ---
st.subheader("📈 Top 3 Market Trend Crops")

try:
    df = pd.read_csv("data/market_researcher_dataset.csv")
    df.columns = [col.strip().lower() for col in df.columns]

    if "price" in df.columns and "demand" in df.columns:
        df_sorted = df.sort_values(by="price", ascending=False).head(3)
        st.table(df_sorted[['crop', 'price', 'demand']])
    else:
        st.warning("🟡 CSV missing 'price' or 'demand' column.")

except FileNotFoundError:
    st.error("❌ Market researcher dataset not found!")
except Exception as e:
    st.error(f"⚠️ Error loading market data: {e}")
