from django.urls import path
from . views import Home,Contact,About


urlpatterns = [
    
    path("",Home.as_view(),name="home"),
    path('about/',About.as_view(),name="about"),
    path('contact/',Contact.as_view(),name='contact'),
   
]
