from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    KINDS = [("slot", "Slot based"), ("ticket", "Ticket based")]
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=KINDS)
    place = models.CharField(max_length=100)
    price = models.IntegerField()  # price per slot / per ticket

    def __str__(self):
        return self.name


class Slot(models.Model):
    # for slot events this is a time slot, for ticket events this is a show
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.IntegerField(default=60)  # in minutes
    capacity = models.IntegerField()
    booked = models.IntegerField(default=0)

    def left(self):
        return self.capacity - self.booked

    def __str__(self):
        return f"{self.event.name} {self.start}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # + for money added, - for money spent
    note = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
