"""
URL configuration for alora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from appname import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resetpassword',views.password_reset_request,name='resetpassword'),
    path('verifyotp',views.verify_otp,name='verifyotp'),
    path('newpassword',views.set_new_password,name='newpassword'),
    path('',views.index),
    path('reg', views.register,name='reg'),
    path('log', views.log, name='log'),
    path('ho/', views.home,name='home'),






    path('ad/', views.ad,name='admin'),
    path('profile', views.profile,name='profile'),
    path('all', views.vu,name='all'),
    path('edit', views.edit,name='edit'),
    path('view_hall',views.view_hall,name='hall'),
    path('add_hall',views.add_hall,name='addhall'),
    path('food',views.food,name='food'),
    path('ad_fud',views.add_food,name='ad_fud'),
    path('viewd',views.decoration_details,name='viewd'),
    path('addd',views.add_decoration,name='addd'),
    path('log_out',views.log_out,name='log_out'),
    path('book',views.booking,name='book'),
    path('userviewbooking',views.user_view_booking,name='userviewbooking'),
    path('adminviewbooking',views.admin_view_booking,name='adminviewbooking'),
    path('acceptrejectbooking/<int:id>',views.accept_reject_booking,name='acceptrejectbooking'),
    # path('payment_status/<int:id>',views.stripe_payments,name='payment_status'),


     path('ind',views.ind2),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
