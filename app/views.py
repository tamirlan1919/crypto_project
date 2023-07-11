from django.shortcuts import render,redirect,get_object_or_404
from .models import Transaction,Wallet
from django.contrib.auth import get_user_model
from .mock_api import MockAPI
from .forms import UserLoginForm,SignupForm
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer,WalletSerializer
from rest_framework import generics
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


class TransactionAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
@api_view(['POST'])
def confirm_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(id=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    transaction.is_confirmed = True
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
            return redirect('/')  
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})