from django.shortcuts import render,redirect,get_object_or_404
from .models import Transaction,Wallet
from django.contrib.auth import get_user_model
from .mock_api import MockAPI
from .forms import UserLoginForm
from django.contrib.auth import logout,login
# Create your views here.

User = get_user_model

def index(request):
    if request.method == 'POST':
        sender_wallet_address = request.POST.get('sender_wallet')
        recipient_address = request.POST.get('recipient_address')
        amount = request.POST.get('amount')
      
        sender_wallet = Wallet.objects.get(address=sender_wallet_address)

        transaction = Transaction.objects.create(sender_wallet=sender_wallet, recipient_address=recipient_address, amount=amount, confirming_user=request.user)
        return redirect('transaction_detail', pk=transaction.pk)
    return render(request, 'index.html')



def confirm_transaction(request, pk):
    print("Confirm transaction view is called.")
    transaction = get_object_or_404(Transaction, pk=pk)
    print("Transaction object:", transaction)
    MockAPI.confirm_transaction(transaction.id)
    transaction.confirm_transaction(transaction.recipient_address)
    
    return redirect('transaction_detail', pk=transaction.pk)

def cancel_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.cancel_transaction()
    return redirect('transaction_detail', pk=transaction.pk)

def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('/')