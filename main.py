from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# needs integration with all modern browsers
# 1) Firefox
# 2) Google Chrome
# 3) Microsoft Edge
# 4) Apple Safari
# 5) Opera


driver = webdriver.Chrome('./chromedriver')
driver.get("https://www.python.org")

print(driver.title)