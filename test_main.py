import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_predict(self):
        print('----------------------')
        data =  {
            "Title": "Naruto", 
            "Genre": "Action, Adventure, Romance", 
            "Synopsis": "In the year 2071, humanity has colonized the monkeys", 
            "Type": "TV", 
            "Producer": "['Bandai Visual']", 
            "Studio": "['Madhouse']"
        }
        
        response = self.app.post('/predict', json=data)
        print(data)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Rating": 6.7481600394244206})
        
if __name__ == '__main__':
    unittest.main()
