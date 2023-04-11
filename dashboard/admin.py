from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import *

# Register your models here.
class InvestmentPlanAdmin(admin.ModelAdmin):
    list_display = ('name','minimum_deposit', 'maximum_deposit', 'interest_rate', 'duration')
admin.site.register(InvestmentPlan, InvestmentPlanAdmin)

class InvestmentDepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'date')
    list_filter = ('status',)
    actions = ['approve_deposits']

    def approve_deposits(self, request, queryset):
        for deposit in queryset:
            deposit.status = 'received'
            deposit.save()

            # Send email to user
            subject = 'Investment Deposit Received'
            message = f'Your deposit of {deposit.amount} has been received and approved.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [deposit.user.email]
            send_mail(subject, message, from_email, recipient_list)

        self.message_user(request, f'{queryset.count()} deposits have been approved.')
admin.site.register(InvestmentDeposit, InvestmentDepositAdmin)



class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'date')
    list_filter = ('status',)
admin.site.register(Withdrawal, WithdrawalAdmin)

