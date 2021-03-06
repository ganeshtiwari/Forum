from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..views import signup
from ..forms import SignUpForm
# Create your tests here.

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)


    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_signup_url_resolves_to_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
    
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
    

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'password1': '1234567',
            'password2': '1234567',
            'emial': 'john@gmail.com',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('board:home')
    
    # def test_redirection(self):
    #     self.assertRedirects(self.response, self.home_url)
    
    # def test_user_authentication(self):
    #     response = self.client.get(self.home_url)
    #     user = response.context.get('user')
    #     self.assertTrue(user.is_authenticated)
    

class InvalidSignUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
    
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'password1', 'password2', 'email']
        actual = list(form.fields)
        self.assertEquals(expected, actual)