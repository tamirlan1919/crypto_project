from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import messages
# Create your models here.

User = get_user_model()



class Wallet(models.Model):
    address = models.CharField(max_length=255)
    subaccount_id = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    cryptocurrency = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.address} {self.subaccount_id}'

class Transaction(models.Model):
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    confirming_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def confirm_transaction(self, address):
        if not self.is_confirmed and not self.is_cancelled  and self.sender_wallet.address!= address:
            self.is_confirmed = True
            self.save()
        else:
            messages.error( 'Нельзя переводить деньги на свой счет')
            
    

    def cancel_transaction(self):
        if not self.is_confirmed and not self.is_cancelled:
            self.is_cancelled = True
            self.save()