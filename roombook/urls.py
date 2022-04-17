from django.urls import path
from .views import AvailableForm

app_name  = 'roombook'


urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('book_1/<type>/', AvailableForm.as_view(), name="book_1"),
  

]