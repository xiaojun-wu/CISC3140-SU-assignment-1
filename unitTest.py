import unittest
import test
import json
import datetime
import requests


class webTest(unittest.TestCase):
    currentTime = datetime.datetime.now().date()
    date = "&date=" + currentTime.strftime("%Y-%m-%d")
    url = 'https://api.nasa.gov/planetary/apod?api_key=ybnJWsrHUoT6QlQLuRpYQ5n0IkwkN7p2m5tvn5Ef'

    render_templates = False

    def setUp(self):
        self.app = test.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        home = self.app.get('/')
        self.assertIn('Hello, welcome to the NASA APOD alternative website!',str(home.data))
        #self.assertEqual(' ',home.data)

    def test_nasa_page(self):
        response = self.app.get('/nasa')
        URL = self.url + self.date
        r = requests.get(URL)
        jData = r.json()
        title = jData['title']
        explanation = jData['explanation']
        mediaURL = jData['url']
        self.assertIn(str.encode(title),response.data)
        #self.assertIn(explanation,response.data)
        self.assertIn(str.encode(mediaURL),response.data)


if __name__== "__main__":
    unittest.main()
