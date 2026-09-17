from django.urls import path
from website.core.views import home

urlpatterns = [
    path('', home, name='home'),
]
