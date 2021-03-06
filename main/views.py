from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Orders
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import REST, TimeFrame

# For alpaca api keys
from dotenv import load_dotenv
load_dotenv()

stock = ""
price = 0

# Create your views here.
def homepage(request):

	#print(request.GET)

	stock = "AAPL"

	api = REST()

	bars = api.get_barset(stock, "day", limit=7)
	data = []

	price = bars[stock][-1].c

	for count, bar in enumerate(bars[stock]):
		data.append(['Day ' + str(count + 1), bar.l, bar.c, bar.o, bar.h])

	if 'buyBtn' in request.GET:
		Orders.objects.create(orderType="Buy", ticker=stock, price=price, transactionDate=datetime.now(), user=request.user)

	elif 'sellBtn' in request.GET:
		Orders.objects.create(orderType="Sell", ticker=stock, price=price, transactionDate=datetime.now(), user=request.user)


	return render(request=request, template_name="main/home.html", context={"Stock": stock, "CurrentPrice": price, "Bars": data})

def single_slug(request, single_slug):

	stock = single_slug

	api = REST()

	bars = api.get_barset(stock, "day", limit=7)

	if len(bars[stock]) == 0:
		messages.error(request, "Stock does not exist.")
		return redirect("main:homepage")

	price = bars[stock][-1].c

	if 'buyBtn' in request.GET:
		Orders.objects.create(orderType="Buy", ticker=stock, price=price, transactionDate=datetime.now(), user=request.user)

	elif 'sellBtn' in request.GET:
		Orders.objects.create(orderType="Sell", ticker=stock, price=price, transactionDate=datetime.now(), user=request.user)

	data = []

	for count, bar in enumerate(bars[stock]):
		data.append(['Day ' + str(count + 1), bar.l, bar.c, bar.o, bar.h])

	return render(request=request, template_name="main/home.html", context={"Stock": stock, "CurrentPrice": price, "Bars": data})

def orders(request):

	user = request.user
	if user.is_authenticated:
		return render(request=request, template_name="main/orders.html", context={"Orders": user.orders.all})
	else:
		messages.error(request, "You do not have permission to view this page.")
		return redirect("main:homepage")

def register(request):

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New Account Created: {username}")
			login(request, user)
			messages.info(request, f"You are logged in as {username}")
			return redirect("main:homepage")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}: {form.error_messages[msg]}")

	form = UserCreationForm()
	return render(request, "main/register.html", context={"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You are now logged out.")
	return redirect("main:homepage")

def login_request(request):

	if request.method == "POST":
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are logged in as {username}")
				return redirect("main:homepage")
			else:
				messages.error(request, "Invalid username or password.")

		else:
			messages.error(request, "Invalid username or password.")

	form = AuthenticationForm()
	return render(request, "main/login.html", context={"form":form})