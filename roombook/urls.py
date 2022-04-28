from django.urls import path
from .views import  AvailabilityView, BookView

app_name  = 'roombook'


urlpatterns = [
    path('book_1/<type>/', AvailabilityView.as_view(), name="book_1"),
    path('book/<booking>/', BookView.as_view(), name="book"),
  

]