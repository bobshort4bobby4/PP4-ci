
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView ,FormView, View
from .models import Room, RoomType, Booking
# Create your views here.

class Home(ListView):
    model = RoomType
    template_name = 'roombook/home.html'
    ordering = ['pk']
