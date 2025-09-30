import json

# Load the sampled business IDs
f = open("../yelp_dataset/tip_sample.json", "r", encoding="utf-8")
businesses = json.load(f)
f.close()

user_ids = set()
for b in businesses:
    if "user_id" in b:
        user_ids.add(b["user_id"])

# Collect matching tips into a list
fout = open("../yelp_dataset/samples/user_sample.json", "w", encoding="utf-8")
fin = open("yelp_academic_dataset_user.json", "r", encoding="utf-8")


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