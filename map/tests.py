from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string

from map.views import home_page

fake_lat = 39.483070
fake_lng = -87.323493

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

#    def test_home_page_button_redirects_to_map(self):
#        client = self.client
#
#        response = self.client.get('/')
#
#        # click "Find restaurants around me"ish button to be redirected
#        url_params = '?lat={lat}&lng={lng}'.format(lat=fake_lat, lng=fake_lng)

class MapPageTest(TestCase):

    def test_map_page_initialize_with_coords(self):
        client = self.client
        response = client.get('/map', {'lat': fake_lat, 'lng': fake_lng})

        self.assertContains(response, 'lat={lat}'.format(lat=fake_lat))
        self.assertContains(response, 'lng={lng}'.format(lng=fake_lng))
