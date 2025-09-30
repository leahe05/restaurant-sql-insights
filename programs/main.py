#!/usr/bin/env python3

import json
import os
import random
random.seed(42)
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.dialects.mysql import JSON
import os; os.makedirs("../yelp_dataset/samples", exist_ok=True)

# error handeling 
#next thing to relearn is my code for the first 2 programs, try except a

def random_business_sample():
   

    f = open("../yelp_dataset/yelp_academic_dataset_business.json", "r", encoding="utf-8")
    lines = f.readlines()
    f.close()


    sampled = random.sample(lines, 1000)


    objects = []
    for line in sampled:
        obj = json.loads(line)
        objects.append(obj)
        #print(obj)   # still print to screen


    out = open("../yelp_dataset/samples/business_sample.json", "w", encoding="utf-8")
    json.dump(objects, out, indent=2, ensure_ascii=False)
    out.close()

def sampling_with_business_id():
    l= ["../yelp_dataset/yelp_academic_dataset_checkin.json", "../yelp_dataset/yelp_academic_dataset_review.json", "../yelp_dataset/yelp_academic_dataset_tip.json" ]
    l_new = [path.replace("yelp_academic_dataset_", "samples/").replace(".json", "_sample.json") for path in l]
    f = open("../yelp_dataset/samples/business_sample.json", "r", encoding="utf-8")
    businesses = json.load(f)
    f.close()
    business_ids = set()

    for b in businesses:
            if "business_id" in b:
                business_ids.add(b["business_id"])
                
    for src_path, out_name in zip(l,l_new):

    
        fin = open(src_path, "r", encoding="utf-8")
        fout = open(out_name, "w", encoding="utf-8")

        fout.write("[")
        first=True
        for line in fin:
            line = line.strip()
            if line == "":
                continue
            obj = json.loads(line)



            if obj["business_id"] in business_ids:
                if not first:
                    fout.write(", \n")
                else:
                    first = False
                json.dump(obj, fout)

        fout.write("]\n")        

        fin.close()
        fout.close()

def sampling_with_user_id ():
    # Load the sampled business IDs
    f = open("../yelp_dataset/samples/tip_sample.json", "r", encoding="utf-8")
    businesses = json.load(f)
    f.close()

    user_ids = set()
    for b in businesses:
        if "user_id" in b:
            user_ids.add(b["user_id"])

    # Collect matching tips into a list
    fout = open("../yelp_dataset/samples/user_sample.json", "w", encoding="utf-8")
    fin = open("../yelp_dataset/yelp_academic_dataset_user.json", "r", encoding="utf-8")


    fout.write("[")
    first=True
    for line in fin:
        line = line.strip()
        if line == "":
         continue
        obj = json.loads(line)



        if obj["user_id"] in user_ids:
            if not first:
                fout.write(", \n")
            else:
                first = False
            json.dump(obj, fout)

    fout.write("]\n")        
    # Save as a JSON array (same style as your business_sample.json)

    fout.close()
    fin.close()

def json_to_sQL():
    #dnt hardcode engine 

    db_url = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    
    engine = create_engine(db_url)
    #engine = create_engine("mysql+pymysql://root:Lea110229!@localhost:3306/yelp_reviews")

    business_df = pd.read_json("../yelp_dataset/samples/business_sample.json")
    checkin_df = pd.read_json("../yelp_dataset/samples/checkin_sample.json")
    user_df = pd.read_json("../yelp_dataset/samples/user_sample.json")  
    review_df= pd.read_json("../yelp_dataset/samples/review_sample.json")
    tip_df= pd.read_json("../yelp_dataset/samples/tip_sample.json")
    
    dtype_map_business={}
    dtype_map_user={}

   #check categories 
    for columns in business_df.columns:
        if columns in {"attributes", "hours", "categories"}:
            business_df[columns] = business_df[columns].where(business_df[columns].notna(), None)
            dtype_map_business[columns]= JSON()

    
    for columns in user_df.columns:
        if columns in {"friends","elite"}:
            dtype_map_user[columns]= MEDIUMTEXT()
    
    checkin_df["date"]= checkin_df["date"].str.split(",")
    checkin_df= checkin_df.explode("date")
    checkin_df["date"]= pd.to_datetime(checkin_df["date"].str.strip(), errors="coerce")

    business_df.to_sql("business_sample", con=engine,if_exists= "replace", index= False, dtype=dtype_map_business, chunksize=1000, method="multi")
    user_df.to_sql("user_sample", con=engine, if_exists="replace", index=False, dtype=dtype_map_user, chunksize=1000, method="multi")
    checkin_df.to_sql("checkin_sample", con=engine, if_exists="replace", index=False)
    review_df.to_sql("review_sample", con=engine, if_exists="replace", index=False)
    tip_df.to_sql("tip_sample", con=engine, if_exists="replace", index=False)

def main():
    random_business_sample()
    sampling_with_business_id()
    sampling_with_user_id()
    json_to_sQL()

if __name__ == "__main__":
    main()