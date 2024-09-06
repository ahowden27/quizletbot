from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from credentials import USER, QUIZLETPASS

# Insert quizlet url here
URL = "https://quizlet.com/{id}/"

"""
TIMES
.465 - 3.8s
.5 - 4.0s
.7 - 4.9s
0.75 - 5.2s
1 - 6.4s
"""

termsList = {}
x = 0

# Set to your path
PATH = "/{PATH}/chromedriver"
chrome_options = Options()
driver = webdriver.Chrome(PATH)
driver.get("https://quizlet.com/login")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(USER + Keys.TAB)
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(QUIZLETPASS + Keys.ENTER)

time.sleep(.25)

driver.switch_to.new_window("tab")
driver.get(URL)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='TermText notranslate lang-en']")))

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2)")
time.sleep(2)

"""
CHANGE LANGUAGE ACCORDINGLY
"""
while True:
    try:
        termsList.update({driver.find_elements(By.XPATH, "//span[@class='TermText notranslate lang-fr']")[x].text: driver.find_elements(By.XPATH, "//span[@class='TermText notranslate lang-en']")[x].text})
        # termsList.update({driver.find_elements(By.XPATH, "//span[@class='TermText notranslate lang-en']")[x].text: driver.find_elements(By.XPATH, "//span[@class='TermText notranslate lang-en']")[x+1].text})
        x += 1
        # x += 2
    except:
        break

termsList.update({v: k for k, v in termsList.items()})
print(termsList)
driver.switch_to.new_window("tab")
driver.get(URL + "micromatch")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Start game']"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@style='display: block;']")))

while True:
    try:
        driver.find_elements(By.XPATH, "//div[@style='display: block;']")[0].click()
        value = driver.find_elements(By.XPATH, "//div[@style='display: block;']")[0].text
        for i in range(1, 12):
            try:
                if driver.find_elements(By.XPATH, "//div[@style='display: block;']")[i].text == termsList[value]:
                    driver.find_elements(By.XPATH, "//div[@style='display: block;']")[i].click()
            except:
                pass
        time.sleep(.545)
    except:
        break
print("done")
time.sleep(10)
