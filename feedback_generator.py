import json
import itertools

# all possible feedback symbols
symbols = ['r', 'y', 'g']

# generate all possible combinations of length 5
all_feedbacks = [''.join(p) for p in itertools.product(symbols, repeat=5)]

# save to JSON
with open('dataset/feedbacks.json', 'w', encoding='utf-8') as f:
    json.dump(all_feedbacks, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_feedbacks)} feedback patterns to all_feedbacks_5_letter.json")
