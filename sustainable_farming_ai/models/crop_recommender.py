import pandas as pd

# Load dataset
try:
    df = pd.read_csv("data/farmer_advisor_dataset.csv")
except FileNotFoundError:
    raise FileNotFoundError("The dataset 'farmer_advisor_dataset.csv' was not found in the 'data' folder.")

# Normalize column names
df.columns = [col.strip().lower() for col in df.columns]

# Ensure 'crop_type' column exists
if 'crop_type' not in df.columns:
    raise KeyError(f"'crop_type' column not found in dataset. Available columns: {df.columns.tolist()}")

# Convert 'crop_type' to category
df['crop_type'] = df['crop_type'].astype('category')

# Example crop recommendation function
def recommend_crop(soil_ph, soil_moisture, temperature_c, rainfall_mm):
    filtered = df[
        (df['soil_ph'] >= soil_ph - 0.5) & (df['soil_ph'] <= soil_ph + 0.5) &
        (df['soil_moisture'] >= soil_moisture - 5) & (df['soil_moisture'] <= soil_moisture + 5) &
        (df['temperature_c'] >= temperature_c - 2) & (df['temperature_c'] <= temperature_c + 2) &
        (df['rainfall_mm'] >= rainfall_mm - 20) & (df['rainfall_mm'] <= rainfall_mm + 20)
    ]
    
    if not filtered.empty:
        return filtered['crop_type'].value_counts().idxmax()
    else:
        return "No suitable crop found"
