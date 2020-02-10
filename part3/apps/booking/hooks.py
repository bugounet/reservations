from websocket import create_connection


from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking

@receiver(post_save, sender=Booking)
def trigger_wesocket_event(sender, instance, *args, **kwargs):
    socket = create_connection('ws://localhost:8001')
    socket.send(b'%d//%d'%(instance.pk, instance.resource_id))
    socket.close()
