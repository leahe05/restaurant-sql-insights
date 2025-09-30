import pandas as pd
from sqlalchemy import create_engine

df = pd.read_json("../yelp_dataset/samples/checkin_sample.json")

df["date"]= df["date"].str.split(",")
df= df.explode("date")
df["date"]= pd.to_datetime(df["date"].str.strip())

engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")
df.to_sql("checkin_sample", con=engine, if_exists="replace", index=False)

