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
    [ id,text,classification]
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
        text = post['text']
        id_text_class[item] = {
            "text": text,
            "class": keys[item]
        }

    return id_text_class
# TODO make replies and source df

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



if __name__ == "__main__":
    list_of_files = get_file_path(train_dir)
    post_addresses = get_post_addresses(list_of_files)
    id_text_class_train = make_source_df(post_addresses,
                                         "/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/train-key.json",
                                         "subtaskbenglish"
                                         )
    id_text_class_dev = make_source_df(post_addresses,
                                          "/Users/macbook/Desktop/rumoureval2019/rumoureval-2019-training-data/dev-key.json",
                                          "subtaskbenglish"
                                          )
    list_of_files = get_file_path(test_dir)
    post_addresses = get_post_addresses(list_of_files)
    id_text_class_test = make_source_df(post_addresses,
                                          "/Users/macbook/Desktop/rumoureval2019/final-eval-key.json",
                                          "subtaskbenglish"
                                          )
    make_panda_df(id_text_class_train,"train.json")
    make_panda_df(id_text_class_dev,"dev.json")
    make_panda_df(id_text_class_test,"test.json")
