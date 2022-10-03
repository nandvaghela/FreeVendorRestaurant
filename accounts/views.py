from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm


# Create your views here.
def register_user(request):
    if request.method == 'POST':

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
    if request.method == 'POST':
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
            return redirect('registerUser')

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
