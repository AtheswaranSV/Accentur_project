from agents.memory import memory
from agents.market_researcher import get_top_market_trends
from models.crop_recommender import recommend_crop

def run_demo():
    farmer = {
        "name": "Raj",
        "soil": 2,
        "rain": 300,
        "temp": 27
    }
    crop = recommend_crop(farmer["soil"], farmer["rain"], farmer["temp"])
    memory.save(farmer["name"], crop)

    print(f"{farmer['name']} should grow {crop}")
    print("Market Trends:")
    for trend in get_top_market_trends():
        print(trend)

run_demo()
