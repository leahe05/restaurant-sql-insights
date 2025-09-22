import json

# Load the sampled business IDs
f = open("yelp_dataset/tip_sample.json", "r", encoding="utf-8")
businesses = json.load(f)
f.close()

user_ids = set()
for b in businesses:
    if "user_id" in b:
        user_ids.add(b["user_id"])

# Collect matching tips into a list
fin = open("yelp_dataset/yelp_academic_dataset_user.json", "r", encoding="utf-8")
tips = []

for line in fin:
    line = line.strip()
    if line == "":
        continue
    obj = json.loads(line)
    if obj["user_id"] in user_ids:
        tips.append(obj)

fin.close()

# Save as a JSON array (same style as your business_sample.json)
fout = open("yelp_dataset/user_sample.json", "w", encoding="utf-8")
json.dump(tips, fout, indent=2)
fout.close()
