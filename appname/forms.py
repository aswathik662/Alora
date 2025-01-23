from django import forms
from .models import User_details

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User_details
        fields = ['user_id', 'phone_number', 'gender', 'address']