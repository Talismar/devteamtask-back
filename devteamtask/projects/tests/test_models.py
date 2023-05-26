from django.test import TestCase


# Learning tests in python
class UserTestCase(TestCase):
    def test_user_create(self):
        print("User created")
        self.assertEqual(1, 1)
