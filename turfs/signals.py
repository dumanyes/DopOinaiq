# signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Booking, TimeSlot

@receiver(pre_delete, sender=Booking)
def update_timeslot_when_booking_deleted(sender, instance, **kwargs):
    if instance.time_slot:
        instance.time_slot.booked = False
        instance.time_slot.save()
