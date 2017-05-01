from django.shortcuts import render
from django.contrib.auth import  authenticate, login ,logout
from django.contrib.auth.decorators import  login_required
from .forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def homePage(request):
	return render(request,'facebookPostsAnalysis/homePage.html', {})

def signUpPage(request):
	#a boolean value for telling the template wether the registration was successful
    #Set to false initially.Code changes value to to True when registration succeeds
    registered = False

    #If its a HTTP POST,we're interested in processing the form data
    if request.method == 'POST':
    	#Attempt to grab information from the raw information data
    	#Note that we make use of both UserForm,UserProfileForm
    	user_form = UserForm(data=request.POST)
    	profile_form = UserProfileForm(data=request.POST)

    	#If the two forms are valid
    	if user_form.is_valid() and profile_form.is_valid():
    		#Save the user's form to the database
    		user = user_form.save()

    		#now we hash the password with the set_password() method
    		#once hashed we could update the user object
    		user.set_password(user.password)
    		user.save()

    		#now sort out the userProfile instance
    		profile = profile_form.save(commit=False)
    		profile.user = user

    		#Did the user provide aprofile pic?
    		#If so we need to get it from the input form and put it in the UserProfile  model
    		if 'picture' in request.FILES:
    			profile.picture = request.FILES['picture']

    		#now we save the userProfile model instance
    		profile.save()

    		#update your variable to tell the temmplate SignUpPage,the registration was successful
    		registered = True
    		return HttpResponseRedirect('/loginPage/')


    		#Invalid forms,print problems
    	else:
    		print user_form.errors, profile_form.errors

    #Nota HTTP POST,so we render our form using two model ModelForm instances
    #this forms will be blank ready for user input
    else:
    	user_form = UserForm()
    	profile_form = UserProfileForm()
	return render(request,'facebookPostsAnalysis/signUpPage.html', 
			{'user_form': user_form, 'profile_form' : profile_form, 'registered': registered})	

def loginPage(request):
	#If the request is a HTTP POST,try to pull out relevant information.
	if request.method == 'POST':
		#Gather the username and passwors from the user obtained from the login form
		username = request.POST.get('username')
		password = request.POST.get('password')

		#use djando's machinery to attempt to see if the username/password
		#combination is valid -A user object is returned if it is
		user = authenticate(username=username, password=password)

		#If we have a User object the details are correct
		if user:
			#is the account active?It could have been disabled
			if user.is_active:
				#if the account is valid and active ,we can log the user in
				#Wel send the user to the patientInfo page
				login(request, user)
				return HttpResponseRedirect('/homePage/') 
			else:
				#An active account was used -no logging in
				return HttpResponse("You account has been disabled") 
		else:
			#Bad login details were provided
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	#This request is not an HTTP POST,so display the login form
	#This scenario would most likely be a HTTP GET .
	else:
		#No context variable to pass the template variables hence the blank dictionary object 					
		return render(request,'facebookPostsAnalysis/loginPage.html', {})	

def patient_Info(request):
	return render(request,'facebookPostsAnalysis/patient_Info.html', {})	

def dataAnalysis(request):
	return render(request,'facebookPostsAnalysis/dataAnalysis.html', {})

def patientsInfo(request):
	return render(request,'facebookPostsAnalysis/patientsInfo.html', {})				

@login_required
def restricted(request):
	return HttpResponse("You are logged in")
#only those logged in can access the view
@login_required
def user_logout(request):
	#since we know the user is logged in we can just log them out
	logout(request)
	#take the user to the homepage
	return HttpResponseRedirect('/homePage/')
	