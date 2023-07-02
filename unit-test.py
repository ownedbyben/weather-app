import requests
import unittest


class Test(unittest.TestCase):
    def test_reachable(self):
        url = "http://localhost:5000/"
        # response = requests.get(url)
        try:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)

            # If the response was successful, no Exception will be raised
            # response.raise_for_status()

        except Exception as unreachable:
            print(f'http error, web isnt reachable: {unreachable}')




if __name__ == '__main__':
    unittest.main()
    