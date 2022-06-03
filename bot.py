
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
import time
from selenium.webdriver.common.by import By
from telegram_notif import send_telegram_message
from dotenv import load_dotenv
import logging
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.environ.get('api_key')
chat_id = os.environ.get('chat_id')

print(api_key)


option = webdriver.ChromeOptions()

# You will need to specify the binary location for Heroku 
option.binary_location = os.getenv('GOOGLE_CHROME_BIN')

option.add_argument("--headless")
option.add_argument('--disable-gpu')
# option.add_argument('--no-sandbox')
browser = webdriver.Chrome(service=Service(os.getenv('CHROME_EXECUTABLE_PATH')), options=option)


is_liquidity = False
counter  = 1
while not is_liquidity:
    try:
        #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = firefox_options)
        driver = webdriver.Chrome(options = option)
        print("in while loop")
        # try:
        URL = 'https://v1.scream.sh/lend'
        driver.get(URL)
        print("proceeding to sleep")

        #time.sleep(40)
        wait = WebDriverWait(driver, 200)
        block = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[3]/div[2]/table/tbody/tr[18]/td[4]/div')))
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
    except TimeoutException:
        print("timedout")
    # except:
    #     is_liquidity = True
    #     driver.quit()
    #     send_email("something broke")
    #     break

