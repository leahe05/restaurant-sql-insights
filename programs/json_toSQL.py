import pandas as pd
from sqlalchemy import create_engine

# Your JSON data (list of dicts)
data = pd.read_json("yelp_dataset/checkin_sample.json")
df = pd.DataFrame(data)

# Step 2: Create SQLAlchemy engine for MySQL
# Replace values with your own MySQL credentials
engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")

# Step 3: Write DataFrame to MySQL
df.to_sql("checkin_test", con=engine, if_exists="replace", index=False)

print("Data inserted into MySQL successfully!")
