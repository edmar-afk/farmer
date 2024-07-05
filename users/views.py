from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login as auth_login
from .models import Pesticides

from django.db.models import F, FloatField, ExpressionWrapper, Value
from django.db.models.functions import Replace, Cast, Abs
from django.db.models.functions import Abs
# Create your views here.


def pesticides(request):
    products = Pesticides.objects.all().order_by('-id')
    
    if request.method == 'POST':
        pic = request.FILES.get('pic') 
        name = request.POST['name']
        display = request.POST['display']
        description = request.POST['description']
        price = request.POST['price']

        new_product = Pesticides.objects.create(name=name, description=description,display=display, price=price, image=pic)
        new_product.save()
        messages.success(request, 'Product Added!')
        
    context = {
        'products': products
    }
        
    return render(request, 'main/pesticides.html', context)


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


def pest(request):
    return render(request, 'farmer/pest.html')

def cropSeason(request):
    return render(request, 'farmer/cropSeason.html')



def farmerDashboard(request):
    query = request.GET.get('pesticides_search')
    pesticides = Pesticides.objects.filter(display='Pesticides')
    if query:
        try:
            query = float(query.replace(',', ''))  # Remove commas and convert to float

            # Annotate and filter to handle price conversion and display condition
            pesticides = Pesticides.objects.filter(display='Pesticides').annotate(
                price_as_float=Cast(
                    Replace(F('price'), Value(','), Value('')),
                    output_field=FloatField()
                ),
                price_difference=ExpressionWrapper(
                    Abs(Cast(
                        Replace(F('price'), Value(','), Value('')),
                        output_field=FloatField()
                    ) - query),
                    output_field=FloatField()
                )
            ).order_by('price_difference')

        except ValueError:
            pesticides = Pesticides.objects.none()
        
    context = {
        'pesticides': pesticides,
        'query': query if query else ''
    }
    return render(request, 'farmer/index.html', context)


def farmerFertilizer(request):
    query = request.GET.get('fertilizer_search')
    pesticides = Pesticides.objects.filter(display='Fertilizer')
    if query:
        try:
            query = float(query.replace(',', ''))  # Remove commas and convert to float

            # Annotate and filter to handle price conversion and display condition
            pesticides = Pesticides.objects.filter(display='Fertilizer').annotate(
                price_as_float=Cast(
                    Replace(F('price'), Value(','), Value('')),
                    output_field=FloatField()
                ),
                price_difference=ExpressionWrapper(
                    Abs(Cast(
                        Replace(F('price'), Value(','), Value('')),
                        output_field=FloatField()
                    ) - query),
                    output_field=FloatField()
                )
            ).order_by('price_difference')

        except ValueError:
            pesticides = Pesticides.objects.none()
        
    context = {
        'pesticides': pesticides,
        'query': query if query else ''
    }
    return render(request, 'farmer/fertilizer.html', context)




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

def removeProduct(request, product_id):
    Pesticides.objects.filter(id=product_id).delete()
    messages.success(request, 'Product Removed')
    return redirect(request.META.get('HTTP_REFERER'))