from django.test import TestCase
from django.urls import reverse

from app_users.models import CustomUser

LOAD_DATA = ['users_data.json']

USER_DATA = {
    'username': 'Tor',
    'password': '123',
    'tin': '845643278458',
}

USER_DATA_BOSS = {
    'username': 'admin',
    'password': 'admin',
}

USERS_TIN = ['912300012932', '912300012932', '28343746374', '123928349', '111']


class MoneySendLogicTest(TestCase):
    fixtures = LOAD_DATA

    def test_money_send_user_recipients_with_duplicates(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.post(reverse('send_money_url'), data={
            'sender': USER_DATA['tin'],
            'recipients': USERS_TIN[:3],
            'sum': 1
        })

        self.assertContains(response, 'TIN duplicated in recipients list')

    def test_money_send_user_recipients_not_found(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.post(reverse('send_money_url'), data={
            'sender': USER_DATA['tin'],
            'recipients': USERS_TIN[4],
            'sum': 1
        })

        self.assertContains(response, f'Recipient not found -')

    def test_money_send_user_no_balance(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.post(reverse('send_money_url'), data={
            'sender': USER_DATA['tin'],
            'recipients': USERS_TIN[0],
            'sum': 10000000000
        })

        self.assertContains(response, 'Please charge balance')

    def test_money_send_to_yourself(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.post(reverse('send_money_url'), data={
            'sender': USER_DATA['tin'],
            'recipients': USER_DATA['tin'],
            'sum': 1
        })

        self.assertContains(response, 'send money to yourself')

    def test_money_send_correct_round_and_receive(self):
        self.client.login(username=USER_DATA['username'], password=USER_DATA['password'])

        response = self.client.post(reverse('send_money_url'), data={
            'sender': USER_DATA['tin'],
            'recipients': USERS_TIN[1:4],
            'sum': 100
        })

        self.assertContains(response, 'Money was send')

        user = CustomUser.objects.get(tin=USERS_TIN[1])
        self.assertEqual(float(user.balance), 1033.33)

        user = CustomUser.objects.get(tin=USERS_TIN[2])
        self.assertEqual(float(user.balance), 2033.33)

        user = CustomUser.objects.get(tin=USERS_TIN[3])
        self.assertEqual(float(user.balance), 533.33)

        user = CustomUser.objects.get(tin=USER_DATA['tin'])
        self.assertEqual(float(user.balance), 4900.01)
