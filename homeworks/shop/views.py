from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm, AdminRegisterForm, LoginForm
from django.http import JsonResponse

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {
        'form': form,
        'title': 'Реєстрація користувача',
        'button_text': 'Зареєструватись'
    })

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AdminRegisterForm()
    return render(request, 'register.html', {
        'form': form,
        'title': 'Реєстрація адміністратора',
        'button_text': 'Зареєструватись як адміністратор'
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return JsonResponse({'success': True}) 
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
