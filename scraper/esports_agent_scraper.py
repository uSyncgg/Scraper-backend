from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper import TEAMS, PLATFORM, GAMEMODE, REQUIREMENT
import traceback 
import re

# driver = webdriver.Chrome()

URL = 'https://esportsagent.gg/tournament'

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
urls = []
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
entry_for_filter = []
skill_for_filter = []
free_bool = []
na_bool = []
eu_bool = []
latam_bool = []
usa_bool = []

return_dict = {
    'Title': [],
    'Time': [], # Derive from date
    'Date': [],
    'Team Size': [],
    'Gamemode': [], # Derive from title
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

def extend_page(wait):
    button = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-button.ui-button__size-middle.ui-button__type-primary.ui-button__outlined.mt-4')))
    
    try:
        while button[0].is_enabled():
            button[0].click()
    except:
        pass

    return None

def get_active_tournaments_and_platforms(wait):
    global platforms
    global tourney_info

    classes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'relative.flex-1.p-6.space-y-3')))
    
    for c in classes:
        gray = False
        gray_text = None

        try:
            gray_text = c.find_element(By.CLASS_NAME, 'font-semibold.text-lg.leading-6.text-gray-700')
            
            if gray_text.text:
                gray = True
        except:
            gray = False

        if gray is False:
            tourney_info.append(c.text)

            try:
                platforms_found = c.find_elements(By.CSS_SELECTOR, 'img')
                platforms_listed = []

                for plat in platforms_found:
                    platform_option = plat.get_attribute('alt').lower()

                    for p in PLATFORM:
                        if p in platform_option:
                            platforms_listed.append(p)

                if len(platforms_listed) == len(PLATFORM):
                    platforms.append('All')
                elif PLATFORM[0] in platforms_listed and PLATFORM[1] in platforms_listed and PLATFORM[2] not in platforms_listed and PLATFORM[3] not in platforms_listed:
                    platforms.append('PC')
                elif PLATFORM[2] in platforms_listed and PLATFORM[3] in platforms_listed and PLATFORM[0] not in platforms_listed and PLATFORM[1] not in platforms_listed:
                    platforms.append('Console')
                elif PLATFORM[2] in platforms_listed and PLATFORM[0] not in platforms_listed and PLATFORM[1] not in platforms_listed and PLATFORM[3] not in platforms_listed:
                    platforms.append('Console')
                elif PLATFORM[3] in platforms_listed and PLATFORM[0] not in platforms_listed and PLATFORM[1] not in platforms_listed and PLATFORM[2] not in platforms_listed:
                    platforms.append('Console')

            except:
                print(f'PLATFORMS BROKE')
                traceback.print_exc()

    return None

def get_urls(wait):
    global urls

    tourney_card = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".grid.md\\:grid-cols-2.lg\\:grid-cols-3.gap-4")))
    urls_located = tourney_card[0].find_elements(By.TAG_NAME, 'a')

    for card in urls_located:
        url = card.get_attribute('href')
        
        if 'tournament' in url:
            urls.append(url)

    return None

def extract_tourney_info():
    global tourney_info
    global date_time
    global titles
    global prize_pools
    global entry_fees
    global regions
    global team_sizes
    global series
    global skills

    for index, tourney in enumerate(tourney_info):
        info = tourney.split('\n')

        date_time.append(info[0])
        

        for team in TEAMS:
            if team in info[1]:
                team_sizes.append(team)
                pattern = re.escape(team)
                info[1] = re.sub(pattern, "", info[1], flags=re.IGNORECASE)
                break
        
        skill = ''
        for req in REQUIREMENT:
            if req in info[1].lower():
                skill += f'{req}/'

                temp_list = info[1].split(' ')
                skill_idxs = []
                for i in range(len(temp_list)):
                    if req in temp_list[i].lower():
                        skill_idxs.append(i)
                
                temp_list = [item for i, item in enumerate(temp_list) if i not in skill_idxs]
                info[1] = ' '.join(w for w in temp_list)
        
        if skill != '':
            skill = skill[0].upper() + skill[1:]
            skills.append(skill)
        else:
            skills.append('All')

        titles.append(info[1])

        # if len(skills) - 1 != index:
        #     skills.append('all')

        if len(requirements) - 1 != index:
            requirements.append('None')

        prize_pools.append(info[3])

        if 'free' in info[5].lower():
            entry_fees.append('Free Entry')
        else:

            if ' ' in info[5]:
                temp_list = info[5].split(' ')
                entry_fees.append(" ".join(entry[0].upper() + entry[1:] for entry in temp_list))
            else:
                entry_fees.append(info[5][0].upper() + info[5][1:])

        regions.append(info[7])

        series.append(info[10])

        company.append('codagent')

    return None

def derive_date_time():
    global date_time
    global dates
    global times

    for d in date_time:
        temp_date_time_list = d.split(' ')

        dates.append(' '.join(item for item in temp_date_time_list[:3]))
        times.append(' '.join(item for item in temp_date_time_list[3:]))

def derive_gamemode():
    global titles
    global gamemodes

    for index, title in enumerate(titles):
        for game in GAMEMODE:
            if game in title.lower():
                gamemodes.append(game)
                break

        if len(gamemodes) - 1 != index:
            gamemodes.append('variant')

def combine_requirements():
    global skills
    global requirements
    global platforms

    for index, skill in enumerate(skills):
        new_entry = ''

        if platforms[index] == 'Console':
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

def set_bools():
    global nov_bool
    global am_bool
    global expert_bool
    global one_player_bool 
    global two_player_bool
    global three_player_bool
    global four_player_bool
    global platforms_for_filter
    global entry_for_filter
    global agent_bool
    global master_bool
    global challenger_bool
    global free_bool
    global na_bool
    global eu_bool
    global latam_bool
    global usa_bool
    global skill_for_filter

    global skills
    global team_sizes
    global platforms
    global entry_fees
    global regions
    global series

    for i in range(len(skills)):
        if 'nov' in skills[i]:
            nov_bool.append(True)
        else:
            nov_bool.append(False)

        if 'am' in skills[i]:
            am_bool.append(True)
        else:
            am_bool.append(False)

        if 'agent' in skills[i]:
            agent_bool.append(True)
        else:
            agent_bool.append(False)

        if 'master' in skills[i]:
            master_bool.append(True)
        else:
            master_bool.append(False)

        if 'challenger' in skills[i]:
            challenger_bool.append(True)
        else:
            challenger_bool.append(False)

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

        if 'agent' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Agent')
            else:
                skill_for_filter[i] += ' Agent'

        if 'master' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Master')
            else:
                skill_for_filter[i] += ' Master'

        if 'challenger' in skills[i].lower():
            if len(skill_for_filter) - 1 < i:
                skill_for_filter.append('Challenger')
            else:
                skill_for_filter[i] += ' Challenger'

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
        
        if 'free' in entry_fees[i].lower() and entry_fees[i] == '$1':
            entry_for_filter.append('Free Entry ECO')
        elif 'free' in entry_fees[i].lower():
            entry_for_filter.append('Free Entry')
        elif entry_fees[i] == '$1':
            entry_for_filter.append('ECO')
        else:
            entry_for_filter.append('')

        if 'free' in entry_fees[i].lower():
            free_bool.append(True)
        else:
            free_bool.append(False)
        
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
        
        expert_bool.append(False)

def build_codagent_return_dict(driver):
    global return_dict

    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    
    extend_page(wait)

    get_active_tournaments_and_platforms(wait)

    get_urls(wait)

    extract_tourney_info()

    derive_date_time()

    derive_gamemode()

    combine_requirements()

    set_bools()

    return_dict['Title'] = titles
    return_dict['Time'] = times
    return_dict['Date'] = dates
    return_dict['Team Size'] = team_sizes
    return_dict['Gamemode'] = gamemodes
    return_dict['Series'] = series
    return_dict['Platform'] = platforms
    return_dict['Entry Fee'] = entry_fees
    return_dict['Region'] = regions
    return_dict['Prize'] = prize_pools
    return_dict['Requirements'] = requirements
    return_dict['URLs'] = urls
    return_dict['Company'] = company
    return_dict['Skill'] = skills

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
    return_dict['isEu'] = eu_bool
    return_dict['isLatam'] = latam_bool
    return_dict['isUSA'] = usa_bool
    return_dict['Skills_for_filter'] = skill_for_filter

    return return_dict
