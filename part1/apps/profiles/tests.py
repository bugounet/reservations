import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from .models import UserPreference


class PreferencesTestCase(TestCase):
    def test_preferences_are_created_with_new_user(self):
        # assuming
        User = get_user_model()

        # when
        u = User.objects.create_user(username="toto")

        # then prefs are created
        self.assertTrue(UserPreference.objects.filter(user=u).exists())
        # AND access to preferences works
        self.assertIsNotNone(u.preferences.id)

    def test_user_prefs_are_initialized_with_paris_TZ(self):
        User = get_user_model()

        # when
        u = User.objects.create_user(username="toto")

        # then
        self.assertEqual(u.preferences._preferred_timezone, 'Europe/Paris')
        self.assertEqual(
            u.preferences.preferred_timezone,
            pytz.timezone('Europe/Paris')
        )

    def test_user_prefs_are_removed_on_user_delete(self):
        # assuming
        User = get_user_model()
        u = User.objects.create_user(username="toto")
        self.assertTrue(UserPreference.objects.filter(user=u).exists())

        # when
        u.delete()

        # then
        self.assertFalse(UserPreference.objects.filter(user=u).exists())
