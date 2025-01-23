from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth import logout,authenticate,login
import random
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def send_otp(email):
    otp=random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'meethuprasanthkk@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method =='POST':
        email=request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp=send_otp(email)

            context={
                "email":email,
                "otp": otp,
            }
            return render(request,'forgot_password2.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'forgot_password1.html')
    return render(request,'forgot_password1.html')

def verify_otp(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        otpold=request.POST.get('otp1')
        otp=request.POST.get('otp2')

        if otpold==otp:
            context={
                'otp' : otp,
                'email' : email
            }
            return render(request,'forgot_password3.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'forgot_password2.html')

def set_new_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        if new_password==confirm_password:
            try:
                user=User.objects.get(email=email)
                
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(log)
            except User.DoesNotExist:
                messages.error(request,'Password does not match')
        return render(request,'forgot_password3.html',{'email':email})
    return render(request,'forgot_password3.html',{'email':email})



def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return render(request,'registration.html',{'error':'email already exist'})
        gender=request.POST.get('gender')
        phone_number=request.POST.get('no')
        if User_details.objects.filter(phone_number=phone_number).exists():
            return render(request,'registration.html',{'error':'phone already exist'})
        address=request.POST.get('address')
        uname=request.POST.get('uname')
        if User.objects.filter(username=uname).exists():
            return render(request,'registration.html',{'error':'username already exist'})
        pas=request.POST.get('password')
        pas1=request.POST.get('cpass')
        if pas!=pas1:
            return render(request,"registration.html",{'error':'password does not match'})
        obj=User.objects.create_user(username=uname,password=pas,email=email,first_name=name)
        obj.save()
        val=User_details.objects.create(user_id=obj,phone_number=phone_number,gender=gender,address=address)
        val.save()
        return redirect('log')
    return render(request,'registration.html')

def log(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        admin_user=authenticate(request,username=username,password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect('admin')
        elif user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'invalid username or password'})
    
    else:
       return render(request,'login.html')

def home(request):
   return render(request,'home.html')


def profile(request):
    user=User.objects.get(id=request.user.id)
    a=User_details.objects.get(user_id=user.id)
    return render(request,'detail.html',{'data':a})
def edit(request):
    data=User.objects.get(id=request.user.id)
    user = User_details.objects.get(user_id=data.id)
    if request.method == 'POST':
        user.user_id.first_name=request.POST['name']
        user.user_id.email=request.POST['email']
        user.phone_number=request.POST['no']
        user.gender=request.POST['gender']
        user.address=request.POST['address']
        user.user_id.save()
        user.save()
        return redirect('all')
    else:
        return render(request,'edituser.html',{'data':user})

# admin....................................................
def ad(request):
   return render(request,'admin.html')
def vu(request):
    data=User_details.objects.all()
    return render(request,'alluser.html',{'data':data})

def view_hall(request):
    data=Halls.objects.all()
    return render(request,'hall.html',{'data':data})

def add_hall(request):
    if request.method== 'POST':
         hall_name=request.POST['name']
         location=request.POST['location']
         capacity=request.POST['capacity']
         price_per_day=request.POST['price']
         photo_url=request.FILES['photo']
         hall_description=request.POST['description']
         val=Halls.objects.create(hall_name=hall_name,location=location,capacity=capacity,price_per_day=price_per_day,photo_url=photo_url,hall_description=hall_description)
         val.save()
         return redirect('hall')
    else:
        return render(request,'add_hall.html')
    
def food(request):
    data=Food.objects.all()
    return render(request,'food.html',{'data':data})

def add_food(request):
    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES['image']
        price=request.POST['price']
        val=Food.objects.create(food_name=name,food_image=image,food_price=price)
        val.save()
        return redirect('food')
    else:
        return render(request,'add_food.html')
    



    
    
    
    
     

         

    


    