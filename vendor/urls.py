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

    # Food Item CRUD
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/update/<int:pk>/', views.update_food, name='update_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # Opening hours CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    path('order_details/<int:order_number>/', views.order_details, name='vendor_order_details'),
    path('my_orders/', views.my_orders, name='vendor_my_orders')
]
