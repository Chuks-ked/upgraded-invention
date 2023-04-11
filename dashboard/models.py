from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

# Create your models here.

class InvestmentPlan(models.Model):
    name = models.CharField(max_length=100)
    minimum_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return self.name

class InvestmentDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('received', 'Received')), default='pending')
    date = models.DateTimeField(auto_now_add=True)


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('sent', 'Sent'),
    ], default='pending')
    date = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Withdrawal)
def send_withdrawal_emails(sender, instance, created, **kwargs):
    if created:
        # Send email to user to confirm their withdrawal request
        send_mail(
            'Withdrawal request received',
            'Your withdrawal request for {} has been received and is pending approval.'.format(instance.amount),
            'from@example.com',
            [instance.user.email],
            fail_silently=False,
        )
    elif instance.status == 'approved':
        # Send email to user to let them know their withdrawal has been approved
        send_mail(
            'Withdrawal approved',
            'Your withdrawal request for {} has been approved and is being processed.'.format(instance.amount),
            'from@example.com',
            [instance.user.email],
            fail_silently=False,
        )
    elif instance.status == 'sent':
        # Send email to user to let them know their withdrawal has been sent to their account
        send_mail(
            'Withdrawal sent',
            'Your withdrawal request for {} has been sent to your account.'.format(instance.amount),
            'from@example.com',
            [instance.user.email],
            fail_silently=False,
        )

class User(models.Model):
    ...
    
    def get_referral_link(self):
        try:
            return self.referral.referral_link
        except Referral.DoesNotExist:
            return None

class Referral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_link = models.CharField(max_length=255, unique=True)

    @receiver(post_save, sender=User)
    def create_referral_link(sender, instance, created, **kwargs):
        if created:
            referral_link = get_random_string(length=20)
            Referral.objects.create(user=instance, referral_link=referral_link)