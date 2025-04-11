from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper import TEAMS, PLATFORM, GAMEMODE, REQUIREMENT, MONTHS, SERIES_WORDING
import traceback
from datetime import datetime
import time
import re

# driver = webdriver.Chrome()

URL = 'https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-black-ops-6'

tournaments = []
tourney_info = []

date_time = []

dates = [] 
times = [] 
team_sizes = [] 
gamemodes = [] 
series = [] 
platforms = [] 
entry_fees = [] 
regions = []
prize_pools = []
titles = []
requirements = []
skills = []
company = []

nov_bool = []
am_bool = []
expert_bool = []
agent_bool = []
master_bool = []
challenger_bool = []
one_player_bool = []
two_player_bool = []
three_player_bool = []
four_player_bool = []
platforms_for_filter = []
free_bool = []
na_bool = []
eu_bool = []
latam_bool = []
entry_for_filter = []
usa_bool = []
skill_for_filter = []

return_dict = {
    'Title': [],
    'Time': [],
    'Date': [],
    'Team Size': [],
    'Gamemode': [], 
    'Series': [],
    'Platform': [],
    'Entry Fee': [],
    'Region': [],
    'Prize': [],
    'Requirements': [],
    'URLs': [],
    'Skill': [],
    'Company': [],
    'isEco': [],
    '1v1': [],
    '2v2': [],
    '3v3': [],
    '4v4': [],
    'Platforms_for_filter': [],
    'Novice': [],
    'Amateur': [],
    'Expert': [],
    'Agent': [],
    'Master': [],
    'Challenger': [],
    'isFree': [],
    'isNa': [],
    'isEu': [],
    'isLatam': [],
    'isUSA': [],
    'Skills_for_filter': []
}

def get_banner_info(tournament_banners):
    global regions
    global prize_pools

    for banner in tournament_banners:
        banner_text = banner.text
        banner_text_lst = banner_text.split('\n')
        
        prize_pools.append(banner_text_lst[0])

        for item in banner_text_lst:
            if 'region' in item.lower():
                regions.append(banner_text_lst[banner_text_lst.index(item) + 1])
                break
    
    return None

def get_tournament_links(tournament_link_tags):
    global tournaments

    for link in tournament_link_tags:
        if link.get_attribute('href'):
            tournaments.append(link.get_attribute('href'))
    
    return None

def get_tournament_links_tags(driver, wait):
    driver.get(URL)

    button = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[mi-name="chevron_right"]')))

    try:
        tournament_link_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mdl-button.mdl-js-button.css-ripple-effect.css-ripple-activated')))
        tournament_banners = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tournament-box')))
        
        get_banner_info(tournament_banners)
        get_tournament_links(tournament_link_tags)
    except:
        pass

    while 'disabled' not in button[0].get_attribute('class'):
        try:
            button[0].click()

            button = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[mi-name="chevron_right"]')))
            tournament_link_tags = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mdl-button.mdl-js-button.css-ripple-effect.css-ripple-activated')))
            tournament_banners = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tournament-box')))

            get_banner_info(tournament_banners)
            get_tournament_links(tournament_link_tags)
        except:
            pass

def get_tournament_info(driver, wait):
    global tournaments

    for link in tournaments:
        driver.get(link)
        
        
        tournament_details = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tournament-details-info-container')))

        for detail in tournament_details:
            tourney_info.append(detail.text)

    return None

def extract_tournament_info():
    global tourney_info
    global titles
    global gamemodes
    global series
    global date_time
    global platforms
    global entry_fees
    global team_sizes
    global requirements
    global skills

    for index, tourney in enumerate(tourney_info):
        info = tourney.split('\n')
        ruleset_present = False
        present_skill = []

        entry_fee_index = 10
        team_size_index = 12
        requirement_size_index = 19


        for gamemode in GAMEMODE:
            if gamemode in info[0].lower():
                gamemodes.append(gamemode)
                break

        for word in SERIES_WORDING:
            if word in info[0].lower():
                series.append(word)

                pattern = re.escape(word)
                info[0] = re.sub(pattern, "", info[0], flags=re.IGNORECASE)
                break

        titles.append(info[0])

        if len(series) - 1 < index:
            series.append('none')

        date_time.append(info[8])

        if 'rule' in info[9].lower():
            ruleset_present = True
            entry_fee_index += 2
            team_size_index += 2
            requirement_size_index += 2

        for item in info[requirement_size_index:]:
            for req in REQUIREMENT:
                if req in item.lower():
                    req = req[0].upper() + req[1:]
                    present_skill.append(req)

        if ruleset_present is False:
            platforms.append('All')

        else:
            if 'console' in info[10].lower():
                platforms.append('Console')
            elif 'pc only' in info[10].lower():
                platforms.append('PC')
            elif not any(req in info[10].lower() for req in REQUIREMENT):
                requirements.append(info[10].lower())
                platforms.append('All')
            else:
                platforms.append('All')

        if len(requirements) - 1 < index:
            requirements.append('None')

        if 'free' in info[entry_fee_index].lower():
            entry_fees.append('Free Entry')
        else:

            if ' ' in info[entry_fee_index]:
                temp_list = info[entry_fee_index].split(' ')
                entry_fees.append(" ".join(entry[0].upper() + entry[1:] for entry in temp_list))
            else:
                entry_fees.append(info[entry_fee_index][0].upper() + info[entry_fee_index][1:])

        # entry_fees.append(info[entry_fee_index])

        team_sizes.append(info[team_size_index])

        if len(present_skill) > 0:
            skills.append('/'.join(req for req in present_skill))
        else:
            skills.append('All')

        company.append('cmg')

    return None

def combine_requirements():
    global skills
    global requirements
    global platforms

    for index, skill in enumerate(skills):
        new_entry = ''

        if platforms[index] == 'console only':
            new_entry = 'Console/'
        
        if skill != 'All':
            new_entry += f'{skill}/'

        if requirements[index] != 'None':
            temp_list = []
            if ' ' in requirements[index]:
                temp_list = requirements[index].split(' ')

                new_entry += f'{" ".join(item[0].upper() + item[1:] for item in temp_list)}/'
            else:
                new_entry += f'{requirements[index][0].upper() + requirements[index][1:]}/'

        if new_entry != '':
            if new_entry[-1] == '/':
                new_entry = new_entry[:-2]

            requirements[index] = new_entry

def separate_date_time():
    global date_time
    global dates
    global times

    for dt in date_time:
        dt_lst = dt.split(' ')
        dates.append(dt_lst[0] + ' ' + dt_lst[1])
        times.append(dt_lst[2] + ' ' + dt_lst[3])

    return None  

def set_bools():
    global nov_bool
    global am_bool
    global expert_bool
    global one_player_bool 
    global two_player_bool
    global three_player_bool
    global four_player_bool
    global platforms_for_filter
    global free_bool
    global agent_bool
    global master_bool
    global challenger_bool
    global na_bool
    global eu_bool
    global latam_bool
    global entry_for_filter
    global usa_bool
    global skill_for_filter

    global skills
    global team_sizes
    global platforms
    global entry_fees
    global regions
    global skills

    for i in range(len(skills)):
        if 'nov' in skills[i]:
            nov_bool.append(True)
        else:
            nov_bool.append(False)

        if 'am' in skills[i]:
            am_bool.append(True)
        else:
            am_bool.append(False)

        if 'exp' in skills[i]:
            expert_bool.append(True)
        else:
            expert_bool.append(False)

        if 'nov' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Novice')
            else:
                skill_for_filter[i] += ' Novice'

        if 'am' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Amateur')
            else:
                skill_for_filter[i] += ' Amateur'

        if 'exp' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Expert')
            else:
                skill_for_filter[i] += ' Expert'

        if len(skill_for_filter) - 1 < i:
            skill_for_filter.append('All')

        if '1v1' == team_sizes[i].replace(' ', '') or '1vs1' == team_sizes[i].replace(' ', ''):
            one_player_bool.append(True)
            team_sizes[i] = '1v1'
        else:
            one_player_bool.append(False)

        if '2v2' == team_sizes[i].replace(' ', '') or '2vs2' == team_sizes[i].replace(' ', ''):
            two_player_bool.append(True)
            team_sizes[i] = '2v2'
        else:
            two_player_bool.append(False)
        
        if '3v3' == team_sizes[i].replace(' ', '') or '3vs3' == team_sizes[i].replace(' ', ''):
            three_player_bool.append(True)
            team_sizes[i] = '3v3'
        else:
            three_player_bool.append(False)
        
        if '4v4' == team_sizes[i].replace(' ', '') or '4vs4' == team_sizes[i].replace(' ', ''):
            four_player_bool.append(True)
            team_sizes[i] = '4v4'
        else:
            four_player_bool.append(False)
        
        if 'pc' in platforms[i].lower():
            platforms_for_filter.append('PC')
        elif 'console' in platforms[i].lower():
            platforms_for_filter.append('Console')
        else:
            platforms_for_filter.append('All')
        
        if 'free' in entry_fees[i].lower() and '1 credit' in entry_fees[i].lower():
            entry_for_filter.append('Free Entry ECO')
        elif 'free' in entry_fees[i].lower():
            free_bool.append(True)
            entry_for_filter.append('Free Entry')
        elif '1 credit' in entry_fees[i].lower():
            entry_for_filter.append('ECO')
            free_bool.append(False)
        else:
            free_bool.append(False)
            entry_for_filter.append('')
        
        if 'worldwide' in regions[i].lower():
            regions[i] = 'All'
        
        if 'europe' in regions[i].lower():
            regions[i] = 'EU'

        if 'na' in regions[i].lower():
            na_bool.append(True)
        else:
            na_bool.append(False)

        if 'eu' in regions[i].lower():
            eu_bool.append(True)
        else:
            eu_bool.append(False)

        if 'latam' in regions[i].lower():
            latam_bool.append(True)
        else:
            latam_bool.append(False)

        if 'united states' in regions[i].lower() or 'usa' in regions[i].lower():
            usa_bool.append(True)
            na_bool.append(True)
        else:
            usa_bool.append(False)

        if 'bo' in series[i].lower():
            series[i] = 'Best of ' + series[i][-1]
        elif 'best' in series[i].lower():
            series[i] = series[i][0].upper() + series[i][1:]
        
        master_bool.append(False)
        agent_bool.append(False)
        challenger_bool.append(False)

def build_cmg_return_dict(driver):
    global return_dict

    wait = WebDriverWait(driver, 10)

    get_tournament_links_tags(driver, wait)

    get_tournament_info(driver, wait) 

    extract_tournament_info()   

    separate_date_time()

    set_bools()

    return_dict['Date'] = dates
    return_dict['Entry Fee'] = entry_fees
    return_dict['Gamemode'] = gamemodes
    return_dict['Platform'] = platforms
    return_dict['Prize'] = prize_pools
    return_dict['Region'] = regions
    return_dict['Requirements'] = requirements
    return_dict['Series'] = series
    return_dict['Team Size'] = team_sizes
    return_dict['Time'] = times
    return_dict['Title'] = titles
    return_dict['URLs'] = tournaments
    return_dict['Skill'] = skills
    return_dict['Company'] = company

    return_dict['isEco'] = entry_for_filter
    return_dict['1v1'] = one_player_bool
    return_dict['2v2'] = two_player_bool
    return_dict['3v3'] = three_player_bool
    return_dict['4v4'] = four_player_bool
    return_dict['Platforms_for_filter'] = platforms_for_filter
    return_dict['Novice'] = nov_bool
    return_dict['Amateur'] = am_bool
    return_dict['Expert'] = expert_bool
    return_dict['Agent'] = agent_bool
    return_dict['Master'] = master_bool
    return_dict['Challenger'] = challenger_bool
    return_dict['isFree'] = free_bool
    return_dict['isNa'] = na_bool
    return_dict['isEu'] = entry_for_filter
    return_dict['isLatam'] = latam_bool
    return_dict['isUSA'] = usa_bool
    return_dict['Skills_for_filter'] = skill_for_filter

    return return_dict
