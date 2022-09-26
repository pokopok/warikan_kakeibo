from django.urls import path
from . import views

app_name = 'warikan'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
]