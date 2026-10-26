from django.contrib import admin

from .models import Booking, Event, Profile, Slot, Transaction

admin.site.register([Profile, Event, Slot, Booking, Transaction])
