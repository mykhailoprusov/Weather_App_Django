from . import views
from django.urls import path

urlpatterns = [
    path('', views.start, name = 'start-page'),
]