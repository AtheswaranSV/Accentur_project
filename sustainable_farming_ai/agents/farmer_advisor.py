from fastapi import FastAPI
from models.crop_recommender import recommend_crop
from agents.memory import memory
import sqlite3
from datetime import datetime

app = FastAPI()

@app.get("/recommend/{farmer_id}")
def recommend(farmer_id: int):
    conn = sqlite3.connect("farming.db")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM farmers WHERE id=?", (farmer_id,))
    row = cur.fetchone()
    if not row:
        return {"error": "Farmer not found"}

    name, location, soil, rain, temp = row[1], row[2], row[3], row[4], row[5]
    crop = recommend_crop(soil, rain, temp)
    memory.save(name, crop)

    cur.execute("INSERT INTO recommendations (farmer_id, recommendation, timestamp) VALUES (?, ?, ?)",
                (farmer_id, crop, datetime.now()))
    conn.commit()
    conn.close()

    return {"name": name, "recommendation": crop}
