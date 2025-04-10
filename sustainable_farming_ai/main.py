from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import torch
import torchvision.transforms as transforms
import sqlite3
import pandas as pd

# --- Model and class map ---
MODEL_PATH = "model/soil_cnn.pt"  # replace with actual model path
SOIL_CLASSES = {0: "Sandy", 1: "Clay", 2: "Silty", 3: "Loamy"}

# Load the model
model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
model.eval()

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

# Initialize FastAPI app
app = FastAPI()

# Enable CORS so frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Soil Prediction Endpoint ---
@app.post("/predict_soil/")
async def predict_soil(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = output.argmax(1).item()

    return {"soil_type": predicted_class, "soil_name": SOIL_CLASSES[predicted_class]}

# --- Crop Recommendation Endpoint ---
@app.get("/recommend/{farmer_id}")
def recommend_crop(farmer_id: int):
    conn = sqlite3.connect("farming.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, soil_type, rainfall, temperature FROM farmers WHERE id = ?", (farmer_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Farmer not found"}

    name, soil, rainfall, temp = row

    # Recommend based on soil type
    suitable_crops = []
    if soil == 0:
        suitable_crops = ["Pearl Millet", "Sorghum"]
    elif soil == 1:
        suitable_crops = ["Wheat", "Barley"]
    elif soil == 2:
        suitable_crops = ["Sugarcane", "Maize"]
    elif soil == 3:
        suitable_crops = ["Rice", "Wheat"]

    try:
        df = pd.read_csv("data/market_researcher_dataset.csv")
        df.columns = [col.strip().lower() for col in df.columns]
        df_filtered = df[df["crop"].isin(suitable_crops)]
        df_sorted = df_filtered.sort_values(by="price", ascending=False)

        if not df_sorted.empty:
            best_crop = df_sorted.iloc[0]["crop"]
        else:
            best_crop = suitable_crops[0]

    except Exception:
        best_crop = suitable_crops[0]

    return {"name": name, "recommendation": best_crop}
