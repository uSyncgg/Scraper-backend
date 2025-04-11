#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
from .pymongo_get_database import get_database

def write_all(data):
    dbname = get_database()
    collection_name = dbname["tournaments"]
    num = 0

    for i in range(len(data['date'])):
        tournament_num = {
            "_id": num,
            "date": data["date"][i],
            "time": data["time"][i],
            "title": data["title"][i],
            "entry": data["entry fee"][i],
            "region": data["region"][i],
            "platforms": data["platform"][i],
            "requirements": data["requirements"][i],
            "skill": data["skill"][i],
            "gamemode": data['gamemode'][i],
            'series': data['series'][i],
            'prize': data['prize'][i],
            'team_size': data['team size'][i],
            'company': data['company'][i],
            'iseco': data['iseco'][i],
            '1v1': data['1v1'][i],
            '2v2': data['2v2'][i],
            '3v3': data['3v3'][i],
            '4v4': data['4v4'][i],
            'Platforms_for_filter': data['Platforms_for_filter'][i],
            'novice': data['novice'][i],
            'amateur': data['amateur'][i],
            'expert': data['expert'][i],
            'agent': data['agent'][i],
            'master': data['master'][i],
            'challenger': data['challenger'][i],
            'isFree': data['isFree'][i],
            'isNa': data['isNa'][i],
            'isEu': data['isEu'][i],
            'isLatam': data['isLatam'][i],
            'isUSA': data['isUSA'][i],
            'Skills_for_filter': data['Skills_for_filter'][i],
            'url': data['urls'][i]
        }

        collection_name.insert_one(tournament_num)
        num += 1
    
    return None

def write_all_links(data):
    dbname = get_database()
    collection_name = dbname["links"]
    num = 0

    for i in data['urls']:

        link_num = {
            "_id": num,
            "url": i
        }        

        collection_name.insert_one(link_num)
        num += 1

    return None
