#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
# from bs4 import BeautifulSoup
from selenium import webdriver
# import requests
# import re
from datetime import datetime

# from web_scraper import get_tournament_info, get_tournament_link, get_date, get_tournament_ids
from .data_writer import write_all, write_all_links
from .drop_info import drop_all_tourneys, drop_all_links

from .esports_agent_scraper import build_codagent_return_dict
from .updated_cmg_scraper import build_cmg_return_dict

from .check_tourney_time import check_tourney_time_interface

from scraper import MONTHS

sorted_tourneys = []

def create_sorted_tourneys(cmg_dict, codagent_dict):
    # Function to normalize date formats
    def normalize_date(date_str):
        try:
            print(f'DATE STR: {date_str}')
            return datetime.strptime(date_str, "%B %d, %Y")
        except ValueError:
            clean_date = date_str.replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
            return datetime.strptime(clean_date + ", 2025", "%b %d, %Y")

    # Combine lists from both dictionaries
    combined_entries = []
    for i in range(len(cmg_dict["Date"])):
        combined_entries.append({
            "date": cmg_dict["Date"][i],
            "time": cmg_dict["Time"][i],
            "title": cmg_dict["Title"][i],
            "team size": cmg_dict["Team Size"][i],
            "gamemode": cmg_dict["Gamemode"][i],
            "series": cmg_dict["Series"][i],
            "platform": cmg_dict["Platform"][i],
            "entry fee": cmg_dict["Entry Fee"][i],
            "region": cmg_dict["Region"][i],
            "prize": cmg_dict["Prize"][i],
            "requirements": cmg_dict["Requirements"][i],
            "company": cmg_dict["Company"][i],
            'skill': cmg_dict['Skill'][i],
            'urls': cmg_dict['URLs'][i],
            'iseco': cmg_dict['isEco'][i],
            '1v1': cmg_dict['1v1'][i],
            '2v2': cmg_dict['2v2'][i],
            '3v3': cmg_dict['3v3'][i],
            '4v4': cmg_dict['4v4'][i],
            'Platforms_for_filter': cmg_dict['Platforms_for_filter'][i],
            'novice': cmg_dict['Novice'][i],
            'amateur': cmg_dict['Amateur'][i],
            'expert': cmg_dict['Expert'][i],
            'agent': cmg_dict['Agent'][i],
            'master': cmg_dict['Master'][i],
            'challenger': cmg_dict['Challenger'][i],
            'isFree': cmg_dict['isFree'][i],
            'isNa': cmg_dict['isNa'][i],
            'isEu': cmg_dict['isEu'][i],
            'isLatam': cmg_dict['isLatam'][i],
            'isUSA': cmg_dict['isUSA'][i],
            'Skills_for_filter': cmg_dict['Skills_for_filter'][i]
        })
    
    for i in range(len(codagent_dict["Date"])):
        combined_entries.append({
            "date": codagent_dict["Date"][i],
            "time": codagent_dict["Time"][i],
            "title": codagent_dict["Title"][i],
            "team size": codagent_dict["Team Size"][i],
            "gamemode": codagent_dict["Gamemode"][i],
            "series": codagent_dict["Series"][i],
            "platform": codagent_dict["Platform"][i],
            "entry fee": codagent_dict["Entry Fee"][i],
            "region": codagent_dict["Region"][i],
            "prize": codagent_dict["Prize"][i],
            "requirements": codagent_dict["Requirements"][i],
            "company": codagent_dict["Company"][i],
            'skill': codagent_dict['Skill'][i],
            'urls': codagent_dict['URLs'][i],
            'iseco': codagent_dict['isEco'][i],
            '1v1': codagent_dict['1v1'][i],
            '2v2': codagent_dict['2v2'][i],
            '3v3': codagent_dict['3v3'][i],
            '4v4': codagent_dict['4v4'][i],
            'Platforms_for_filter': codagent_dict['Platforms_for_filter'][i],
            'novice': codagent_dict['Novice'][i],
            'amateur': codagent_dict['Amateur'][i],
            'expert': codagent_dict['Expert'][i],
            'agent': codagent_dict['Agent'][i],
            'master': codagent_dict['Master'][i],
            'challenger': codagent_dict['Challenger'][i],
            'isFree': codagent_dict['isFree'][i],
            'isNa': codagent_dict['isNa'][i],
            'isEu': codagent_dict['isEu'][i],
            'isLatam': codagent_dict['isLatam'][i],
            'isUSA': codagent_dict['isUSA'][i],
            'Skills_for_filter': codagent_dict['Skills_for_filter'][i]
        })

    # Convert dictionary entries to include datetime objects for sorting
    for entry in combined_entries:
        entry["datetime"] = datetime.strptime(
            f"{normalize_date(entry['date']).strftime('%B %d, %Y')} {entry['time']}", 
            "%B %d, %Y %I:%M %p"
        )

    # Sort combined entries by datetime
    sorted_entries = sorted(combined_entries, key=lambda x: x["datetime"])

    # Remove temporary datetime key
    for entry in sorted_entries:
        del entry["datetime"]

    # Reconstruct the sorted dictionaries
    sorted_dict = {
        "date": [entry["date"] for entry in sorted_entries],
        "time": [entry["time"] for entry in sorted_entries],
        "title": [entry["title"] for entry in sorted_entries],
        "team size": [entry["team size"] for entry in sorted_entries],
        "gamemode": [entry["gamemode"] for entry in sorted_entries],
        "series": [entry["series"] for entry in sorted_entries],
        "platform": [entry["platform"] for entry in sorted_entries],
        "entry fee": [entry["entry fee"] for entry in sorted_entries],
        "region": [entry["region"] for entry in sorted_entries],
        "prize": [entry["prize"] for entry in sorted_entries],
        "requirements": [entry["requirements"] for entry in sorted_entries],
        "company": [entry["company"] for entry in sorted_entries],
        'skill': [entry['skill'] for entry in sorted_entries],
        'urls': [entry['urls'] for entry in sorted_entries],
        'iseco': [entry['iseco'] for entry in sorted_entries],
        '1v1': [entry['1v1'] for entry in sorted_entries],
        '2v2': [entry['2v2'] for entry in sorted_entries],
        '3v3': [entry['3v3'] for entry in sorted_entries],
        '4v4': [entry['4v4'] for entry in sorted_entries],
        'Platforms_for_filter': [entry['Platforms_for_filter'] for entry in sorted_entries],
        'novice': [entry['novice'] for entry in sorted_entries],
        'amateur': [entry['amateur'] for entry in sorted_entries],
        'expert': [entry['expert'] for entry in sorted_entries],
        'agent': [entry['agent'] for entry in sorted_entries],
        'master': [entry['master'] for entry in sorted_entries],
        'challenger': [entry['challenger'] for entry in sorted_entries],
        'isFree': [entry['isFree'] for entry in sorted_entries],
        'isNa': [entry['isNa'] for entry in sorted_entries],
        'isEu': [entry['isEu'] for entry in sorted_entries],
        'isLatam': [entry['isLatam'] for entry in sorted_entries],
        'isUSA': [entry['isUSA'] for entry in sorted_entries],
        'Skills_for_filter': [entry['Skills_for_filter'] for entry in sorted_entries]
    }

    return sorted_dict

def establish_common_date(mass_tourney_dict):
    for index, date in enumerate(mass_tourney_dict['date']):
        for month in MONTHS:
            if month in date.lower():
                temp = date.split(' ')
                temp = temp[1:]
                mass_tourney_dict['date'][index] = ' '.join(char for char in temp)
                mass_tourney_dict['date'][index] = month + ' ' + mass_tourney_dict['date'][index]
                mass_tourney_dict['date'][index] = mass_tourney_dict['date'][index].replace('th', '')
                mass_tourney_dict['date'][index] = mass_tourney_dict['date'][index].replace('rd', '')
                mass_tourney_dict['date'][index] = mass_tourney_dict['date'][index].replace('st', '')
                break

        date_list = date.split(' ')
        if ',' in date_list[1]:
            date_list[1] = date_list[1][:-1]

        if date_list[1] in ['1', '21', '31']:
            date_list[1] = date_list[1] + 'st'
        elif date_list[1] in ['2', '3', '22', '23']:
            date_list[1] = date_list[1] + 'rd'
        elif date_list[1] in ['4', '5', '6', '7', '8', '9', '10', '11', '12','13','14','15','16','17','18','19','20','24','25','26','27','28','29','30']:
            date_list[1] = date_list[1] + 'th'
        
        mass_tourney_dict["date"][index] = date_list[0][0].upper() + date_list[0][1:3].lower() + ' ' + date_list[1]

    return None

def expand_series(mass_tourney_dict):
    for series in mass_tourney_dict['series']:
        if 'bo' in series:
            mass_tourney_dict['series'] = 'best of ' + series[-1]

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

def run_main():
    mass_tourney_dict = {}
    driver = webdriver.Chrome(options=options)

    esports_agent_tourney_info = build_codagent_return_dict(driver)

    cmg_tourney_info = build_cmg_return_dict(driver)

    mass_tourney_dict = create_sorted_tourneys(cmg_tourney_info, esports_agent_tourney_info)

    establish_common_date(mass_tourney_dict)

    expand_series(mass_tourney_dict)

    drop_all_tourneys()

    write_all(mass_tourney_dict)

    return 'Scrapers Have Run Successfully'
if __name__ == '__main__':
    run_main()
#     mass_tourney_dict = {}
#     driver = webdriver.Chrome(options=options)

#     esports_agent_tourney_info = build_codagent_return_dict(driver)

#     cmg_tourney_info = build_cmg_return_dict(driver)

#     mass_tourney_dict = create_sorted_tourneys(cmg_tourney_info, esports_agent_tourney_info)

#     establish_common_date(mass_tourney_dict)

#     expand_series(mass_tourney_dict)

#     drop_all_tourneys()

#     write_all(mass_tourney_dict)

    # tester_dict = check_tourney_time_interface(driver, titles=['4v4 *NO APRIL WINNERS* BO6 VARIANT'], URLs=['https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-black-ops-6/1v1-snd-best-of-1-233535'])
