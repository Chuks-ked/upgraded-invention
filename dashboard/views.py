from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def investment(request):
    return render(request, 'dashboard/investment.html')

def withdraw(request):
    return render(request, 'dashboard/withdraw.html')

def history(request):
    return render(request, 'dashboard/history.html')

def referral(request):
    return render(request, 'dashboard/referral.html')

def all_settings(request):
    return render(request, 'dashboard/all_settings.html')
