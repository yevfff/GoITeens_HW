from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('register-admin/', views.register_admin, name='register_admin'),
    path('login/', views.login_view, name='login'),

    path('', views.ProductListView.as_view(), name='product_list'),
    path('add_product/', views.add_product, name='add_product'),
]
