from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('investment/', views.investment, name='investment'),

    path('success/', views.deposit, name='success'),
    path('deposit/', views.deposit, name='deposit'),

    path('withdraw/', views.withdraw, name='withdraw'),
    path('history/', views.history, name='history'),
    path('history/', views.referral, name='referral'),
    path('settings/', views.all_settings, name='all_settings'),
]
