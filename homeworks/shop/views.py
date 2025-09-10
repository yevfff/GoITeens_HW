from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, AdminRegisterForm, LoginForm, ProductForm
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Product

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
            return redirect('shop:login')
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


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_color_map = {
            'Roses': 'bg-pink-200 text-pink-800',
            'Tulips': 'bg-yellow-200 text-yellow-800',
            'Lilies': 'bg-indigo-200 text-indigo-800',
            'Orchids': 'bg-purple-200 text-purple-800',
        }

        for product in context['products']:
            product.badge_class = category_color_map.get(
                product.category.category_name,
                'bg-gray-200 text-gray-800'  
            )

        
        new_products = Product.objects.filter(new=True)
        context['new_products'] = new_products
        return context


@login_required
def add_product(request):
    if not request.user.is_admin_user:
        return redirect('shop:product_list') 

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:product_list')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})