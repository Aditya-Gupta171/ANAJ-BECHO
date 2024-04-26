from django.urls import path
from .import views
urlpatterns = [
    path('', views.home,name='home'),
    path('cart/',views.cart),
    path('account/',views.account,name='account'),
    path('aboutUs/',views.aboutUs),
    path('account/signup',views.signUp,name='signup'),
    path('account/login',views.login,name='login'),
    path('account/logout',views.logout),
    path('products/',views.products),
    path('addToCart/',views.addToCart)
    
]
