# Selenium imports here
import csv
import time
from typing import List

# Other imports here
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def Excel1(listdata):
    # INIT EXCEL
    with open('mycsv.csv', 'w', newline='', encoding="utf-8") as f:
        fieldnames = ['instagram name', 'real name', 'account style', 'followers']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(listdata)

def CleanList(data):
    data_final_primary: List[any] = []
    data_final_secondary: List[any] = []

    print("begin cleaning")
    for elem in data:  # For Each list in list
        Business_flag = 0  # Bool for restricted accounts
        for value in elem:  # for each value within list of list
            if any(x in value.lower() for x in cleanout):  # if value matches any tag of restriction
                Business_flag = 1
        if Business_flag == 0:
            if elem not in data_final_secondary:  # if list value doesnt already exist

                data_final_secondary.append(elem)

    data_final_filtered = data_final_secondary
    print("clean version")
    print(data_final_filtered)

    Excel1(data_final_filtered)


def Scroll():
    n_scrolls = 10
    for i in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[2]/button'))).click()

        time.sleep(1)


def IterationTime(iteration, data):
    failsave = 0  # failsave variable

    for x in range(iteration):
        # time.sleep(60) #timer to avoid block

        driver.switch_to.window(driver.window_handles[0])

        driver.get("https://www.tiktok.com/search?q=" + data[x])

        Scroll()
        time.sleep(60)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        links = [a['href'] for a in soup.find_all('a', href=True)]

        links_final = [x for x in links if "@" in x and "https" not in x]

        del links_final[:56]
        links_final = [tiktok_link + x for x in links_final]

        driver.switch_to.window(driver.window_handles[1])

        for z in range(len(links_final)):  # len(links_final)

            driver.get(links_final[z])
            time.sleep(2)

            num = driver.find_elements \
                (By.XPATH, "//*[@id='app']/div[2]/div[2]/div/div[1]/h2[1]/div[2]/strong")

            if len(num) > 0:  # if num exists
                if num[0].text != 0:  # if num is not 0
                    if len(num[0].text) == 3:
                        followers = num[0].text.replace(',', '').replace('K', '000').replace('.', '').replace('M', '000000')
                    else:
                        followers = num[0].text.replace(',', '').replace('K', '00').replace('.', '').replace('M', '000000')

                # Criteria handling
                if 20000 > int(followers) > 900:

                    tiktok_name = links_final[z]
                    tiktok_name = tiktok_name[23:]

                    hyperlink_name = '=HYPERLINK("' + links_final[z] + '", "' + tiktok_name + '")'

                    likes_element = driver.find_elements(By.XPATH, ".//strong[@title='Likes']")
                    summary_element = driver.find_elements(By.XPATH, ".//h2[@class='tiktok-b1wpe9-H2ShareDesc e1awr0pt3']")
                    summary_element_fixed = summary_element[0].text.replace("\n", " ")
                    if bool(summary_element):
                        account_summary = summary_element_fixed
                    else:
                        account_summary = "N/A"

                    if bool(likes_element):
                        account_likes = likes_element[0].text
                    else:
                        account_likes = "N/A"

                    data_final.append([hyperlink_name, account_likes, account_summary, followers])

            print(data_final)

            if len(num) == 0:  # counter if follower search failed
                print("failed")
                failsave += 1
            elif failsave != 0:  # search succeed and counter reset if need be
                failsave = 0

            if failsave == 5:  # exit function dues to repeating error
                # print("error occured 5 times, exiting function")
                print("error occured on iteration #" + str(x) + " and on links/list number #" + str(
                    z) + " (this is after 5 fails)")
                return


tiktok_link = "https://www.tiktok.com"

tiktoktags = ["torontoinfluencer", "torontolife", "toronto", "torontotiktok", "tiktoktoronto",
           "torontoyyz", "torontofood", "torontoblogger", "todotoronto", "torontophotographer"]

hashtag = ["torontoinfluencer", "torontolife", "toronto", "nathanphillipssquare", "cntower",
           "torontostyle", "torontofood", "torontoblogger", "todotoronto", "torontophotographer"]

hashtag2 = ["downtowntoronto", "tastetoronto", "torontoeats", "torontocreator", "torontofashion",
            "torontoblogger", "yyzblogger", "torontofashionblogger"]

hashtag_test = ["tastetoronto"]

cleanout = ["restaurant", "store", "kitchen", "business", "fan page", "shop",
            "estate", "cafe", "eatery", "bakery", "pub", "bistro", "studio"
                                                                   "jewelry", "outlet", "company", "bar",
            "organization", "org",
            "retail", "agency", "fair", "event", "market", "buffet", "salon",
            "lease", "realtor"]

followers = "0"
tiktok_name = ""
list_final: List[any] = []
data_final: List[any] = []
data_final_filtered: List[any] = []

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(chrome_options=options,
                                     executable_path=r'C:\Users\User\Desktop\chrome webdriver/chromedriver.exe')

driver.get(tiktok_link)

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[0])

time.sleep(10)  # time to complete Captcha

IterationTime(len(tiktoktags), tiktoktags)
CleanList(data_final)
