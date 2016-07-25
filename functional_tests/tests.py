from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def tearDown(self):
        self.browser.quit()

    def wait_for_element_with_id(self, element_id):
        return WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, element_id)))

    def wait_for_element_with_class(self, element_class):
        WebDriverWait(self.browser, timeout=10).until(
                lambda b: b.find_element_by_class_name(element_class)
        )

    def wait_for_class_on_given_element(self, element_class, element):
        WebDriverWait(self.browser, timeout=10).until(
                lambda b: element_class in element.get_attribute('class')
        )

    def wait_for_class_not_on_given_element(self, element_class, element):
        WebDriverWait(self.browser, timeout=10).until(
                lambda b: element_class not in element.get_attribute('class')
        )

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
        #location_text = self.wait_for_element_with_id('location_text').text
        location_text = self.browser.find_element_by_id('location_text').text
        self.assertIn('Your Location:', location_text)

        # If the location is not found or there is another error, there is a
        # text input to manually enter in the current location.
        location_error = self.browser.find_element_by_id('location_error')
        location_form = self.browser.find_element_by_id('location_form')
        lat_input = self.browser.find_element_by_id('lat_input')
        lng_input = self.browser.find_element_by_id('lng_input')


        # With geolocation disabled, it is certain that the user will have to manually
        # type in their location

        if not testing_settings.GEOLOCATION_ENABLED:
            print('Geolocation disabled')

            self.wait_for_class_not_on_given_element("hidden", location_form)
            self.assertTrue(location_form.is_displayed())

            self.assertEqual(
                    lat_input.get_attribute('placeholder'),
                    'Enter your latitude'
            )
            self.assertEqual(
                    lng_input.get_attribute('placeholder'),
                    'Enter your longitude'
            )

            # enter data into the form manually (Chicago)
            lat_input.send_keys('41.875206')
            lng_input.send_keys('-87.630556')

            # submit the form as POST request
            lng_input.send_keys(Keys.ENTER)

        else:
            # Eventhough geolocation is enabled does not mean that the location will
            # be successfully found. Need to also check for an error before checking
            # that input form is hidden.

            print('Geolocation enabled')

            try:
                # try to find if error message is present, throws exception if
                # the error is hidden and does tests for successful geolocation

                # wait to see if error message will become unhidden, if not times out
                # TODO: this causes the successful case to wait for timeout period
                # would be better if only had to wait when it failed
                self.wait_for_class_not_on_given_element('hidden', location_error)

                print('Geolocation failed')

                # the form should also be visible
                self.wait_for_class_not_on_given_element("hidden", location_form)
                self.assertTrue(location_form.is_displayed())

                self.assertEqual(
                        lat_input.get_attribute('placeholder'),
                        'Enter your latitude'
                )
                self.assertEqual(
                        lng_input.get_attribute('placeholder'),
                        'Enter your longitude'
                )

                # enter data into the form manually (Chicago)
                lat_input.send_keys('41.875206')
                lng_input.send_keys('-87.630556')

                # submit the form as POST request
                lng_input.send_keys(Keys.ENTER)

            except TimeoutException:
                # On success
                self.wait_for_class_on_given_element("hidden", location_form)

                # checks that the element is actually hidden
                self.assertFalse(location_form.is_displayed())

                # user can see current location in lat/lng coords
                self.assertIn('lat', lat_text)
                self.assertIn('lng', lng_text)

        # The page gets redirected to show a map
        the_map = self.browser.find_element_by_id('map')

        # There is a map in the center of the screen that shows this location
        self.fail("Finish the tests!")
        self.assertIsNotNone(the_map)

        # There is button that when clicked picks a random restaurant

        # The location of the restaurant is displayed on the map

        # Information about the restaurant appears below the map

        # There are directions to the restaurant from Stefan's current location
        # on the map

if __name__ == '__main__':
    unittest.main(warnings='ignore')
