from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Booking, Event, Profile, Slot, Transaction


def home(request):
    events = Event.objects.all()
    return render(request, "home.html", {"events": events})


def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Profile.objects.create(user=user)
        login(request, user)
        return redirect("home")
    return render(request, "registration/signup.html", {"form": form})


def event_page(request, id):
    event = get_object_or_404(Event, id=id)
    slots = event.slot_set.filter(start__gte=timezone.now()).order_by("start")
    return render(request, "event.html", {"event": event, "slots": slots})


@login_required
def add_money(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == "POST":
        amount = int(request.POST.get("amount") or 0)
        if amount <= 0:
            messages.error(request, "Enter a valid amount")
        else:
            profile.balance += amount
            profile.save()
            Transaction.objects.create(user=request.user, amount=amount, note="Added money")
            messages.success(request, f"Added Rs {amount}")
            return redirect("add_money")
    return render(request, "add_money.html", {"profile": profile})


@login_required
def book(request, slot_id):
    if request.method != "POST":
        return redirect("home")
    quantity = int(request.POST.get("quantity") or 1)

    with transaction.atomic():
        slot = Slot.objects.select_for_update().get(id=slot_id)
        profile = Profile.objects.select_for_update().get_or_create(user=request.user)[0]
        total = slot.event.price * quantity

        if quantity < 1:
            messages.error(request, "Wrong quantity")
        elif quantity > slot.left():
            messages.error(request, "Not enough seats left")
        elif total > profile.balance:
            messages.error(request, "Not enough balance, add money first")
        else:
            slot.booked += quantity
            slot.save()
            profile.balance -= total
            profile.save()
            Booking.objects.create(user=request.user, slot=slot, quantity=quantity, total=total)
            Transaction.objects.create(user=request.user, amount=-total, note=f"Booked {slot.event.name}")
            messages.success(request, "Booking done!")
            return redirect("tickets")
    return redirect("event", id=slot.event.id)


@login_required
def bookings(request):
    all_bookings = Booking.objects.filter(user=request.user).order_by("-time")
    return render(request, "bookings.html", {"bookings": all_bookings})


@login_required
def tickets(request):
    active = Booking.objects.filter(user=request.user, slot__start__gte=timezone.now()).order_by("slot__start")
    return render(request, "tickets.html", {"bookings": active})


@login_required
def history(request):
    items = Transaction.objects.filter(user=request.user).order_by("-time")
    return render(request, "history.html", {"items": items})
