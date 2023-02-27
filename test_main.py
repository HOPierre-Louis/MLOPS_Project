import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_predict(self):
        data={'Title': 'Naruto', 'Genre': 'Action, Adventure, Romance', 'Synopsis': 'In the year 2071, humanity has colonized the monkeys with fire', 'Type': '', 'Producer': 'Bandai Visual', 'Studio': 'Madhouse'}
        response = self.app.post('/predict_test/', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Rating": 6.7481600394244206})
        
if __name__ == '__main__':
    unittest.main()
