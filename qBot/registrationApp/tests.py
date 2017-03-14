from django.test import TestCase
from django.core.urlresolvers import reverse
from .forms import RegistrationForm



class RegisterAppTestCase(TestCase):
    # Test to see if the status code is OK for the registerApp page
    def test_register_respone(self):
        response = self.client.get(reverse('questions:index'), follow= True)
        # 200 = evrything ok
        self.assertEqual(response.status_code, 200)

    def createUser(self):
        testUser = RegistrationForm()
        testUser.username('long')
        testUser.email('long@email.com')
        testUser.password1('long')
        testUser.password2('long')

    #Test to see if form restrictions work
    def test_register_user(self):
        self.assertEqual()
