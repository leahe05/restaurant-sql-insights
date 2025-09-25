import json

# Load the sampled business IDs

f = open("../yelp_dataset/business_sample.json", "r", encoding="utf-8")
businesses = json.load(f)
f.close()

business_ids = set()
for b in businesses:
    if "business_id" in b:
        business_ids.add(b["business_id"])

desired_sample=input("please put in the file u want to sample based on business ")

end_sample = input("please put the name of the sampled file ")
# Collect matching tips into a list
fin = open(desired_sample, "r", encoding="utf-8")
fout = open(end_sample, "w", encoding="utf-8")

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

