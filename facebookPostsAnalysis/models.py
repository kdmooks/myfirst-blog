from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Patient(models.Model):
	patient=models.CharField(max_length=200)
	facebookId=models.CharField(max_length=200)
	assignedClinician=models.CharField(max_length=200)

	def __str__(self):
		return self.patient + self.facebookId 
class UserProfile(models.Model):
	#links UserProfile to a User model instance,we refernce the default user model usin a one-to-ne relationship
	#because othe applications may wants to use the User model
	user = models.OneToOneField(User)

	#The additional attributes we wish to include
	#the upload_to attribute value is cojoined with the project's MEDIA_ROOT setting 
	#to provide a path with which uploaded profile images will be stored
	#e.g facebookPostsAnlysis/media/profile_images/ 
	picture=models.ImageField(upload_to='profile_images', blank=True)#it is not a must for users to supply values

    #Override the 
	def __unicode__(self):
		return self.user.username	