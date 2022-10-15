from django.urls import path
from gtrgtrapp import views

app_name = 'gtrgtrapp'

urlpatterns = [
    path('', views.index, name='index'),
]

