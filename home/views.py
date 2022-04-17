
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView , View, TemplateView
from roombook.models import  RoomType

# Create your views here.
class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = RoomType.objects.all()
        return context

class InfoView(TemplateView):
    template_name = 'home/info.html'


class ContactView(TemplateView):
    template_name = 'home/contact.html'