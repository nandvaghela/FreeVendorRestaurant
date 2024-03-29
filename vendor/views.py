from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm, OpeningHoursForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor, OpeningHours
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm, FoodItemForm
from django.template.defaultfilters import slugify

from orders.models import Order, OrderedFood


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Create your views here
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Restaurant Profile Updated ")
            return redirect('vendor_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendor_profile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menu_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category).order_by('created_at')
    context = {
        'category': category,
        'fooditems': fooditems,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()
            category.slug = slugify(category_name) + '-' + str(category.id)
            category.save()
            messages.success(request, "Category Added successfully ")
            return redirect('menu_builder')
        else:
            messages.error(request, "Category not added ")
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()

            messages.success(request, "Category Updated successfully ")
            return redirect('menu_builder')
        else:
            messages.error(request, "Category not updated ")
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'vendor/update_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully ")
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            foodItem = form.save(commit=False)
            foodItem.vendor = get_vendor(request)
            foodItem.slug = slugify(food_title)
            form.save()

            messages.success(request, "Food Item Added successfully ")
            return redirect('fooditems_by_category', foodItem.category.id)
        else:
            messages.error(request, "Food Item not added ")
            print(form.errors)

    else:
        form = FoodItemForm()

        # modified form for categories
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_dish.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def update_food(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, instance=food_item)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            foodItem = form.save(commit=False)
            foodItem.vendor = get_vendor(request)
            foodItem.slug = slugify(food_title)
            form.save()

            messages.success(request, "Food item Updated successfully ")
            return redirect('fooditems_by_category', foodItem.category.id)
        else:
            messages.error(request, "Category not updated ")
            print(form.errors)

    else:
        form = FoodItemForm(instance=food_item)

        # modified form for categories
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'food_item': food_item
    }
    return render(request, 'vendor/update_food_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food_item = get_object_or_404(FoodItem, pk=pk)
    food_item.delete()
    messages.success(request, "Food item deleted successfully ")
    return redirect('fooditems_by_category', food_item.category.id)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def opening_hours(request):
    opening_hours = OpeningHours.objects.filter(vendor=get_vendor(request))
    form = OpeningHoursForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_opening_hours(request):
    if request.user.is_authenticated:
        if is_ajax(request=request) and request.method == 'POST':

            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            print(day, from_hour, to_hour, is_closed)

            try:
                hour = OpeningHours.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour,
                                                   to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day = OpeningHours.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(),
                                    'is_closed': 'Closed'}
                    else:
                        response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(),
                                    'from_hour': day.from_hour, 'to_hour': day.to_hour,
                                    'is_closed': 'Open'}
                    return JsonResponse(response)

            except IntegrityError as e:
                response = {'status': 'failed', 'message': from_hour + '-' + to_hour + ' already exists for this day!'}
                return JsonResponse(response)

        else:
            HttpResponse('Invalid Request')
    else:
        HttpResponse('Invalid Request')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            hour = get_object_or_404(OpeningHours, pk=pk)
            hour.delete()
            return JsonResponse({'status': 'success', 'id': pk})
        else:
            HttpResponse('Invalid Request')
    else:
        HttpResponse('Invalid Request')


def order_details(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))

        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'total': order.get_total_by_vendor()['grand_total'],
            'tax_data': order.get_total_by_vendor()['tax_dict'],
        }
    except:
        return redirect('vendor')
    return render(request, 'vendor/vendor_order_details.html',context)


def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
        'order_count': orders.count(),
    }
    return render(request, 'vendor/my_orders.html', context)
