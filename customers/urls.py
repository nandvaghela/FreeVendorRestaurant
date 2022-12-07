from django.urls import path, include
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.customer_dashboard,name='customer'),
    path('profile/', views.customer_profile, name='customer_profile'),

]
