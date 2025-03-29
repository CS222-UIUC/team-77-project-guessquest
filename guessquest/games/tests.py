from django.test import TestCase
from . import services
# Create your tests here.


class WeatherApiTest(TestCase):
    def test_city_to_coords(self):
        lat, lon = services.city_to_coords("Champaign")
        self.assertTrue(40.0 < lat < 40.2)
        self.assertTrue(-88.3 < lon < -88.2)
        print(f"{lat}, {lon}")
    