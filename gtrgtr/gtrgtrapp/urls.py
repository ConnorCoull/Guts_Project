from django.urls import path
from .views import IndexView

app_name = 'gtrgtrapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]

