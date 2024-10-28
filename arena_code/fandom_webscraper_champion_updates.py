import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helper_classes.champion_class import ArenaChampion

driver = webdriver.Chrome()
driver.get('https://leagueoflegends.fandom.com/wiki/Arena_(League_of_Legends)')
print(driver.title)
html_source = driver.page_source
if not html_source:
    print('ERROR: Cannot get page info.')
    exit()

soup = BeautifulSoup(html_source,'html.parser')

print('FINDING TABLE-------------------------------------------')
s = soup.find('table',class_='article-table sortable jquery-tablesorter')
if not s:
    print('ERROR: Unable to find champion table.')
    exit()

#print('Champion Table',s)
content = s.find_all('tr')

champions_tracker = []

for champion in content[1:]:
    cur_champion = ArenaChampion()
    name = champion.find_all('a')[1]
    cur_champion.set_name(name)
    print('Champion Name:',name.text)

    print('Champion Ability Changes:')
    abilities = champion.find_all('td')[3] #inside is <p>(name of ability/pic),<ul>(desc of changes)

    test = abilities.find_all(['p','ul'])
    cur_ability_name = ''
    ability_changes = []

    temp = {}
    #iterating through all ability changes skipping in pairs
    for index in range(0,len(test),2):
        name_row = test[index]
        change_row = test[index+1]

        cur_ability_name= ''
        ability_changes = []
        if name_row.text.rstrip().lstrip() == 'Stats':
            print('Stat Change: vvv')
            cur_ability_name = 'Stats'
        else:
            cur_ability_name = name_row.find_all('a')[1].text
            cur_name_photo = name_row.find('img',)['data-src']
            print('Ability Name:',cur_ability_name,'| Ability Photo URL:',cur_name_photo)

        #add ability changes
        for bulletpoint in change_row.find_all('li'):
            ability_changes.append(bulletpoint.text)
            print('change -',bulletpoint.text)
        
        cur_champion.add_single_ability_changes(cur_ability_name,ability_changes)
    
    champions_tracker.append(cur_champion)

    #print('champ tracker',champions_tracker)
    print(temp)
    break

print('print',str(champions_tracker[0]))
    


#print(content[0])
print(type(content))