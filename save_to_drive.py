from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import config

usr = config.USR
pw = config.PW

#Log in to google account
print('Logging into account`')
driver = webdriver.Chrome()
driver.get('https://www.drive.google.com')
time.sleep(1)
driver.find_element_by_xpath('/html/body/section/div[2]/div/a').click()
time.sleep(1)
elem = driver.find_element_by_id('identifierId')
elem.send_keys(usr + Keys.ENTER)
time.sleep(1)
elem = driver.find_element_by_name('password')
elem.send_keys(pw + Keys.ENTER)

time.sleep(2)
#Upload to Google Drive
# print('Uploading to Google Drive')
# elem = driver.find_element_by_xpath('//*[@id="drive_main_page"]/div[2]/div/div[1]/div/div/div[3]/div[1]/div/button[1]/div[2]')
# time.sleep(1)
# elem.click()
# time.sleep(1)
# actions = ActionChains(driver)

# actions.send_keys(Keys.DOWN * 2 + Keys.ENTER)
# actions.perform()
driver.find_element_by_css_selector('#drive_main_page > div.a-qc-La.sd-ph > div > div.a-s-tb-sc-Ja-Q.a-s-tb-sc-Ja-Q-Nm.a-s-tb-Pe-Q.a-D-Pe-Q > div > div > div.a-D-B-x > div.a-D-B-Lc-j > div > button.RTMQvb.Kzazxf.fCmhtc.hc0pBf.x6jRSb.a-qb-d.h-sb-Ic.sXaDqb')
# elem.send_keys('./FULL_MAP.png')
time.sleep(10)


driver.quit()