import itertools
import json


# all possible feedback symbols
symbols = ['r', 'y', 'g']

# generate all possible combinations of length 5
all_feedbacks = [''.join(p) for p in itertools.product(symbols, repeat=5)]


all_feedbacks_coded ={}

for fedback in all_feedbacks:
    code = 0
    for j in range(5):
        if fedback[j] == 'y':
            code += (3 ** j)  
        elif fedback[j] == 'g':
            code += (3 ** j) * 2
        
    all_feedbacks_coded[fedback] = code
    


# save to JSON
with open('dataset/feedbacks.json', 'w', encoding='utf-8') as f:
    json.dump(all_feedbacks_coded, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_feedbacks)} feedback patterns to all_feedbacks_5_letter.json")
