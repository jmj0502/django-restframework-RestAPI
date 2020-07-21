from .test_setup import TestSetUp
from ..models import User
import pdb

"""In order to perform a deeper analisis to our test cases using pdb, we must run, at least, res, and res.data"""

class TestAPIViews(TestSetUp):
    def test_user_cant_register_without_providing_info(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)


    def test_user_registration(self):
        res = self.client.post(self.register_url, data=self.user_data)
        #pdb.set_trace()
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    
    def test_user_cant_login_if_emai_not_verified(self):
        self.client.post(self.register_url, data=self.user_data)
        res= self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(res.status_code, 401)

    
    def test_user_can_login_if_email_is_verified(self):
        response = self.client.post(self.register_url, data=self.user_data)
        email = response.data['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res = self.client.post(self.login_url, data=self.user_data)
        self.assertEqual(res.status_code, 200)