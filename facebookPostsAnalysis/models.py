from django.db import models
from django.utils import timezone

class Patient(models.Model):
	patient=models.CharField(max_length=200)
	facebookId=models.CharField(max_length=200)
	assignedClinician=models.CharField(max_length=200)

	def __str__(self):
		return self.patient + self.facebookId 
