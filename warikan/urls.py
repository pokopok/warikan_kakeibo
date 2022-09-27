from django.urls import path
from . import views

app_name = 'warikan'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('expenses_add/', views.ExpensesAddView.as_view(), name='expenses_add'),
    path('expenses_data/', views.ExpensesDataView.as_view(), name='expenses_list'),
]