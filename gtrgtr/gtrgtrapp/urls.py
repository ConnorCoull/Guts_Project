from django.urls import path
from .views import index

app_name = 'gtrgtrapp'

urlpatterns = [
    path('', index, name='index'),
]

