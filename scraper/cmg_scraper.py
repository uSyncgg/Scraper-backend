#### uSync LLC
#### Matthew O'Connor, Co-Founder

# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
import requests
import re
import datetime
import time

# Test Data
# Checkmate Gaming Page, testing all tournaments and tournaments for the day
# URL begin = https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii

# Info
# Date and Time
# Tournament Title
# Entry Fee - Done
# Scan title for Requirements
# Regions - Done 
# Skill Level - Done
# URL

# URL = "https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii/-100-gtd-2v2-novice-amateur-snd-best-of-3-180049"
URL_begin = "https://www.checkmategaming.com/tournament/cross-platform/call-of-duty-modern-warfare-ii"
driver = webdriver.Chrome(ChromeDriverManager().install())

# driver.implicitly_wait(10)

#### IMPORTANT: you will need to set a bound for each piece of code here or else it will look through outdate tourneys as well
def ref_link(driver, URL):
    driver.refresh()
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    link = soup.find('div', {'class': 'view-tournament'})
    print(link)
    if str(link) == 'None':
        return ref_link(driver, URL)
    
    return link

def get_link(driver, URL):
    driver.get(URL)

    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    link = soup.find('div', {'class': 'view-tournament'})
    print(link)
    print(type(link))

    if str(link) == 'None':
        ref_link(driver, URL)

    
    link_str = str(link)
    match = re.search(r'href=/tournament/"(.+?)"', link_str)
    # print(link_str.find(':href'))
    print(match)
    if match:
        path = match.group(0)
        print(path)
    else:
        print("Did not work")

    # link_href = link_str[link_str.find(':href'):]
    # # print(link_href)
    # link_hrefPath = link_href[:link_href.find(' ')]
    # # print(link_hrefPath)
    # link_path = link_hrefPath[link_hrefPath.find('"') + 1:len(link_hrefPath) - 1]
    # print(link_path)

    # print(type(link))
    # tes = str(link)
    # print(type(tes))
    # print(tes)
    # a = link.find('a')
    # print(a)
    # # print(type(a))
    # path = a.get('href')
    # print(path)

# Inputs: driver, tourney URL
# Returns: all tournament information
# def cmg_tourney_info(driver, URL):
#     driver.get(URL)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')

    # NEED TO FINISH
    # IMPORTANT: look at main in the esportsagent git hub under the ld3 branch and see what he does to create a list of dictionaries rather
    # than dictionary of lists
    # class was 'tournament-details-date-text'
    # date_time_res = soup.find_all('span', {'class': 'start-date'})
    # print(date_time_res)
    # for i in range(len(date_time_res)):
    #     print(i)
    # date_time = date_time_res[0].text.strip()
    # date_time_list = date_time.split()
    # date = date_time_list[0] + " " + date_time_list[1]
    # # # print(date)
    # time = date_time_list[2] + " " + date_time_list[3] + " " + date_time_list[4]

    # Tourney Title - DONE
    # class was 'tournament-details-info-header'
    # title_res = soup.find_all('div', {'class': 'tournament-details-info-header'})
    # title = title_res[0].text.strip()
    # tourneyTitle = ""
    # for i in range(len(title)):
    #     tourneyTitle = tourneyTitle + title[i]
    #     if (title[i] == "\n"):
    #         break

    # Entry/Per, Team Size, Skill Level - DONE
    # class was 'tournament-details-entry-info'
    # tourney_details_res = soup.find_all('div', {'class': 'tournament-details-entry-info'})
    # tourney_details = tourney_details_res[0].text.strip()
    # tourney_details_list = tourney_details.split()
    # print(tourney_details_res[0].text)

    # entry = tourney_details_list[1] + " " + tourney_details_list[2]
    # team_size_full = tourney_details_list[4] + " " + tourney_details_list[5] + " " + tourney_details_list[6]
    # team_size = team_size_full[4:10]
    # skill_level = tourney_details_list[12] + " " + tourney_details_list[13]

    # print(entry)
    # print(team_size)
    # print(skill_level)  

    # Figure this out
    # Tournament Title 
    # tourney_title_res = soup.find_all('div', {'class': 'tournament-details-info-header'})
    # tourney_title = tourney_title_res[0].text.strip()
    # tourney_title_list = tourney_title.split()
    # # print(tourney_title)
    # tourney = ""
    # for x in tourney_title_list:
    #     tourney = tourney + tourney_title_list[x]
    #     if(tourney_title_list[x] == 'Call'):
    #         break
    
    # print(tourney)
    # info = date_time_res
    # info = tourneyTitle
    # info = per_person
    # return info


# def cmg_tourney_region(driver, URL_begin):
#     driver.get(URL_begin)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     region_details_res = soup.find_all('div', {'class': 'tournament-stats'})
#     # print(region_details_res)
#     region_details = region_details_res[2].find('p')
#     # print(type(str(region_details)))
#     region_string = str(region_details)
#     region_chop = len(region_string) - 4
#     # print(region_details)
#     region = region_string[3:region_chop]
#     # print(region_string[3:region_chop])

#     return region_chop
    

# print(cmg_tourney_info(driver, URL_begin))
# print(cmg_tourney_region(driver, URL_begin)) 
# cmg_tourney_region(driver, URL_begin)
# cmg_tourney_info(driver, URL_begin)
get_link(driver, URL_begin)