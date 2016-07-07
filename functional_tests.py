from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# have to do this because the Firefox 47 didn't work with the Selenium 2.53
# driver
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

#display = Display(visible=0, size=(1024, 768))
#display.start()

browser = webdriver.Firefox(capabilities=firefox_capabilities)
browser.get('http://localhost:8000')

assert 'Django' in browser.title

browser.quit()
#display.stop()
