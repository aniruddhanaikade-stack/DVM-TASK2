from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import Event, Slot


class Command(BaseCommand):
    help = "Adds some sample events"

    def handle(self, *args, **kwargs):
        if Event.objects.exists():
            self.stdout.write("Already has events")
            return

        now = timezone.now().replace(minute=0, second=0, microsecond=0)

        turf = Event.objects.create(name="Football Turf", kind="slot", place="City Sports Arena", price=500)
        court = Event.objects.create(name="Basketball Court", kind="slot", place="Hoops Club", price=300)
        movie = Event.objects.create(name="Movie Night", kind="ticket", place="PVR Cinemas", price=250)
        concert = Event.objects.create(name="Rock Concert", kind="ticket", place="Open Ground", price=1000)

        for i in range(1, 6):
            Slot.objects.create(event=turf, start=now + timedelta(hours=i * 2), duration=60, capacity=10)
            Slot.objects.create(event=court, start=now + timedelta(hours=i * 3), duration=60, capacity=8)
        for i in range(1, 4):
            Slot.objects.create(event=movie, start=now + timedelta(days=i), duration=150, capacity=50)
            Slot.objects.create(event=concert, start=now + timedelta(days=i * 2), duration=180, capacity=100)

        self.stdout.write("Sample events added")
