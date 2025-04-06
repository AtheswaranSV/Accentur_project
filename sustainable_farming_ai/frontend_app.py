import streamlit as st
import sqlite3
import requests
import pandas as pd

st.set_page_config(page_title="Smart Farming Advisor", layout="centered")
st.title("🌾 Smart Farming Crop Advisor")

# --- Input form for farmer details ---
with st.form("farmer_input"):
    name = st.text_input("Farmer Name")
    location = st.text_input("Location")
    soil = st.selectbox("Soil Type", [0, 1, 2, 3], format_func=lambda x: f"Type {x}")
    rainfall = st.number_input("Rainfall (mm)", min_value=0)
    temp = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0)
    submitted = st.form_submit_button("Get Recommendation")

# --- Handle form submission ---
if submitted:
    try:
        conn = sqlite3.connect("farming.db")
        cursor = conn.cursor()

        # Insert new farmer into DB
        cursor.execute("""
            INSERT INTO farmers (name, location, soil_type, rainfall, temperature)
            VALUES (?, ?, ?, ?, ?)
        """, (name, location, int(soil), float(rainfall), float(temp)))
        conn.commit()

        farmer_id = cursor.lastrowid
        conn.close()

        # Call backend API
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
    # Print columns for debugging
    # st.write("CSV Columns:", df.columns.tolist())

    # Fix case-sensitivity by renaming if needed
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
