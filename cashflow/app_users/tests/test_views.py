from django.test import TestCase
from django.urls import reverse

LOAD_DATA = ['users_data.json']

USER_DATA = {
    'username': 'Tor',
    'password': '123',
}

USER_DATA_BOSS = {
    'username': 'admin',
    'password': 'admin',
}


class UserRegisterViewTest(TestCase):
    def test_user_register_page(self):
        response = self.client.get(reverse('user_register_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, '<h1>Sign Up</h1>')
        self.assertContains(response, 'Register</button>')


class UserLoginViewTest(TestCase):
    fixtures = LOAD_DATA

    def test_user_login_page(self):
        response = self.client.get(reverse('user_login_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, '<h1>Sign In</h1>')
        self.assertContains(response, 'Login</button>')

    def test_user_logged_redirect_login_page(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])
        response = self.client.get(reverse('user_login_url'))
        self.assertRedirects(response, reverse('main_url'), 302, target_status_code=200)


class UserLogoutViewTest(TestCase):
    def test_user_logout_page(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])
        response = self.client.get(reverse('user_logout_url'))
        self.assertRedirects(response, reverse('main_url'), 302, target_status_code=200)


class UserProfileViewTest(TestCase):
    fixtures = ['users_data.json']

    def test_user_not_logged_profile_page(self):
        response = self.client.get(reverse('user_profile_url', kwargs={'pk': 1}))
        next_url = reverse('user_login_url') + '?next=' + reverse('user_profile_url', kwargs={'pk': 1})
        self.assertRedirects(response, next_url, 302, target_status_code=200)

    def test_logged_user_profile_page(self):
        self.client.login(username=USER_DATA_BOSS['username'], password=USER_DATA_BOSS['password'])

        response = self.client.get(reverse('user_profile_url', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertContains(response, 'Save changes</button>')
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, '<h1>Hi, admin</h1>')
        self.assertContains(response, 'Balance: 100000.00')


class MoneySendViewTest(TestCase):
    fixtures = ['users_data.json']

    def test_user_not_logged_send_money_page(self):
        response = self.client.get(reverse('send_money_url'))
        next_url = reverse('user_login_url') + '?next=' + reverse('send_money_url')
        self.assertRedirects(response, next_url, 302, target_status_code=200)

    def test_logged_user_send_money_page(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.get(reverse('send_money_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('recipients_list' in response.context)
        self.assertFalse('senders_list' in response.context)
        self.assertTemplateUsed(response, 'send.html')
        self.assertContains(response, '<select name="recipients"')
        self.assertContains(response, '<input type="text" name="sum" placeholder="Amount"')
        self.assertContains(response, '<button type="submit">Confirm send</button>')
        self.assertContains(response, 'Balance: 5000.00')

    def test_logged_staff_user_send_money_page(self):
        self.client.login(username=USER_DATA_BOSS['username'], password=USER_DATA_BOSS['password'])

        response = self.client.get(reverse('send_money_url'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('recipients_list' in response.context)
        self.assertTrue('senders_list' in response.context)
        self.assertTemplateUsed(response, 'send.html')
        self.assertContains(response, '<select name="recipients"')
        self.assertContains(response, '<select name="sender"')
        self.assertContains(response, '<input type="text" name="sum" placeholder="Amount"')
        self.assertContains(response, '<button type="submit">Confirm send</button>')
        self.assertContains(response, 'Balance: 100000.00')