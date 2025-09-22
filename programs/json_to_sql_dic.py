import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import LONGTEXT  # use MYSQL_JSON if your MySQL >= 5.7

# 1) load your array-of-objects JSON
df = pd.read_json("yelp_dataset/business_sample.json")  # <-- update path if needed

# 2) find columns that have dict/list values
def has_nested(col: pd.Series) -> bool:
    return col.map(lambda v: isinstance(v, (dict, list))).any()

nested_cols = [c for c in df.columns if has_nested(df[c])]

# 3) serialize nested cells to JSON strings
for c in nested_cols:
    df[c] = df[c].apply(lambda v: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)

# 4) write to MySQL
engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")

# make a dtype map for the nested columns so they have room
dtype_map = {c: LONGTEXT for c in nested_cols}  # or MYSQL_JSON if supported

df.to_sql(
    "business",
    con=engine,
    if_exists="replace",
    index=False,
    method="multi",
    dtype=dtype_map
)

print("Wrote", len(df), "rows to table 'business'")
