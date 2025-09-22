import json

# Load the sampled business IDs
f = open("yelp_dataset/business_sample.json", "r", encoding="utf-8")
businesses = json.load(f)
f.close()

business_ids = set()
for b in businesses:
    if "business_id" in b:
        business_ids.add(b["business_id"])

# Collect matching tips into a list
fin = open("yelp_dataset/yelp_academic_dataset_checkin.json", "r", encoding="utf-8")
tips = []

for line in fin:
    line = line.strip()
    if line == "":
        continue
    obj = json.loads(line)
    if obj["business_id"] in business_ids:
        tips.append(obj)

fin.close()

# Save as a JSON array (same style as your business_sample.json)
fout = open("yelp_dataset/che_sample.json", "w", encoding="utf-8")
json.dump(tips, fout, indent=2)
fout.close()
