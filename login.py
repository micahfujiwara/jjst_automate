from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import yaml
from yaml import FullLoader
import subprocess


def gmail_login(driver):
    email, password = get_gmail_info()
    gmail_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[2]/div[2]/div/input[1]")))
    gmail_email.clear()
    gmail_email.send_keys(email)
    nextButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div[3]/div/div/div/div[4]/div/div/div/div[2]/input")))
    nextButton.click()
    password_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[2]/input")))
    password_box.clear()
    password_box.send_keys(password)
    sign_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span")))
    sign_in_button.click()
    textButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div")))
    textButton.click()
    time.sleep(10)
    
    verification_code = wait_for_new_message()
    print(verification_code)
    # if verification_code:
    #     verification_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "...")))
    #     verification_input.clear()
    #     verification_input.send_keys(verification_code)
    # else:
    #     print("Verification code not received within the timeout period.")
        


def wait_for_new_message():
    # Your AppleScript code here
    applescript_code = """
    tell application "System Events"
        -- Access and process the last notification
        set latestNotification to item 1 of (sort (every notification of every process whose (title of it contains "Messages" or title of it contains "Messages (iCloud)")) by id)

        set notificationText to text of latestNotification
        if notificationText contains "Use verification code" and notificationText contains "for Microsoft authentication" then
            set verificationCode to extract_verification_code(notificationText)
            if verificationCode is not "" then
                return verificationCode
            end if
        end if
    end tell

    return ""

    -- Extract verification code from text
    on extract_verification_code(notificationText)
        -- Search for the verification code in the notification text
        set AppleScript's text item delimiters to space
        set textItems to text items of notificationText
        set verificationCode to ""
        repeat with anItem in textItems
            if anItem is "code" then
                set verificationCode to item (offset of anItem) + 2 of textItems
                exit repeat
            end if
        end repeat
        set AppleScript's text item delimiters to ""
        return verificationCode
    end extract_verification_code
    """
    
    process = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=applescript_code)
    
    print("stdout:", stdout)
    print("stderr:", stderr)
    verification_code = stdout.strip()
    print("got here")
    print(verification_code)
    print("verification code should be above")
    return verification_code






def get_gmail_info():
    with open('micahinfo.yaml') as config_file:
        ydata = yaml.load(config_file, Loader = FullLoader)
    
    email = ydata['email']
    password = ydata['password']

    return email, password
