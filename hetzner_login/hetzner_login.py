from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time 
import sys

username       = os.environ.get('USERNAME')
password       = os.environ.get('PASSWORD')
submit         = "submit-login"
project        = os.environ.get('PROJECT')
permissions    = os.environ.get('PERMISSIONS') # Valid inputs: "Read" "Read & Write"
member         = os.environ.get('MEMBER')
member_role    = os.environ.get('MEMBER_ROLE') # valid inputs: "admin" "member" "restricted"

# check if USERNAME, PASSWORD or PROJECT exists

if username is None:
  print("No username for Hetzner Login has been set. Aborting script...")
  sys.exit()

if password is None:
  print("No password for Hetzner Login has been set. Aborting script...")
  sys.exit()

if project is None:
  print("No project name has been set. Aborting script...")
  sys.exit()

# assign default permissions to Read & Write if not passed.

permissions = permissions or "Read & Write"

# initialize the Chrome  driver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

# call Hcloud login page and pass credentials
driver.get("https://console.hetzner.cloud")
driver.find_element(By.ID, "_username").send_keys(username)
driver.find_element(By.ID, "_password").send_keys(password)
driver.find_element(By.ID, submit).click()

# wait the ready state to be complete
time.sleep(1.5)

# check if login has been succesfully
try:
    driver.find_element(By.XPATH, "//hc-app[1]")
except Exception:
    print("Login failed")
    sys.exit()




# create a new Project
def create_project():

    # check if Project already exists
    project_names = driver.find_elements(By.XPATH, "(//*[contains(@class, 'project-card__name ng-tns')])")
    project_exists = ""
    for i in project_names:
        if project == i.text:
            project_exists = "exists"
            break
    if project_exists == "exists":
      print("Project already exists. Can't create a Project with the same name. Aborting script...")
      sys.exit()
    
    # create Hetzner project

    new_project = driver.find_element(By.CSS_SELECTOR, "[id^='PAGE_CONTENT-PROJECTS-ADD_PROJECT_BTN']")
    new_project.click()
    driver.find_element(By.ID, "name").send_keys(project)
    confirm = driver.find_element(By.CSS_SELECTOR, "[id^='PAGE_CONTENT-PROJECTS-CONFIRM-ADD_BTN']")
    confirm.click()


## enter a Hetzner Project
def enter_project():

    project_names = driver.find_elements(By.XPATH, "(//*[contains(@class, 'project-card__name ng-tns')])")
    project_exists = ""

    for i in project_names:
        if project == i.text:
            i.click()
            time.sleep(1)
            project_exists = "exists"
            break
    if project_exists != "exists":
        print("Project not found")
        sys.exit()


### Member Invitation Management
def send_member_invitation():

    if member is None:
      print("No Member name has been set. Aborting script...")
      sys.exit()

    if member_role is None:
      print("No Member Role has been set. Aborting script...")
      sys.exit()

    

    member_config = driver.find_elements(By.XPATH, "(//*[contains(@class, 'ng-star-inserted')])")
    for n in member_config:
        print(n.text)
        if "ADD MEMBER" == n.text:
            
            n.click()
            time.sleep(1)

            actions = ActionChains(driver)
            actions.send_keys(member)
            actions.send_keys(Keys.TAB)
            
            if member_role == "admin":
                actions.send_keys(Keys.UP)

            if member_role == "restricted":
                actions.send_keys(Keys.DOWN)
            
            actions.send_keys(Keys.ENTER) # lock in member role
            actions.send_keys(Keys.ENTER) # send invitation
            actions.perform()
            time.sleep(1.5)
            break
## API Token generation
def generate_api_token():

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
                print(api_token)
        break

# create a Hetzner Project
create_project()
time.sleep(1)

# enter the project and define navigation URLs
enter_project()
project_url = '/'.join(driver.current_url.split("/")[:-1])
token_url = project_url+"/security/tokens"
member_url = project_url+"/security/members"

# navigate to security/tokens and generate the api token
driver.get(token_url)
time.sleep(1)
generate_api_token()

# navigate to security/tokens and add member to the Project
# driver.get(member_url)
# time.sleep(1)
# send_member_invitation()


# close the driver
driver.close()