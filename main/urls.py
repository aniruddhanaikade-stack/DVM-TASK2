from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("event/<int:id>/", views.event_page, name="event"),
    path("book/<int:slot_id>/", views.book, name="book"),
    path("add-money/", views.add_money, name="add_money"),
    path("bookings/", views.bookings, name="bookings"),
    path("tickets/", views.tickets, name="tickets"),
    path("history/", views.history, name="history"),
]
