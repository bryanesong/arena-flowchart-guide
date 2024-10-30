import re
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from secrets import SECRETS
from helper_classes.champion_class import ArenaChampion
import time

#dict mapping for specific colors the website uses to categorize effects an augment gives

stat_styling_dict = {
   "color:orange; white-space:normal": "AttackDamage",
   "color: #7A6DFF; white-space:normal":"AbilityPower",
   "color: #FF8C34; white-space:normal": "PhysicalDamage",
   "color: #00B0F0; white-space:normal": "MagicDamage",
   "color: #43D9FB; white-space:normal": "Automatically",
   "color:orangered; white-space:normal": "CriticalStrikeChance",
   "color: #F5EE99; white-space:normal": "AttackSpeed",
   "color: #7ADECD; white-space:normal": "AbilityHaste",
   #"color: #1F995C; white-space:normal": "Health", #caveat on this one, refers to "user's bonus health" as well as based on "enemy's maximum health"
    "color: #FFFDC9; white-space:normal": "MoveSpeed",
    "color: #F9966B; white-space:normal": "TrueDamage" ,
    "color: #E34D4C; white-space:normal": "Burn",
    "color:yellow; white-space:normal": "BonusArmor",
    #"BonusMagicResist": "color: #00FFFF; white-space:normal", #This is a repeat color with magic pen
    "color: #0099CC; white-space:normal": "MaximumMana",
    "color:tomato; white-space:normal": "Lethality",
    "color:tomato; white-space:normal": "ArmorPen",
    #"MagicPenetration": "color: #00FFFF; white-space:normal" #This is a repeat color with magic resist
}

#dict mapping for specific stats that can be found via image(<img>) and their "data-image-key=" tag
stat_image_key_dict = {
    "Heal_power_icon.png": "Healing",
    "Hybrid_resistances_icon.png": "Shielding",
    "Heal_and_shield_power_icon.png": "HealAndShield",
    "Slow_icon.png": "Slow",
    "Flash.png": "FlashModifier",
    "Stun_icon.png": "Immobilizing",
    "Damage_rating.png": "OnTakedown",
    "Melee_role.png": "BecomeMelee", #this one highkey useless since theres only one, incase they add more in the future
    "Dash.png": "DashingModifier",
    "Airborne_icon.png": "KnockBack",
    "Gold.png": "GoldModifier",
    "Disarm_icon.png": "Disarm",
    "Flee_augment.png": "SummonerSpellReplacement", #replaces flee specifically, odd one out would be summoners roulette
    "Cc-immune_icon.png": "CrowdControlImmunity",
    "Akali_Twilight_Shroud_old2.png": "Invisibility",
    "Critical_strike_icon.png": "CriticalStrikeApplier", #not the same as CriticalStrikeChance, this allows abilities/attacks that couldn't crit before to crit
    "Stat_Bonus_item.png": "StatAnvil",
    "Prismatic_Item_item.png": "PrismaticItemAnvil", #either modies future prismatic anvils or grants prismatic anvils... hopefully future augments will compliment
    "Annie_Summon-_Tibbers.png": "PetBooster",
    "Adaptive_Force_icon.png": "AdaptiveForce"
}

#this is a dict mapping for words you can straight up search for in the block of text in its description
stat_key_words_dict = {
   "on-hit": "OnHit",
   "takedown": "OnTakedown",
   "bonus attack range": "AttackRange",
   "keystone runes": "ExtraRunes",
   "Dragon Soul": "DragonSouls",
   "permanent stack": "PermanentStacking",
   "magic resistance": "MagicResistance" ,
   "magic penetration": "MagicPenetration",
   "end of the current round": "CurrentRoundInfiniteStacking",
   "item haste": "ItemHaste",
   "target's maximum health": "TargetMaxHealth",
   "your maximum health": "MaxHealth",
   "bonus health": "BonusHealth"
}

#dict mapping for the actual augment category icons
#CURRENTLY USELESS DO NOT USE 
stat_image_icon_key_dict = {
   "ServeBeyondDeath" : "Serve_Beyond_Death_augment.png",
   "SelfDestruct":"Self_Destruct_augment.png",
   "ScopierWeapons":"Scopier_Weapons_augment.png",
   "CoolDownsRelated" : "Restart_augment.png",
   "Healing":"Restless_Restoration_augment.png",
}

def updateMongoDBWithAugmentCategories(augment_dict):
    try:
        uri = SECRETS["mongo_uri"]
        client = MongoClient(uri,
                            username= SECRETS["username"],
                            password=SECRETS["password"])
        database = client["augment_data"]
        collection = database["augment_basic_info"]
        if not augment_dict:
            raise Exception("Attemped to add to DB without any data. Data:",augment_dict)
        name = augment_dict['name']
        #check if augment already exists
        

        if collection.count_documents({'name': re.compile('^' + re.escape(augment_dict['name']) + '$', re.IGNORECASE)}):
            result = collection.update_one(
                {'name': re.compile('^' + re.escape(augment_dict['name']) + '$', re.IGNORECASE)},
                {"$set":augment_dict},
                upsert=True
            )
            print(f'Found existing entry, modifying.({name})')
        else:
            result = "NOT FOUND"
            print('Unable to insert, no previous augment in db found.')
        print('RESULT',result)
        client.close()

    except Exception as e:
        raise Exception("The following error occurred: ", e)

#takes in html of row, returns dict(dict) 
#{tier:
#   { Augment Name:categories augment falls under}
#} 
def categorizeAugmentStats(row) -> dict:
    cur_augment_info = row.find_all('td')
    augment_data = []
    for col in cur_augment_info:
        augment_data.append(col)
    #print('augment_data',augment_data)

    title = augment_data[0].text
    print('title',title)

    
    html_desc = augment_data[1]
    #search styling
    styling_search = html_desc.find_all("span",style=True)

    categories = set()
    for span in styling_search:
        if (span["style"] in stat_styling_dict) and (stat_styling_dict[span["style"]] not in categories):
            categories.add(stat_styling_dict[span["style"]])
    print('categories',categories)

    #search image key
    image_search = html_desc.find_all("img")
    for img in image_search:
        key = img['data-image-key']
        if (key in stat_image_key_dict) and (stat_image_key_dict[key] not in categories):
            categories.add(stat_image_key_dict[key])
    print('categories2',categories)
    
    #search direct key words
    desc_paragraph_str = html_desc.text
    for key,stat in stat_key_words_dict.items():
        if (key in desc_paragraph_str) and (stat not in categories):
            categories.add(stat)
    print('categories3',categories)

    #tier_text = augment_data[2]
    res = {
        "name":title,
        "categories": list(categories)
    }

    return res



driver = webdriver.Firefox()
driver.get('https://leagueoflegends.fandom.com/wiki/Arena_(League_of_Legends)/Augments')
html_source = driver.page_source
if not html_source:
    print('ERROR: Cannot get page info.')
    driver.quit()
    exit()

soup = BeautifulSoup(html_source,'html.parser')
time.sleep(3)
print('FINDING TABLE-------------------------------------------')
#getting table of augments
s = soup.find_all("table")
if not s:
    print('ERROR: Unable to find augment table.')
    driver.quit()
    exit()

#content is a list of all Augments in their respective rows
content = s[0].find_all('tr')

for row in content[1:]:
    cur_augment_data = categorizeAugmentStats(row)
    print('cur_augment_data',cur_augment_data)
    print('--------')
    updateMongoDBWithAugmentCategories(cur_augment_data)



print('END OF SCRIPT')
driver.quit()

#color:orange; white-space:normal