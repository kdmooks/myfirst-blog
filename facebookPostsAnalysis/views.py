from django.shortcuts import render

# Create your views here.
def homePage(request):
	return render(request,'facebookPostsAnalysis/homePage.html', {})

def signUpPage(request):
	return render(request,'facebookPostsAnalysis/signUpPage.html', {})	

def loginPage(request):
	return render(request,'facebookPostsAnalysis/loginPage.html', {})	

def patient_Info(request):
	return render(request,'facebookPostsAnalysis/patient_Info.html', {})	

def dataAnalysis(request):
	return render(request,'facebookPostsAnalysis/dataAnalysis.html', {})

def patientsInfo(request):
	return render(request,'facebookPostsAnalysis/patientsInfo.html', {})				
