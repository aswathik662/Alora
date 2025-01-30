from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth import logout,authenticate,login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.contrib import messages
import stripe
from django.conf import settings 

# # Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_payments(request,id):
    try:
        data=Bookings.objects.get(id=id)
        total_amount = data.total_payment

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount*100),
            currency="usd",
            metadata={"data":data.id,"user_id":request.user.id},

        )
        context = {
            'client_secret': intent.client_secret,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'total_amount':total_amount,
            'data':data,
        }
        return render(request,'stripe_payments.html',context)
    except Bookings.DoesNotExist:
        return redirect(user_view_booking)


def send_otp(email):
    otp=random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'aswathikudayan@gmail.com',
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
def log_out(request):
    auth.logout(request)
    context = {'success_message': 'You have been logged out successfully.'}
    return redirect(log)


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


def booking(request):
    data=User.objects.get(id=request.user.id)
    halls=Halls.objects.all()
    foods=Food.objects.all()
    decorations=Decoration.objects.all()
    if request.method == 'POST':
        eventdate=request.POST['date']
        hall=request.POST['hall']
        food=request.POST['f']
        food_id=request.POST.get('food')
        no_of_people=request.POST['people_num']
        photography=request.POST['photography']
        decoration=request.POST['decoration']
        decoration_id=request.POST.get('decoration_model')
        check_date=Bookings.objects.filter(hall_id=hall,event_date=eventdate).exists()
        if check_date:
            return HttpResponse('hall already booked!')
        if food == "yes":
            food=True
        else:
            food=False
        if decoration == "yes":
            decoration=True
        else:
            decoration=False
        if no_of_people == "":
            no_of_people=0
        no_of_people=int(no_of_people)
        hall_amount=0
        food_amount=0
        photography_amount=0
        decoration_amount=0
        t_amount=0
        h=Halls.objects.get(id=hall)
        hall_amount=h.price_per_day
        f=None
        d=None
        if food_id:
            f=Food.objects.get(id=food_id)
            food_amount=no_of_people*f.food_price
        if photography == 'yes':
            photography_amount=10000
        if decoration_id:
            d=Decoration.objects.get(id=decoration_id)
            decoration_amount=d.decoration_price
        t_amount=hall_amount+photography_amount+decoration_amount+food_amount
        if food_id and decoration_id :
            obj=Bookings.objects.create(event_date=eventdate,user_id=data,hall_id=h,photography=photography,food_value=food,food=f,no_of_people=no_of_people,decoration_value=decoration,decoration=d,photography_cost=photography_amount,total_payment=t_amount)
            obj.save()
        else:
            obj=Bookings.objects.create(event_date=eventdate,user_id=data,hall_id=h,photography=photography,food_value=food,no_of_people=no_of_people,decoration_value=decoration,photography_cost=photography_amount,total_payment=t_amount)
            obj.save()
        return redirect(user_view_booking)
    else:
        return render(request,'booking.html',{'data':halls,'foods':foods,'decoration':decorations})
    
def user_view_booking(request):
    user=User.objects.get(id=request.user.id)
    booking=Bookings.objects.filter(user_id=user)
    for i in booking:
        print(i.event_status)
    return render(request,'view_booking.html',{'x':booking})

 
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
    
def decoration_details(request):
    data=Decoration.objects.all()
    return render(request,'decoration_details.html',{'data':data})
def add_decoration(request):
    if request.method == 'POST':
        name=request.POST['name']
        price=request.POST['price']
        image=request.FILES['image']
        obj=Decoration.objects.create(decoration_name=name,decoration_price=price,decoration_image=image)
        obj.save()
        return redirect(decoration_details)
    return render(request,'add_decoration.html')

def admin_view_booking(request):
    book=Bookings.objects.all()
    return render(request,'admin_booking.html',{'data':book})

def accept_reject_booking(request,id):
    data=Bookings.objects.get(id=id)
    if request.method == 'POST':
        value=request.POST.get('Status')
        if value == 'Accept':
            data.event_status='Accept'
        elif value == 'Reject':
            data.event_status='Reject'
        data.save()
        return redirect(admin_view_booking)
    return redirect(admin_view_booking)



# *design********
def ind2(req):
    return render(req,'dindex.html')





    
    
    
    
     

         

    


    