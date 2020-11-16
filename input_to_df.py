import os
import csv
import json
import pickle
import pandas as pd
import math
import emoji
import regex

train_dir = '/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data'
test_dir = "/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-test-data"
'''
1- id - address
2- make a dictionary of sources and replies
3- make a df for source text and classification 
4- make a df for reply and classification
5- source only bert
'''

b = []
def rec(dictionary):
    for key in dictionary:
        b.append(key)
        # print(b)
        if type(dictionary[key]) is dict:
            rec(dictionary[key])

def get_file_path(dirName):
    '''
    :param dirName: direction of the directory of all data
    :return: a list of file directions in that directory
    '''
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    # print('listoffiles',listOfFiles)
    return listOfFiles


def get_post_addresses(list_of_files):
    '''

    :param list_of_files: a list of all files in directory
    :return: a dictionary of all posts from source to reply and tweet and reddit post with the
    format of { id : address}
    '''
    posts_id_address = {}
    for elem in list_of_files:
        elem = str(elem)
        parts = elem.split('/')
        if (parts[-2] != "dev-key") and (parts[-2] != "raw") and (parts[-2] != "structure") and (
                parts[-2] != "train-key") and (parts[-2] != "tweets-dev-key") and (parts[-2] != "tweets-train-key") and \
                parts[-1].endswith('.json'):
            posts_id_address[parts[-1][:-5]] = elem
    return posts_id_address


def get_source_replies(list_of_files):
    '''
    :param list_of_files: a list of all files in directory
    :return: a dictionary of all posts and their replies in the format of
    {source_id :[replies]
    '''
    source_replies = {}
    for elem in list_of_files:
        elem = str(elem)
        parts = elem.split("/")
        if parts[-1].endswith('structure.json'):
            with open(elem) as f:
                structure = json.load(f)
                source_replies.update(structure)
    return source_replies


def make_source_df(list_of_addresses, keys_address, task):
    '''
    [ id:{text,classification}}
    :param list_of_addresses: all of the jsons addresses
    :param keys_address: wether its train or validation or test
    :param task: if its subtask A or B
    :return: a dictionary with the format above
    '''

    id_text_class = {}
    with open(keys_address) as f:
        keys_json = json.load(f)
        keys = keys_json[task]
    for item in keys:
        address_of_post = list_of_addresses[item]
        with open(address_of_post) as f2:
            post = json.load(f2)
        if len(item)>10:
            text = post['text']
        else:
            text = post['data']['children'][0]['data']['title']
        id_text_class[item] = {
            "text": text,
            "class": keys[item]
        }

    return id_text_class


def make_panda_df(id_text_class,output_dir):
    '''
    saves input to json in df form
    :param id_text_class: input of dictionary
    :param output_dir: direction of the json to be saved
    :return: none
    '''
    data = id_text_class
    data_pd = pd.DataFrame.from_dict(data)
    output_address = output_dir
    output = data_pd.T.to_json(output_address)

def unnest_replies(dic_of_structures):
    index = []
    list_dic=list(dic_of_structures)
    '''

    :param dic_of_structures: a nested tree like source replies and replies of replies structure
    :return: un nested source replies with format { source : [ r1,r2...]}
    '''
    dic_of_structures_unnested={}
    for key in dic_of_structures:
        index.append(len(b))
        rec(dic_of_structures[key])
    index.append(len(b))
    for i in range(len(dic_of_structures)):
        dic_of_structures_unnested[list_dic[i]]=b[index[i]:index[i+1]]
    return dic_of_structures_unnested

def make_augmented_text(unnested_replies,list_of_files,id_text_class_source):
    '''

    :param unnested_replies:
    :param list_of_files:
    :param id_text_class_source:
    :return: { source text, reply text , class of source}
    '''
    source_reply_class={}

    for source in id_text_class_source:
        source_text=id_text_class_source[source]['text']
        with open(list_of_files[source]) as f2:
            post = json.load(f2)
        if len(source) > 10:
            replY_text = post['text']
        else:
            replY_text = post['data']['children'][0]['data']['title']
        source_reply_class[source] = {
            "source_text": source_text,
            "reply_text": replY_text,
            "class": id_text_class_source[source]['class']
        }
    return source_reply_class

if __name__ == "__main__":
    list_of_files = get_file_path(train_dir)
    post_addresses = get_post_addresses(list_of_files)
    source_replies = get_source_replies(list_of_files)
    unnested_replies = unnest_replies(source_replies)
    with open('unnested_repliest.json', 'w') as outfile:
        json.dump(unnested_replies,outfile)
    id_text_class_train = make_source_df(post_addresses,
                                         "/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/train-key.json",
                                         "subtaskbenglish"
                                         )
    id_text_class_dev = make_source_df(post_addresses,
                                          "/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/dev-key.json",
                                          "subtaskbenglish"
                                          )
    list_of_files = get_file_path(test_dir)
    source_replies = get_source_replies(list_of_files)
    unnested_replies_test = unnest_replies(source_replies)
    post_addresses_test = get_post_addresses(list_of_files)
    id_text_class_test = make_source_df(post_addresses_test,
                                          "/Users/macbook/Desktop/rumoureval2019/final-eval-key.json",
                                          "subtaskbenglish"
                                          )

    source_reply_class_train = make_augmented_text(unnested_replies, post_addresses,id_text_class_train)
    source_reply_class_test = make_augmented_text(unnested_replies_test, post_addresses_test,id_text_class_test)
    source_reply_class_dev = make_augmented_text(unnested_replies, post_addresses,id_text_class_dev)
    make_panda_df(source_reply_class_train,"source_reply_train.json")
    make_panda_df(source_reply_class_test,"source_reply_dev.json")
    make_panda_df(source_reply_class_dev,"source_reply_test.json")

