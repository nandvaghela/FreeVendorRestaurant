from django.http import HttpRequest
from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.register_user, name='registerUser'),
    path('registerVendor/', views.register_vendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('CustomerDashboard/', views.customer_dashboard, name='CustomerDashboard'),
    path('VendorDashboard/', views.vendor_dashboard, name='VendorDashboard'),

    path('activate/<uidb64>/<token>/', views.activate_user, name='activate_user'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

]
