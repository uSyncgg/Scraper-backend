from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pymongo_get_database import get_database
from .curr_time import get_currTime

date_time = {}
times = {}

CODAGENT_URL = 'https://esportsagent.gg/tournament'

def extract_cmg_tourney_info(wait, URL):
    global date_time

    tournament_details = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tournament-details-info-container')))
    date_time[URL] = tournament_details[0].text.split('\n')[8]

    return None

def separate_date_time():
    global date_time
    global times

    for URL in date_time:
        if 'checkmategaming' not in URL.lower():
            continue

        dt_lst = date_time[URL].split(' ')
        print(f'CMG DATE LIST: {dt_lst}')
        times[URL] = dt_lst[2] + ' ' + dt_lst[3]

    return None  

def extract_codagent_tourney_info(wait, titles):
    global date_time
    
    classes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'relative.flex-1.p-6.space-y-3')))

    for c in classes:
        current_class_list = c.text.split('\n')

        for title in titles:
            if current_class_list[1] == title and title not in date_time.keys():
                date_time[title] = current_class_list[0]

        if len(date_time.keys()) == len(titles):
            break

    return None

def derive_date_time():
    global date_time
    global times

    for title in date_time:
        if 'checkmategaming' in title.lower():
            continue

        temp_date_time_list = date_time[title].split(' ')
       
        times[title] = ' '.join(item for item in temp_date_time_list[3:])

    return None

def cmg_check_tourney_time(driver, URLs):
    for URL in URLs:
        driver.get(URL)
        wait = WebDriverWait(driver, 10)

        extract_cmg_tourney_info(wait, URL)

    separate_date_time()

def codagent_check_tourney_time(driver, titles):
    driver.get(CODAGENT_URL)
    wait = WebDriverWait(driver, 10)

    extract_codagent_tourney_info(wait, titles)
    derive_date_time()

def compare_timing(delete_list, check_list, rewrite_list, current_time):
    global times

    current_time_hour = int(current_time.split(':')[0])
    current_time_minute = int(current_time.split(':')[1].split(' ')[0])

    for entry in check_list:
        doc_time_hour = int(entry['time'].split(':')[0])
        doc_time_minute = int(entry['time'].split(':')[1].split(' ')[0])
        doc_company = entry['company']

        if current_time_minute > doc_time_minute and doc_time_hour == current_time_hour and (('AM' in current_time and 'AM' in entry['time']) or ('PM' in current_time and 'PM' in entry['time'])):
            delete_list.append(entry)
            continue
        elif current_time_hour < doc_time_hour:
            if current_time_minute >= 55 and doc_time_minute <= 5:
                pass
            else:
                delete_list.append(entry)
                continue
        
        if doc_company == 'cmg':
            if entry['time'] != times[entry['url']]:
                entry['time'] = times[entry['url']]
                rewrite_list.append(entry)
            else:
                continue
        
        if doc_company == 'codagent':
            if entry['time'] != times[entry['title']]:
                entry['time'] = times[entry['title']]
                rewrite_list.append(entry)
            else:
                continue

    return None

def check_doc(doc_time, doc_date, current_time, current_date, tomorrow_date):
    doc_date = doc_date[:-2]
    print(f'FIRST DOC TIME: {doc_time}')
    print(f'CURRENT TIME: {current_time}')

    print(f'CURRENT DATE: {current_date}')
    print(f'FIRST DOC DATE: {doc_date}')
    print(f'TOMORROW DATE: {tomorrow_date}')

    doc_time_hour = int(doc_time.split(':')[0])
    doc_time_minute = int(doc_time.split(':')[1].split(' ')[0])

    current_time_hour = int(current_time.split(':')[0])
    current_time_minute = int(current_time.split(':')[1].split(' ')[0])

    print(f'DOC TIME HOUR: {doc_time_hour}')
    print(f'DOC TIME MINUTE: {doc_time_minute}')

    print(f'CURRENT TIME HOUR: {current_time_hour}')
    print(f'CURRENT TIME MINUTE: {current_time_minute}')

    if doc_date == current_date:
        if ('AM' in doc_time and 'AM' in current_time) or ('PM' in doc_time and 'PM' in current_time) or ('AM' in current_time and 'PM' in doc_time):
            if doc_time_hour == current_time_hour:
                if doc_time_minute - current_time_minute >= 0 and doc_time_minute - current_time_minute <= 5:
                    return '1'
                elif doc_time_minute - current_time_minute < 0:
                    return '2'
                else:
                    return '0'
            elif current_time_hour - doc_time_hour == -1:
                if doc_time_minute <= 5 and current_time_minute >= 55:
                    return '1'
                else:
                    return '0'
            elif current_time_hour == 12 and doc_time_hour == 1:
                if doc_time_minute <= 4 and current_time_minute >= 55:
                    return '1'
                else:
                    return '0'    
            elif current_time_hour - doc_time_hour == 1:
                return '2'
            else:
                return '0'
        else:
            return '2'
    elif doc_date == tomorrow_date:
        if 'PM' in current_time and 'AM' in doc_time and current_time_hour == 11 and doc_time_hour == 12:
            if current_time_minute >= 55 and doc_time_minute <= 4:
                return '1'
            else:
                return '0'
        else:
            return '0'
    else:
        return '0'

    # if doc_time_hour == current_time_hour:
    #     if doc_time_minute - current_time_minute > 0 and doc_time_minute - current_time_minute <= 5:
    #         print('WITHIN 5 MINUTES')
    #     elif doc_time_minute - current_time_minute < 0:
    #         print('OVERTIME')
    #     else:
    #         print('EARLY')
    # elif doc_time_hour - current_time_hour == -1 and doc_time_minute >= 50 and current_time_minute <= 10:
    #     print('POTENTIALLY OVERTIME, CHECK DB')
    # need cases for 12 and 1 along with comparing date if it today is the same day as the tourney and if today is the day after but in early am i.e. just after 12am 


def check_tourney_time_interface():
    dbname = get_database()
    collection_name = dbname["tournaments"]

    current_time, current_date, tomorrow_date = get_currTime()
    all_docs = collection_name.find()

    delete_list = []
    check_list = []
    rewrite_list = []

    for doc in all_docs:
        check_res = check_doc(doc['time'], doc['date'], current_time, current_date, tomorrow_date)

        if check_res == '0':
            print('Zero case hit, breaking')
            break
        elif check_res == '1':
            check_list.append(doc)
        else:
            delete_list.append(doc)

    if len(check_list) == 0:
        print('No entries need to be checked')
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        cmg_urls = []
        codagent_titles = []

        for entry in check_list:
            if entry['company'] == 'cmg':
                cmg_urls.append(entry['url'])
            else:
                codagent_titles.append(entry['title'])

        if len(codagent_titles) > 0:
            codagent_check_tourney_time(driver, codagent_titles)
        
        if len(cmg_urls) > 0:
            cmg_check_tourney_time(driver, cmg_urls)

        compare_timing(delete_list, check_list, rewrite_list, current_time)

        print(f'CMG URLS: {cmg_urls}')
        print(f'CODAGENT TITLES: {codagent_titles}')
        print(f'TIME: {times}')
        print(f'REWRITE LIST: {rewrite_list}')

    if len(delete_list) == 0:
        print('No entries need to be deleted')
    else:
        for entry in delete_list:
            collection_name.find_one_and_delete({"_id": entry['_id']})

    if len(rewrite_list) == 0:
        print('No entries need to be overwritten')
    else:
        for entry in rewrite_list:
            collection_name.find_one_and_replace({"_id": entry['_id']}, entry)


    return times

if __name__ == '__main__':
    check_tourney_time_interface()

