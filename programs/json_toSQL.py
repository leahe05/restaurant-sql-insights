import pandas as pd
from sqlalchemy import create_engine


file_to_sql = input("which file to sql")
data = pd.read_json(file_to_sql)
df = pd.DataFrame(data)


engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")

# clean make input 
df.to_sql("user_sample", con=engine, if_exists="replace", index=False)

print("Data inserted into MySQL successfully!")
