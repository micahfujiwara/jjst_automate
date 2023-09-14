from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# import undetected_chromedriver as uc
from login import *


def main():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
    
        driver.get('https://hawaiiantelcom.sharepoint.com/Workspaces/OMS/oe/Manual%20Tracking/Lists/JJST%20Tracking/AllItems.aspx?isAscending=false&viewid=7f46f417%2Dd7d3%2D435b%2D9795%2De303cedd2d6e')
        time.sleep(5)
        gmail_login(driver) 
        
        time.sleep(10)  
        input('hi')
        
    finally:
        driver.quit()
        
        
if __name__ == '__main__':
    main()
    
    
