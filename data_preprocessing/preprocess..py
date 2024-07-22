from datasets import load_dataset

ds = load_dataset("argilla/llama-2-banking-fine-tune",split="train")

ds_formatted = [
    {"messages": [
        {"role": "system", "content": "You are a customer service representative from Bank of baroda. Please reply customer requests using polite and respectful language."},
        {'role': 'user', 'content': x["request"]},
        {'role': 'assistant', 'content': x["response-1"]}]} for x in ds
]

import random
random.shuffle(ds_formatted)

ds_train = ds_formatted[:80]
ds_val = ds_formatted[80:]

import json

with open('data/train.jsonl', 'w') as f:
    for line in ds_train:
        json.dump(line, f)
        f.write('\n')

with open('data/val.jsonl', 'w') as f:
    for line in ds_val:
        json.dump(line, f)
        f.write('\n')


