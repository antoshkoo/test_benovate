from django.test import TestCase
from django.urls import reverse

from app_users.forms import CustomUserCreationForm, CustomUserChangeForm
from app_users.models import CustomUser

USER_DATA = {
    'username': 'testuser',
    'password1': 'password',
    'password2': 'password',
    'tin': '00000000000'
}


class CustomUserCreationFormTest(TestCase):
    def test_user_creation_form_valid(self):
        form = CustomUserCreationForm(data=USER_DATA)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_labels(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['password1'].label, 'Password')
        self.assertEqual(form.fields['password2'].label, 'Password confirmation')
        self.assertEqual(form.fields['tin'].label, 'TIN')

    def test_user_creation_form_post(self):
        response = self.client.post(reverse('user_register_url'), USER_DATA)
        self.assertRedirects(response, reverse('main_url'), status_code=302, target_status_code=200)


class CustomUserChangeFormTest(TestCase):
    def test_user_change_form_valid(self):
        form = CustomUserChangeForm(data=USER_DATA)
        self.assertTrue(form.is_valid())

    def test_user_change_form_labels(self):
        form = CustomUserChangeForm()
        self.assertEqual(form.fields['tin'].label, 'TIN')
        self.assertEqual(form.fields['email'].label, 'Email address')

    def test_user_change_form_post(self):
        user = CustomUser.objects.create_user(username=USER_DATA['username'], password=USER_DATA['password1'])
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password1'])
        response = self.client.post(reverse('user_profile_url', kwargs={'pk': user.pk}), USER_DATA)
        self.assertRedirects(response, reverse('user_profile_url', kwargs={'pk': user.pk}), status_code=302, target_status_code=200)
