from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profiles.models import UserPreference


@receiver(post_save, sender=get_user_model())
def create_prefs_with_users(sender, instance, **kwargs):
    """ Automatically create User preferences when a new django User is
    created.
    """

    UserPreference.objects.get_or_create(user=instance)
