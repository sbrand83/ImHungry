from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# have to do this because the Firefox 47 didn't work with the Selenium 2.53
# driver
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
firefox_capabilities['binary'] = '/usr/bin/firefox'

browser = webdriver.Firefox(capabilities=firefox_capabilities)

# Stefan and his friends are SUPER hungry.  There are restaurants all over the place
# but none of them really stand out.  There is an extreme case of indecisiveness that can
# not be cure. But luckily there is a cool webapp called ImHungry to save the day.

# Stefan opens up his browser and goes to ImHungry.domainnamethathasnotbeendecidedorboughtyet
browser.get('http://localhost:8000')

# Stefan can see the title of the page says "I'm Hungry!"
assert "I'm Hungry!" in browser.title

# Stefan sees a big header at the top that says "I'm Hungry!"

# Stefan sees that his location has been found

# There is a map in the center of the screen that shows this location

browser.quit()
