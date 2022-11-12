from django.urls import path
from accounts import views as account_views
from . import views

urlpatterns = [
    path('', account_views.vendor_dashboard, name='vendor'),
    path('profile/', views.vendor_profile, name='vendor_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/update/<int:pk>/', views.update_category, name='update_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

]
