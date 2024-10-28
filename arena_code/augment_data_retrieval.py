import urllib.request, json 
import pymongo
from pymongo import MongoClient
from secrets import SECRETS
import yaml
import requests
import json

def mongodb_augment_insert(basic_info):
    url = "http://localhost:8000/augment"

    payload = json.dumps({
        "name": basic_info['name'],
        "tier": basic_info['tier'],
        "desc": basic_info['desc'],
        "tooltip": basic_info['tool_tip']
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def mongoDBInsert(data: dict,collection_name: str):
    try:
        uri = SECRETS["mongo_uri"]
        client = MongoClient(uri,
                            username= SECRETS["username"],
                            password=SECRETS["password"])
        database = client["augment_data"]
        collection = database[collection_name]
        if not data:
            raise Exception("Attemped to add to DB without any data. Data:",data)
        name = data['name']
        #check if augment already exists
        

        if collection.count_documents({'name':data['name']}):
            result = collection.replace_one(
                {'name':data['name']},
                data,
                upsert=True
            )
            print(f'Found existing entry, modifying.({name})')
        else:
            result = collection.insert_one(data)
        print('RESULT',result)
        client.close()

    except Exception as e:
        raise Exception("The following error occurred: ", e)

def print_dict(data: dict):
    print(yaml.dump(data))
    return

with open('C:/Users/bryan/OneDrive/Documents/test123/arena_test_py/arena_code/assets/arena_augment_data_1420.json','r') as f:
    augments = json.load(f)
    possible_data_values = set()
    for augment in augments['augments']:
        name = augment['name']
        tier = augment['rarity']
        data_values = augment['dataValues']
        desc = augment['desc']
        tool_tip = augment['tooltip']
        calculations = augment['calculations']

        #print_dict(data_values)
        for stat in data_values.keys():
            if stat not in possible_data_values:
                possible_data_values.add(stat)

        basic_info = {}
        basic_info['name'] = name
        basic_info['tier'] = tier
        basic_info['desc'] = desc
        basic_info['tool_tip'] = tool_tip

        #name is the unique id for each augment
        data_values['name'] = name
        calculations['name'] = name

        #insertion here
        mongodb_augment_insert(basic_info)
        #mongoDBInsert(basic_info,"augment_basic_info")
        #mongoDBInsert(data_values,"augment_data_values")
        #mongoDBInsert(calculations,"augment_calculations")
        

    #print('POSSIBLE DATA VALUES',possible_data_values)
        




