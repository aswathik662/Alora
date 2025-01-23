from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_details(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,unique=True)
    gender=models.CharField(max_length=10)
    address=models.TextField()

class Halls(models.Model):
    hall_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    capacity=models.IntegerField()
    price_per_day=models.DecimalField(max_digits=10,decimal_places=2)
    photo_url=models.FileField()
    hall_description=models.TextField(null=True,blank=True)

class Events(models.Model):
    event_name=models.CharField(max_length=100)
    hall_id=models.ForeignKey(Halls,on_delete=models.CASCADE)
    event_date=models.DateField()
    event_description=models.TextField(null=True,blank=True)
    event_status=models.CharField(max_length=100)

class Food(models.Model):
    food_name=models.CharField(max_length=10,null=True)
    food_image=models.FileField()
    food_price=models.DecimalField(max_digits=10,decimal_places=2)

class Decoration(models.Model):
    decoration_image=models.ImageField(upload_to='image/')
    decoration_price=models.DecimalField(max_digits=10,decimal_places=2)

class Bookings(models.Model):
    event_id=models.ForeignKey(Events,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    hall_id=models.ForeignKey(Halls,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)
    payment_status=models.CharField(max_length=100)
    photography=models.CharField(max_length=100,null=True,blank=True)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    decoration=models.ForeignKey(Decoration,on_delete=models.CASCADE)
    photography_cost=models.DecimalField(max_digits=10,decimal_places=2)
    total_payment=models.DecimalField(max_digits=10,decimal_places=2)
