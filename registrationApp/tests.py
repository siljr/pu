from django.test import TestCase
from django.core.urlresolvers import reverse


class RegisterAppTestCase(TestCase):
    # Test to see if the status code is OK for the registerApp page
    def test_register_respone(self):
        response = self.client.get(reverse('questions:index'), follow= True)
        # 200 = evrything ok
        #print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)

    #Test to see if form restrictions work
    def test_register_user(self):
        response = self.client.post('/register/',
                                    {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                                     'password2': 'test'}, follow=True)
        #print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)

    # wrong password twice
    # valid email
    # username not taken
    def test_register_password_error(self):
        response = self.client.post('/register/',
                                    {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                                     'password2': 'test1'}, follow=True)
        self.assertNotEqual(response.request['PATH_INFO'], 'login')

    def test_register_username_error(self):
        self.client.post('/register/',
                                    {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                                     'password2': 'test'}, follow=True)

        response2 = self.client.post('/register/',
                                    {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                                     'password2': 'test'}, follow=True)

        self.assertNotEqual(response2.request['PATH_INFO'], 'login')

    def test_register_email_error(self):
        response = self.client.post('/register/',
                                    {'username': 'test', 'email': 'test@test', 'password1': 'test',
                                     'password2': 'test1'}, follow=True)
        self.assertNotEqual(response.request['PATH_INFO'], 'login')
