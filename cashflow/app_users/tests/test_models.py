from django.test import TestCase

from app_users.models import CustomUser

LOAD_DATA = ['users_data.json']


class TestCustomUserModel(TestCase):
    fixtures = LOAD_DATA

    def test_custom_user_model(self):
        user = CustomUser.objects.first()

        balance_label = user._meta.get_field('balance').verbose_name
        self.assertEquals(balance_label, 'Balance')

        tin_label = user._meta.get_field('tin').verbose_name
        self.assertEquals(tin_label, 'TIN')

        user = CustomUser.objects.create_user(username='user', password='user')
        self.assertEquals(user.balance, 0)
