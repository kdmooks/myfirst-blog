from django import forms
from django.contrib.auth.models import User
from  .models import UserProfile

#the following classes inherit from forms.ModelForm
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	#an inline class to provide additional information on the form
	class Meta:
		#Provide an association  between the Modelform and a model
		model = User
		fields = ('username','email','password' )

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields=	('picture',)	