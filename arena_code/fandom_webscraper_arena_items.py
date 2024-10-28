import urllib.request, json 

with urllib.request.urlopen("https://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json") as url:
    league_of_legends_items = json.load(url)
    #if ['maps']['30'] == True, in Arena
    for item in league_of_legends_items:
        cur_item_name = league_of_legends_items[item]['name']
        if league_of_legends_items[item]['maps']['30'] and 'requiredChampion' not in league_of_legends_items["data"][item].keys():
            print(cur_item_name)
        
