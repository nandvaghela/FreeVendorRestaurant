from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detect_user
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Restrict vendor from accessing user page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict user from accessing vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myaccount')

    elif request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():

            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.object.create_user(firstname=firstname, lastname=lastname, username=username, email=email,
                                           password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully')
            return redirect('login')

        else:
            print('Invalid form')
            print(form.errors)
            messages.error(request, 'Account not registered')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register_user.html', context)


def register_vendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myaccount')

    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.object.create_user(firstname=firstname, lastname=lastname, username=username, email=email,
                                           password=password)
            user.role = User.VENDOR
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your restaurant has been registered successfully, please wait for approval')
            return redirect('login')

        else:
            print('Invalid form')
            print(form.errors)
            print(vendor_form.errors)
            messages.error(request, 'Restaurant not registered')
    else:
        form = UserForm()
        vendor_form = VendorForm()

    context = {
        'form': form,
        'vendor_form': vendor_form
    }
    return render(request, 'accounts/register_vendor.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in.')
        return redirect('myaccount')

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('myaccount')

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')


@login_required(login_url='login')
def myaccount(request):
    user = request.user
    redirect_url = detect_user(user)
    return redirect(redirect_url)


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')
