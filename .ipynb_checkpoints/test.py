import json
if __name__=="__main__":
    keys_address ="/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/dev-key.json"
    task="subtaskbenglish"
    with open(keys_address) as f:
        keys_json=json.load(f)
        keys = keys_json[task]
    for item in keys:
        print(keys[item])
