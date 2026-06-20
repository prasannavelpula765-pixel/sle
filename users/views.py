from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from . models import UserRegistration
from django.conf import settings
import os
import pandas as pd

def Index(request):
    return render(request, 'index.html')

def UserRegistrationPage(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phonenumber = request.POST['phone']
        address = request.POST['address']
        username = request.POST['username']
        password = request.POST['pswd']
        userdetails = UserRegistration.objects.create(
            name = name,
            email = email,
            phonenumber = phonenumber,
            address = address,
            username = username,
            password = password,
        )
        userdetails.save()
        messages.success(request, 'Registration Successful')
        print('Registration Success............')
    return render(request, 'userregisterpage.html')  
  

def UserLoginPage(request):
    if request.method == 'POST':
        UserName = request.POST['username']
        Password = request.POST['pswd']
        try:
            user = UserRegistration.objects.get(username=UserName, password=Password)
            if user.is_active:
                request.session['username'] = user.username
                request.session['email'] = user.email   
                request.session['name'] = user.name
                return redirect('UserHome')
            else:
                messages.warning(request, 'Your account is not active. Please Activate through Admin.')
                return redirect('userLogin')
        except UserRegistration.DoesNotExist:
            messages.warning(request, 'Check your login details.')
            return redirect('userLogin')
    return render(request, 'userloginpage.html')


def UserHomePage(request):
    name = request.session.get('name')
    email = request.session.get('email')
    username = request.session.get('username')
    return render(request, 'users/userbase.html', {'name':name, 'email':email,'username':username})


def DataSetView(request):
    path = os.path.join(settings.MEDIA_ROOT, 'data', 'Balanced_dataset.csv')
    data = pd.read_csv(path)
    return render(request, 'users/datasetView.html', {'data': data.to_html(classes='table table-striped table-bordered')})


def ModelMatrices(request):
    return render(request, 'analysis/matrices.html')

def UserLogout(request):
    logout(request)
    return redirect('userLogin')

