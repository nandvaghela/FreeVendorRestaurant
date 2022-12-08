import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, OpeningHours
from menu.models import Category, FoodItem
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amount
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from datetime import date, datetime
from orders.forms import OrderForm
from accounts.models import UserProfile


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_details(request, vendor_slug=None):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    # Getting opening hours
    opening_hours = OpeningHours.objects.filter(vendor=vendor).order_by('day', 'from_hour')
    today = date.today().isoweekday()
    print(today)
    # Getting current day's opening hours
    current_opening_hours = OpeningHours.objects.filter(vendor=vendor, day=today)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
    }
    return render(request, 'marketplace/vendor_details.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            # check food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                print(food_id)
                # check if item is already added to cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=food_item)
                    # increase cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased Cart Quantity',
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=food_item, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Food added to cart',
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'food item do not exists'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            # check food item exists
            try:
                food_item = FoodItem.objects.get(id=food_id)
                print(food_id)
                # check if item is already added to cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=food_item)
                    # increase cart quantity
                    if check_cart.quantity > 1:
                        check_cart.quantity -= 1
                        check_cart.save()

                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse({'status': 'Success', 'message': 'Decreased Cart Quantity',
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity,
                                         'cart_amount': get_cart_amount(request)})
                except:

                    return JsonResponse({'status': 'Failed', 'message': 'you do not have this item in your Cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'food item do not exists'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if is_ajax(request=request):
            try:
                cart_item = Cart.objects.filter(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Item removed from Cart.',
                                         'cart_counter': get_cart_counter(request),
                                         'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exists'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})


def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        keyword = request.GET['keyword']
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['long']
        radius = request.GET['radius']
        print(radius)
        # Get vendor's ids that has the keyword
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword,
                                                             is_available=True).values_list(
            'vendor', flat=True)

        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True,
                                                     user__is_active=True))
        if latitude and longitude and radius:
            pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))
            vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword,
                                                                                     is_approved=True,
                                                                                     user__is_active=True),
                                            user_profile__location__distance_lte=(pnt, D(km=radius))).annotate(
                distance=Distance("user_profile__location", pnt)).order_by("distance")

            for v in vendors:
                v.kms = round(v.distance.km, 1)
        vendor_count = vendors.count
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
            'source_location': address
        }
        print(vendors)
        return render(request, 'marketplace/listings.html', context)


@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')

    user_profile = UserProfile.objects.get(user=request.user)

    default_values ={
        'first_name': request.user.firstname,
        'last_name': request.user.lastname,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code
    }

    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items
    }
    return render(request, 'marketplace/checkout.html', context)
