from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth import logout,authenticate,login


# Create your views here.
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
    return render(request,'allu.html',{'data':data})




    