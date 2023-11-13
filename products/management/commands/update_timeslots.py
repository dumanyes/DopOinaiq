from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import TimeSlot

class Command(BaseCommand):
    help = 'Update time slots to make them available again when their end time has passed.'

    def handle(self, *args, **options):
        current_time = timezone.now()
        TimeSlot.objects.filter(end_time__lt=current_time, available=False).update(available=True)
        self.stdout.write(self.style.SUCCESS('Updated time slots.'))