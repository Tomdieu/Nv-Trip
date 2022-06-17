from django import forms

from datetime import date

import re

from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model

from .models import Vehicle

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):

	password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ["first_name", "last_name", "username","email",'sex', "phone", "country","user_type",'password1','password2']


	# def clean_date_of_birth(self):
	# 	data = self.cleaned_data['date_of_birth']
	# 	print('Data : ',data)
	# 	# year,month,day = data.split('-')
	# 	# d = date(int(year), int(month), int(day))

	# 	if data >= date.today():
	# 		raise ValidationError('Select A Valid Date of birthday!')

	# 	return data		

	def clean_phone(self):
		data = self.cleaned_data['phone']

		pattern = re.compile(r'\+?(237)\d{9}$')

		if not pattern.match(data):
			raise ValidationError(["·Please Enter A Valid Number","·+237xxxxxxxxx is an example of a valid number"])

		return data

	def clean_password2(self):
		psw1 = self.cleaned_data["password1"]
		psw2 = self.cleaned_data["password2"]

		if psw1 and psw2 and psw1!=psw2:
			raise ValidationError("Password dont' match!")

		return psw2


	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class VehicleCreationForm(forms.ModelForm):

	class Meta:
		model = Vehicle
		fields = ['driver_plate_number','car_color','max_place','car_type','car_brand']
		# exclude = ['user','nbp','lat','lng']
	
	def save(self,commit=False):
		vehicle = super().save(commit=False)
		if commit:
			vehicle.save()

		return vehicle