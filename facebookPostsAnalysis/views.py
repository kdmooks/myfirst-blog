from django.shortcuts import render

# Create your views here.
def patient_Info(request):
	return render(request,'facebookPostsAnalysis/patient_Info.html', {})