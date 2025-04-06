import pandas as pd

def get_top_market_trends(n=3):
    df = pd.read_csv("data/market_researcher_dataset.csv")
    df_sorted = df.sort_values(by="price", ascending=False)
    return df_sorted.head(n).to_dict(orient="records")
