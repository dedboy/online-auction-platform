from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('my-bids/', views.my_bids, name='my_bids'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='auction/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]