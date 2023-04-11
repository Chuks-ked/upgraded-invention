from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import *


# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def investment(request):
    plans = InvestmentPlan.objects.all()
    return render(request, 'dashboard/investment.html',{
        'plan': plans,
    })

def deposit(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        deposit = InvestmentDeposit(user=request.user, amount=amount)
        deposit.save()

        # Send email to user
        subject = 'Investment Deposit Pending'
        message = f'Your deposit of {amount} has been received and is pending approval.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, 'dashboard/includes/investment/deposit_success.html')
    return render(request, 'dashboard/includes/investment/deposit.html')


def withdraw(request):
    return render(request, 'dashboard/withdraw.html')

def history(request):
    return render(request, 'dashboard/history.html')

def referral(request):
    return render(request, 'dashboard/referral.html')

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             referral_link = user.get_referral_link()
#             return render(request, 'signup_success.html', {'referral_link': referral_link})
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})


def all_settings(request):
    return render(request, 'dashboard/all_settings.html')
