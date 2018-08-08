from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pprint import pprint 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .models import User_account, Block_chain
from datetime import datetime
import hashlib
# Create your views here.

def login_view(request):
	if request.method == "POST":
		username = request.POST['name']
		password = request.POST['password']
		print(username)
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('/transaction/')
	return render(request,'blockchain/login.html')

def logout_view(request):
	logout(request)
	return redirect('/login/')


def register_view(request):
	if request.method == 'POST':
		request.POST = {'csrfmiddlewaretoken' : request.POST['csrfmiddlewaretoken'],
						 'password1' : request.POST['password'],
						 'password2' : request.POST['password'],
						 'username'  : request.POST['name']}
		pprint(request.POST)
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			u = User_account(user_name=username)
			u.save()
			return redirect('/')
	return render(request,'blockchain/register.html')


def transaction_view(request):
	users = list(User.objects.all())
	sender = request.user
	users.remove(request.user)
	if request.method == "POST":
		s = User_account.objects.get(user_name=sender)
		s.account_balance -= int(request.POST['amount'])
		s.save()
		pprint(request.POST)
		r = User_account.objects.get(user_name=request.POST['receiver'])
		print(r.account_balance)
		r.account_balance += int(request.POST['amount'])
		r.save()
		l_block = Block_chain.objects.all().order_by('-id')
		ts = str(datetime.now())
		ph = str(l_block[0].current_hash)
		am = int(request.POST['amount'])
		sen = str(sender)
		rec = str(request.POST['receiver'])
		h = hashlib.sha256()
		h.update(str(ts).encode('utf-8')+
				str(ph).encode('utf-8')+
				str(am).encode('utf-8')+
				str(sen).encode('utf-8')+
				str(rec).encode('utf-8'))
		ch = str(h.hexdigest())
		b = Block_chain(time_stamp=ts,
						previous_hash=ph,
						current_hash=ch,
						amount=am,
						sender=sen,
						receiver=rec)
		b.save()
		logout(request)
		return redirect('/login/')
	return render(request,'blockchain/transactions.html',{'users':users})


def blockchain_view(request):
	users = list(Block_chain.objects.all().order_by('-id'))
	return render(request,'blockchain/blockchain.html',{'users':users})