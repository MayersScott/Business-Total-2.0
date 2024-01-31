from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('index') 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле '{field}': {error}")
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'business_total_gen_app/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'business_total_gen_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        cost_price = request.POST['cost_price']
        selling_price = request.POST['selling_price']
        kol_day = request.POST['kol_day']
        supplier_url = request.POST.get('supplier_url') 
        author = request.user
        product = Product(name=name, cost_price=cost_price, selling_price=selling_price, kol_d=kol_day, supplier_url=supplier_url, author=author)
        product.save()
        return redirect('index')
    return render(request, 'business_total_gen_app/add_product.html')


def delete_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    product.delete()
    return redirect('index')

def index(request):
    user = request.user
    if user.is_authenticated:
        products = Product.objects.filter(author=user)

        kol_day = sum(product.kol_d for product in products)
        costs = sum(product.cost_price for product in products) * kol_day
        revenue = sum(product.selling_price for product in products) * kol_day

        profit = revenue - costs

        kol_day_m = sum(product.kol_d for product in products) * 30
        costs_m = sum(product.cost_price for product in products) * kol_day * 30
        revenue_m = sum(product.selling_price for product in products) * kol_day * 30

        profit_m = (revenue - costs) * 30

        context = {
            'products': products,
            'revenue': revenue,
            'costs': costs,
            'profit': profit,
            'kol_day': kol_day,
            'revenue_m': revenue_m,
            'costs_m': costs_m,
            'profit_m': profit_m,
            'kol_day_m': kol_day_m,
            'user': user,
        }
    else:
        context = {
            'user': user,
        }

    return render(request, 'business_total_gen_app/index.html', context)

def profile(request):
	user = request.user

	context = {
		'user': user,
	}
	return render(request, 'business_total_gen_app/profile.html', context)
