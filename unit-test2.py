import requests
import unittest

class Test(unittest.TestCase):
    def test_reachable(self):
        url = "http://localhost:5000/"
        try:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200, f"Expected status code 200 but received {response.status_code}")

        except Exception as unreachable:
            print(f'http error, web isnt reachable: {unreachable}')

if __name__ == '__main__':
    unittest.main()

