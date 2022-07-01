import os
import time
import re
import csv
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

# Complete these 2 fields ==================
USERNAME = '####'
PASSWORD = '####'
TIMEOUT = 60
DRIVER_PATH = 'chromederiver'

def log_in():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--log-level=3")
        mobile_emulation = {
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        bot = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        bot.set_window_size(600, 1000)
        bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        user_element = WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')))
        user_element.send_keys(USERNAME)
        pass_element = WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')))
        pass_element.send_keys(PASSWORD)
        #logging in button click
        login_button = bot.find_element(By.XPATH, "//main/div/div/div/div[2]/form/div[1]/div[6]")
        time.sleep(0.4)
        login_button.click()
        time.sleep(5)
        print("Successfully Logged In")
        return bot
    except Exception as e:
        print(e)
        
        
def scrape_profile_followers(url):
    bot = log_in()
    try:
        bot.get(url)
        time.sleep(10)
        #finding followers button 
        main = bot.find_element(By.XPATH, "//main/div")
        a_tags = main.find_elements(By.XPATH, "//a[@href]")
        follower_button = ""
        for a_tag in a_tags:
            if "followers" in a_tag.text:
                follower_button = a_tag
                break
        time.sleep(0.4)
        follower_button.click()
        time.sleep(5)
        #scrolling
        scrolldown = bot.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        for i in range (0,99):
            try:
                time.sleep(1)
                scrolldown = bot.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            except:
                break
        time.sleep(2)
        followers = bot.find_elements_by_xpath('//main/div/ul/div/li/div/div[1]/div[2]/div[1]')
        usernames_list = []
        for  i in range(0,len(followers)):
            u = followers[i].text
            usernames_list.append(u)
        save_data(usernames_list)
    except Exception as e:
        print(e)
        
        
def scrape_post_likes(url):
    bot = log_in()
    try:
        bot.get(url+'liked_by/')
        time.sleep(10)

        #scrolling
        scrolldown = bot.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        for i in range (0,99):
            try:
                time.sleep(1)
                scrolldown = bot.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            except:
                break
        time.sleep(2)

        followers = bot.find_elements_by_xpath('//main/div[1]/div/div/div[2]/div[1]')
        usernames_list = []
        for  i in range(0,len(followers)):
            u = followers[i].text
            usernames_list.append(u)
        save_data(usernames_list)
        
    except Exception as e:
        print(e)
        

def save_data(usernames):
    csvFile = open('instagram_profiles.csv', 'w+')
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('username', 'url'))
        for i in range(len(usernames)):
            u = usernames[i]
            url_link = "https://www.instagram.com/"+u+"/"
            writer.writerow((u,url_link))
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
        
def main():
    try:
        n = int(input("Enter 1 to scrape followers from user profile\nEnter 2 to scrape likes from post\n"))
        if(n!=1 and n!=2):
            print("Please enter valid input")
        else:
            if(n==1):
                url = input("Enter profile url:")
                print("scraping profile followers..")
                scrape_profile_followers(url)
            elif(n==2):
                url = input("Enter post url:")
                print("scraping posts like..")
                scrape_post_likes(url)
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    main()