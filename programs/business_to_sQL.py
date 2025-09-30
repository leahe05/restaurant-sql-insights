import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import JSON


data = pd.read_json("../yelp_dataset/samples/business_sample.json")
dtype_map={}

df = pd.DataFrame(data)

print((df["categories"]).dtype)

print(df["categories"].head())


#for columns in df.columns:
   # if columns in {"attributes", "hours", "categories"}:
       # df[columns] = df[columns].where(df[columns].notna(), None)
       # dtype_map[columns]= JSON()
#engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")

#df.to_sql("business_sample", con=engine,if_exists= "replace", index= False, dtype=dtype_map, chunksize=1000, method="multi", schema="yelp_reviews" )


#print("Data inserted into MySQL successfully!")
