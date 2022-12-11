from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detect_user, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from orders.models import Order


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
            user = User.objects.create_user(firstname=firstname, lastname=lastname, username=username, email=email,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()

            # send verification email

            email_subject = 'Activate your FoodOnline account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, email_subject, email_template)

            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')

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
            user = User.objects.create_user(firstname=firstname, lastname=lastname, username=username, email=email,
                                            password=password)
            user.role = User.VENDOR
            user.save()

            vendor = vendor_form.save(commit=False)
            vendor.user = user
            vendor_name = vendor_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # send verification email
            email_subject = 'Activate your FoodOnline account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, email_subject, email_template)

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

    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': recent_orders,
        'order_count': orders.count(),
    }
    return render(request, 'accounts/customer_dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    # vendor = Vendor.objects.get(user=request.user)
    # context = {
    #     'vendor': vendor,
    # }
    return render(request, 'accounts/vendor_dashboard.html')


def activate_user(request, uidb64, token):
    # activate the user by setting the is_active status to be True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations , your account is activated successfully.')
        return redirect('myaccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myaccount')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(email__exact=email)
        if user is not None:

            email_subject = 'Reset your FoodOnline password'
            email_template = 'accounts/emails/reset_password_email.html'
            # send reset password email
            send_verification_email(request, user, email_subject, email_template)

            messages.success(request, 'Password reset link has been sent to email address')
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # decoding the token to validate user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('myaccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            messages.success(request, 'Password reset successfully')
            return redirect('login')

        else:
            messages.error(request, 'Password do not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
