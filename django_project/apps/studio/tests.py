from django.test import SimpleTestCase
from django.urls import resolve


class StudioRouteTests(SimpleTestCase):
    def test_studio_route(self):
        self.assertEqual(resolve("/studio/").url_name, "studio-home")

    def test_games_entry_route(self):
        self.assertEqual(resolve("/games/").url_name, "games")
