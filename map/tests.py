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

    def test_redirect_to_home_if_missing_lat_or_lng(self):
        client = self.client

        # with no GET parameters, should redirect back home
        response = client.get('/map')
        self.assertRedirects(response, '/')

        # missing lng
        response = client.get('/map', {'lat': 20})
        self.assertRedirects(response, '/')

        # missing lat
        response = client.get('/map', {'lng': 20})
        self.assertRedirects(response, '/')
    def test_redirect_if_coordinates_invalid(self):
        client = self.client

        # lat invalid if abs(lat) > 90

        # lat > 90
        response = client.get('/map', {'lat': 90.1, 'lng': 50})
        self.assertRedirects(response, '/')

        # lat < -90
        response = client.get('/map', {'lat': -90.1, 'lng': 50})
        self.assertRedirects(response, '/')


        # lng invalid if abs(lng) > 180

        # lng > 180
        response = client.get('/map', {'lat': 20, 'lng': 180.1})
        self.assertRedirects(response, '/')

        # lng < -180
        response = client.get('/map', {'lat': 20, 'lng': -180.1})
        self.assertRedirects(response, '/')
