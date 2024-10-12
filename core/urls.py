from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('',views.home,name="home"),
    path('signup/',views.signup,name="signup"),
    path('login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form = LoginForm),name="login"),
    path('preferences/',views.preferences,name="preferences"),
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('process_barcode/',views.process_barcode),
    path('product/', views.product_page, name='product_page'),
    path('index/',views.index,name="index"),
]
