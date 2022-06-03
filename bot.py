# scraper.py

# importing selenium into code
from selenium import webdriver 
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os
import time
from selenium.webdriver.common.by import By
#from emailing import send_email
from telegram_notif import send_telegram_message


os.environ['GH_TOKEN'] = "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"

api_key = "5574894235:AAF7QfRpPBIc-__ceIeRAPZqkdncgWigI_0"
chat_id = 1383513208


# initialize the options
firefox_options = Options()
# add the argument headless
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-blink-features=AutomationControlled')



is_liquidity = False
counter  = 1
while not is_liquidity:
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = firefox_options)
    driver = webdriver.Firefox(options = firefox_options)

    # try:
    URL = 'https://v1.scream.sh/lend'
    driver.get(URL)
    time.sleep(30)
    #liquidity_usdc = driver.find_elements_by_xpath('/html/body/div[1]/div[4]/div/div[3]/div[2]/table/tbody/tr[18]/td[4]/div')
    liquidity_usdc = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/div[2]/table/tbody/tr[18]/td[4]/div')

    if float(liquidity_usdc.text) > 10:
        #send_email(f"liquidity is currently {liquidity_usdc.text}")
        send_telegram_message(f"liquidity is currently {liquidity_usdc.text}", chat_id, api_key)
        is_liquidity = True
    
    if counter == 15:
        #send_email(f"15 min update, liquidity is currently {liquidity_usdc.text}")
        send_telegram_message(f"15 min update, liquidity is currently {liquidity_usdc.text}", chat_id, api_key)
        counter = 1

    print(liquidity_usdc.text)
    time.sleep(30)
    driver.quit()
    counter += 1

    # except:
    #     is_liquidity = True
    #     driver.quit()
    #     send_email("something broke")
    #     break

