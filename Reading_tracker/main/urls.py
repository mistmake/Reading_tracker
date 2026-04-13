from django.urls import path
from .views import index, contacts

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
]
