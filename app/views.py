from django.shortcuts import render,redirect,get_object_or_404
from .models import Transaction,Wallet
from django.contrib.auth import get_user_model
from .mock_api import MockAPI
from .forms import UserLoginForm,SignupForm
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
import requests
# Create your views here.

User = get_user_model

def index(request):
   
    return render(request, 'index.html')
@login_required
def wallet(request):
     if request.method == 'POST':
        sender_wallet_address = request.POST.get('sender_wallet')
        recipient_address = request.POST.get('recipient_address')
        amount = request.POST.get('amount')
      
        sender_wallet = Wallet.objects.get(address=sender_wallet_address)

        transaction = Transaction.objects.create(sender_wallet=sender_wallet, recipient_address=recipient_address, amount=amount, confirming_user=request.user)
        return redirect('transaction_detail', pk=transaction.pk)
     return render(request, 'wallet.html')
@api_view(['POST'])
def confirm_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    api_url = 'http://api/confirm-transaction'  # Замените на URL вашего API для подтверждения
    api_data = {
        'transaction_id': transaction.id,
        'amount': transaction.amount,
        'description': transaction.description
    }

    try:
        response = requests.post(api_url, json=api_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Обработка ошибки вызова API
        error_message = 'Ошибка вызова API: {}'.format(str(e))
        return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    transaction.confirmed = True
    transaction.save()
    serializer = TransactionSerializer(transaction)
    return Response(serializer.data)

@login_required
def cancel_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.cancel_transaction()
    return redirect('transaction_detail', pk=transaction.pk)
@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    return render(request, 'transaction_detail.html', {'transaction': transaction})
@login_required
def transaction_list(request):
    user = request.user
    transactions = Transaction.objects.filter(confirming_user = user)
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

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # замените 'home' на URL вашей домашней страницы
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})