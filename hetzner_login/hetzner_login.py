from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import time 

username       = os.environ.get('USERNAME')
password       = os.environ.get('PASSWORD')
submit         = "submit-login"
project        = os.environ.get('PROJECT')
permissions    = os.environ.get('PERMISSIONS') # Valid inputs: "Read" "Read & Write"
email_member   = os.environ.get('EMAIL_MEMBER')
member_role    = os.environ.get('MEMBER_ROLE') # valid inputs: "admin" "member" "restricted"

# initialize the Chrome  driver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

driver.get("https://console.hetzner.cloud")
driver.find_element(By.ID, "_username").send_keys(username)
driver.find_element(By.ID, "_password").send_keys(password)
driver.find_element(By.ID, submit).click()

# wait the ready state to be complete
time.sleep(1.5)


#create a new Project
def create_project():
    new_project = driver.find_element(By.CSS_SELECTOR, "[id^='PAGE_CONTENT-PROJECTS-ADD_PROJECT_BTN']")
    new_project.click()
    driver.find_element(By.ID, "name").send_keys(project)
    confirm = driver.find_element(By.CSS_SELECTOR, "[id^='PAGE_CONTENT-PROJECTS-CONFIRM-ADD_BTN']")
    confirm.click()


## construct Project URL
def get_project():

    project_exists = ""
    project_names = driver.find_elements(By.XPATH, "(//*[contains(@class, 'project-card__name ng-tns')])")

    for i in project_names:
        if project in i.text:
            i.click()
            time.sleep(1)
            project_exists = "exists"
            project_url = '/'.join(driver.current_url.split("/")[:-1])
            driver.get(project_url)
            break
    if project_exists != "exists":
        create_project()
        time.sleep(1)
        get_project()

### Member Invitation Management
def send_member_invitation():
    member_config = driver.find_elements(By.XPATH, "(//*[contains(@class, 'ng-star-inserted')])")
    for n in member_config:
        if "Add member" in n.text:
            n.click()
            time.sleep(1)

            actions = ActionChains(driver)
            actions.send_keys(email_member)
            actions.perform()

            role = driver.find_elements(By.XPATH, "(//*[contains(@class, 'ng-star-inserted')])")
            for o in member_config:
                if member_role in o.text:
                    o.click()
                    time.sleep(1)
            send_invitation = driver.find_elements(By.XPATH, "(//*[contains(@class, 'ng-star-inserted')])")
            for p in member_config:
                if "Send Invitation" in p.text:
                    p.click()
                    time.sleep(1) 
            break

## API Token generation
def get_api_token():

    api_generate = driver.find_elements(By.XPATH, "(//*[contains(@class, 'hc-button ng-tns')])")
    for j in api_generate:
        j.click()
        api_dscr = driver.find_elements(By.XPATH, "(//*[contains(@id, '__hc-field')])")
        for k in api_dscr:
            k.send_keys(project)
            api_read_write = driver.find_elements(By.XPATH, "(//span[contains(@class, 'hc-radio__label')])")
            for l in api_read_write:
                if permissions in l.text:
                    l.click()
            api_generate_token = driver.find_elements(By.XPATH, "(//span[contains(@class, 'ng-star-inserted')])")
            for m in api_generate_token:
                if "GENERATE API TOKEN" in m.text:
                    m.click()
                    time.sleep(1)
            api_token_list = driver.find_elements(By.XPATH, "(//span[contains(@class, 'click-to-copy__content')])")
            for element in api_token_list:
                api_token = element.text
                f = open("/home/seluser/hetzner_api_token/HETZNER_API_TOKEN", "w")
                f.write(api_token)
                f.close()
        break

get_project()
project_url = '/'.join(driver.current_url.split("/")[:-1])
token_url = project_url+"/security/tokens"
member_url = project_url+"/security/members"
time.sleep(1)
driver.get(token_url)
time.sleep(1)
get_api_token()

# close the driver
driver.close()