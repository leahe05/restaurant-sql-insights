import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import MEDIUMTEXT, LONGTEXT
from pathlib import Path


df = pd.read_json("../yelp_dataset/user_sample.json")  


engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")


dtype_map = {}
for columns in df.columns:
    if columns in {"friends","elite"}:
        dtype_map[columns]= MEDIUMTEXT()

df.to_sql("user_sample", con=engine, if_exists="replace", index=False, dtype=dtype_map, chunksize=1000, method="multi", schema="yelp_reviews" )

print(f"Data inserted into MySQL table  successfully!")
