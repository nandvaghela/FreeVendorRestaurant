from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages


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
            user = User.object.create_user(firstname=firstname, lastname=lastname, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Your account has been registered successfully')
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
