from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.

def mainLogin(request):
    return render(request, 'main/mainLogin.html')


def logInInfo(request):
    users = User.objects.all().order_by('-id')
    
    context = {
        'users': users
    }
    
    return render(request, 'main/loginInfo.html', context)


def mainDashboard(request):
    users = User.objects.all().order_by('-id')
    
    context = {
        'users': users
    }
    
    return render(request, 'main/index.html', context)

def login(request):
    if request.method == 'POST':
        number = request.POST.get('number')
        password = request.POST.get('password')

        info = authenticate(username=number, password=password)
        if info is not None:
            auth_login(request, info)
            if info.is_staff:
                return redirect('farmerDashboard')
            else:
                messages.error(request, "You are not approve to the admin. Please wait")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    return render(request, 'login.html')
    
def homepage(request):
    
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        number = request.POST['number']
        address = request.POST['address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=number).exists():
                messages.error(request, 'Mobile Number already taken.')
                return redirect('register')

            else:
                new_farmer = User.objects.create_user(
                    first_name=fullname, username=number, password=password1,last_name=address, is_staff=False, is_superuser=False )
                new_farmer.save()
                messages.success(request, 'Account created')
                return redirect('login')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('register')
    return render(request, 'register.html')


def farmerDashboard(request):
    return render(request, 'farmer/index.html')



def removeUser(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User Removed')
    return redirect(request.META.get('HTTP_REFERER'))


def acceptUser(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'User Accepted')
    return redirect(request.META.get('HTTP_REFERER'))

def declineUser(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    # You can redirect to a success page or to the same page
    messages.success(request, 'User Declined')
    return redirect(request.META.get('HTTP_REFERER'))

def logoutUser(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('homepage')