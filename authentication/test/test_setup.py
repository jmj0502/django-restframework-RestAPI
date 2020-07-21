from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
# from faker import Faker

class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('authentication:registration')
        self.login_url = reverse('authentication:login')

        self.user_data = {
            'email': 'somedarkvoid@gmail.com',
            'username': 'deepstuff',
            'password': 'password12345'
        }

        return super().setUp
    

    def tearDown(self):
        return super().tearDown()