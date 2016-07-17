from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import testing_settings
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # have to do this because the Firefox 47 didn't work with the Selenium 2.53
        # driver
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['binary'] = '/usr/bin/firefox'

        profile = webdriver.FirefoxProfile()
        profile.set_preference("geo.prompt.testing", True)

        # allows geolocation if setting enabled from testing_settings
        profile.set_preference("geo.prompt.testing.allow", testing_settings.GEOLOCATION_ENABLED)

        self.browser = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=profile)
        self.browser.implicitly_wait(3) #waits up to 3 seconds to check everything

    def tearDown(self):
        self.browser.quit()

    def test_can_find_random_restaurant_and_get_directions(self):
        # Stefan and his friends are SUPER hungry.  There are restaurants all over the place
        # but none of them really stand out.  There is an extreme case of indecisiveness that can
        # not be cure. But luckily there is a cool webapp called ImHungry to save the day.

        # Stefan opens up his browser and goes to ImHungry.domainnamethathasnotbeendecidedorboughtyet
        self.browser.get('http://localhost:8000')

        # Stefan can see the title of the page says "I'm Hungry!"
        self.assertIn("I'm Hungry!", self.browser.title)

        # Stefan sees a big header at the top that says "I'm Hungry!"
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("I'm Hungry!", header_text)

        # Stefan sees that his location has been found
        location_text = self.browser.find_element_by_id('location_text').text
        self.assertIn('Your Location:', location_text)

        # If the location is not found or there is another error, there is a
        # text input to manually enter in the current location.
        location_error = self.browser.find_element_by_id('location_error')
        location_input = self.browser.find_element_by_id('location_input')

        if not testing_settings.GEOLOCATION_ENABLED:
            print('Geolocation disabled')

            self.assertNotIn('hidden', location_error.get_attribute("class").split())
            self.assertNotIn('hidden', location_input.get_attribute("class").split())

            self.assertEqual(
                    location_input.get_attribute('placeholder'),
                    'Enter your location'
            )
        else:
            print('Geolocation enabled')

            self.assertIn('hidden', location_error.get_attribute("class").split())
            self.assertIn('hidden', location_input.get_attribute("class").split())


        # The page gets redirected to show a map
        self.fail("Finish the tests!")

        # There is a map in the center of the screen that shows this location
        the_map = self.browser.find_element_by_id('map')
        self.assertIsNotNone(the_map)

        # There is button that when clicked picks a random restaurant

        # The location of the restaurant is displayed on the map

        # Information about the restaurant appears below the map

        # There are directions to the restaurant from Stefan's current location
        # on the map

if __name__ == '__main__':
    unittest.main(warnings='ignore')
