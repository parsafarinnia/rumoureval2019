import json

b=[]
c=[]
# def recursive_items(dictionary):
#     for key, value in dictionary.items():
#         b.append(key)
#         if type(value) is dict:
#             yield from recursive_items(value)
#         else:
#             yield (key, value)
# def rec(dictionary):
#     for key in dictionary:
#         b.append(key)
#         if type(dictionary[key]) is dict:
#             rec(dictionary[key])
# def am():
#     c.append(1)



if __name__ == "__main__":
    # a = {"1": {"2": {"3": {"4": {"5": []}}}, "6": [],
    #                 "7": {"8": {"9": []}}, "10": {"11": []}, "12": [], "13": []}}
    # c = {"000": {"2": {"3": {"4": {"5": []}}}, "6": [],
    #                 "7": {"8": {"9": []}}, "10": {"11": []}, "12": [], "13": []}}
    #
    # # recursive_items(a)
    # # b=[]
    # # recursive_items(c)
    # # print(rec(a))
    # rec(a)
    # b=[]
    # rec(c)
    # c={}
    # a=[0,1,2,3,4,5]
    # c['1'] = a[a[1]:a[2]]
    string ="/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/dev-key.json"
    parts = string.split('/')
    print(parts[-1])