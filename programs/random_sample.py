import json
import random


# input file
filename = "../yelp_dataset/yelp_academic_dataset_business.json"

f = open(filename, "r", encoding="utf-8")
lines = f.readlines()
f.close()


sampled = random.sample(lines, 1000)


objects = []
for line in sampled:
    obj = json.loads(line)
    objects.append(obj)
    print(obj)   # still print to screen


out = open("../yelp_dataset/business_sample.json", "w", encoding="utf-8")
json.dump(objects, out, indent=2, ensure_ascii=False)
out.close()
