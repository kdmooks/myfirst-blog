import os
import re
import random
import urllib2
import json
from django.shortcuts import render
from django.contrib.auth import  authenticate, login ,logout
from django.contrib.auth.decorators import  login_required
from .forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Patient


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
    		#print user_form.errors, profile_form.errors
    		return HttpResponse(user_form.errors, profile_form.errors) 

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

def patient_info(request):
	patients=Patient.objects.all()
	return render(request,'facebookPostsAnalysis/patient_Info.html', {'patients':patients})	

def data_analysis(request):
	return render(request,'facebookPostsAnalysis/dataAnalysis.html', {})

# def get_data(request):

# 	print('******', request.GET['user_id'])

# 	return render(request,'facebookPostsAnalysis/get_data.html', {'keletso': request.GET['user_id']})	

def patients_info(request):
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


#this method provides the functionality of extracting facebook posts,given an active
#facebook user id,the graph API which consists of tables such as posts and select fields(message)
def get_data(request):
	if request.method == 'GET' and request.GET.get('user_ID'):
	    userId= request.GET.get('user_ID')
	    print('******', userId)
	    graphUrl='https://graph.facebook.com/'
	    postsNav='posts?fields=message&since=2015-02-26&limit=100'
	    acessToken='EAAYUC0BHO1sBAEZBQo4ifXHMKCjEU3YJlnUEPQtxmU3sx5jCibgjLOFf4q18swHXxgMKPPhMSBmceKFcuJOZA0bfT0hji7LIZCGKLTzqkGkZCpXY65lnwZCpNOFJVJjLWtlDEijeSiYKFxYde5yJd9VxBNpsKiiAZD'
	    #get the url of the user to extract posts
	    graph_url=graphUrl+ userId  + "/" + postsNav + "&access_token=" + acessToken
	    #navigate to the url and returns a file-like object
	    graph_response = urllib2.urlopen(graph_url)
	    #read the data from the response
	    readable_page = graph_response.read()
	    #converting the response to a JSON object allows access to information
	    #using key value pairs,takes the file contents(readable_page)as a string
	    #and returns a JSON object(a python dictionary data structure)
	    json_postdata = json.loads(readable_page)
	    #access the outermost dictionary(data)which contains a list of dictionaries
	    #with keys,"message" and "id"
	    json_fbposts = json_postdata['data']

	    #create a text file 
	    userPosts=open("C:\Users\User\Documents\FinalYearProject\\finalYearProject\gfgf.txt","w")
	    #get post messages
	    messages="message"
	    #goes through each dictionary nested in the data dictionary
	    for post in json_fbposts:
	        #extract a message if it is contained in the dictionary    
	        if messages in post:
	             #write each message to the text file   
	             userPosts.write(post["message"])

        classlist=['anxiety','depression','moodMania','stable','substanceAbuse']
        current_situation=RunExperiment(classlist)

        context = {'current_situation': current_situation}
        context.update(
        	file_content=userPosts)

        return render(request,'facebookPostsAnalysis/get_data.html', context)             
                
   
yourpath = 'C:\Users\User\Documents\FinalYearProject\\finalYearProject\symptoms'
training = {} # dictionary of training docs
testing = {}
classProbs = {}
conditionalprobs = {}

#Code to read all files in current directory and all subdirectories
# This function can be modified to read all files in a given directory and subdirectories
# under the given directory
def ReadAllFiles(yourpath="C:\Users\User\Documents\FinalYearProject\\finalYearProject\symptoms"):
    dirs = os.listdir(yourpath)

    allfiles = {}
    
    for d in dirs:
        filesInClass = os.listdir(yourpath+"\\"+d)
        allfiles[d] = filesInClass
 
    return allfiles 
# Update class dictionary with new class and text
def SpecifyClasses(classname,classfilepathname,classdictionary,):
    # classdictionary={'classname': ..., 'classtext': ..., 'numdocs': ...}
    classdictionary = {}
    classtext = []
    countDocs = 0
    # navigate to the path where a document is definedfor each file in the class training data, open it and read text
    # then add it to list of lines
    for root, dirs, documents in os.walk(classfilepathname, topdown=False):
        countDocs += 1
        global training
        documents = training[classname] # use training documents only
        for docName in documents:
            document = os.path.join(root, docName)
            # open the document for each class
            openFile = open(document, "r")
            # read only 30 lines of the document
            for i in range(40):
                line = openFile.readline()
                # add the line to the text list
                classtext += [line]
            openFile.close()
    classdictionary['classname'] = classname
    classdictionary['classtext'] = classtext
    classdictionary['numdocs'] = countDocs
    return classdictionary
    
# Create new class token dictionary with name and tokens and their frequenices
def Tokenize(classdictionary):
    classtext = classdictionary['classtext']
    classname = classdictionary['classname']
    tokenfreqs = {}
    classtokenfreqs = {}
    # add the classname to the dictionary
    classtokenfreqs['classname'] = classname
    for line in classtext:
        # find only words made up of upper or lower case letters
        words = re.findall('[a-zA-Z]+', line)
        # if the line has text
        if len(words) > 0:
            for word in words:
                # if word exists increment its frequency, else add it to tokenlist
                # change word to lower case before adding it to tokenlist
                lowerword = str.lower(word)
                if lowerword in tokenfreqs:                    
                    tokenfreqs[lowerword] = tokenfreqs[lowerword] + 1
                else:
                    tokenfreqs[lowerword] = 1
    #{'classname': ..., 'tokenlist':{'tokena': frequency, 'tokenb': frequency, ...}
    # add the tokenlist to the dictionary
    classtokenfreqs['tokenlist'] = tokenfreqs
    return classtokenfreqs

# calculate prior probability for all classes and conditional probabilities for all tokens
def CalculateProbabilities(classdictionary):
    classname = classdictionary['classname']
    # tokenize the class text in the classdictionary
    tokenized = Tokenize(classdictionary)
    # extract the tokenlist from the dictionary 
    tokenlist = tokenized['tokenlist']
    # number of words in the class from given classdictionary
    numberofwords = sum(tokenlist.values())

    global classProbs
    global training
    
    # calculate the total number of docs
    totalDocs = 0
    for key in training:
        for doc in training[key]:
            totalDocs += 1
    # calculate the prior class probabilities and add them to the dictionary
    for key in training:
        classProbs[key] = len(training[key])*1.0/totalDocs
    
    # dictionary of conditional probabilities
    probabilities = {}

    allTokens = {} # collection of just tokens from all classes
    allClassesWithTokens = {} # classes and their tokenlists
    # find the number of unique words in training data
    for key in training:
            filepathname = yourpath + "\\" + key
            classdic = SpecifyClasses(key, filepathname, {})
            tokenls = Tokenize(classdic)['tokenlist']
            allClassesWithTokens[key] = tokenls
            for token in tokenls:
                if token in allTokens:
                    #print "token already exists"
                    allTokens[token] += 1
                else:
                    allTokens[token] = 1
    totalUniqueWords = len(allTokens)

    # now calculate the conditional probabilities for each token from given classdictionary        
    for tkn in tokenlist:
        probsgivenclass = {} # dictionary of probabilities given class
        for cls in allClassesWithTokens:
            tknlst = allClassesWithTokens[cls]
            numwordsinclass = sum(tknlst.values())
            conditionalprob = 0.0
            if tkn in tknlst:
                conditionalprob = ((tknlst[tkn] + 1)*1.0)/(numwordsinclass + totalUniqueWords)
            else:
                conditionalprob = ((0 + 1)*1.0)/(numwordsinclass + totalUniqueWords)
            probsgivenclass[cls] = conditionalprob # add conditional probability
        # add class conditional probabilities for each token
        probabilities[tkn] = probsgivenclass 
    
    return probabilities #{'tokena': {'classa':conditionalprob, 'classb':conditionalprob,'classc':...}}

# classify new document
def Classify(document):
    # list of lines read from the document
    doctext = []
    doc = open(document, "r")
    # read only 30 lines of the document
    for i in range(40):
        line = doc.readline()
        # add the line to doctext
        doctext += [line]
    doc.close()
    # list of words read from the document
    wordslist = []
    for line in doctext:
        # find only words from the english alphabet
        wordsinline = re.findall('[a-zA-Z]+', line)
        # add each word to wordslist
        for word in wordsinline:
            if word not in wordslist:
                wordslist += [str.lower(word)]
    # dictionary of the probability of a class given a document
    classprobalilities = {}
    global classProbs
    # calculate probability of class given document for all classes
    for cls in classlist:
        priorclass = classProbs[cls]
        product = classProbs[cls] # class prior probability
        global conditionalprobs
        wordprobs = []
        # for each word multiply the class prior probability by the probability
        # of a word given class
        for word in wordslist:
            if word in conditionalprobs:
                product *= conditionalprobs[word][cls]
        classprobalilities[cls] = product
    return classprobalilities # {class:prob, ...} ordered structure of class probabilities

# Split data set into training and testing, train using training, then calculate accuracy on testing
def RunExperiment(listofclasses):
    #print listofclasses
    allfiles = ReadAllFiles()
    global training
    global testing
    training = {} # dictionary of training docs
    testing = {} # dictionary of testing docs
    listofAllFiles = {}
    for cls in listofclasses:
        listofAllFiles = allfiles[cls]
        trainingDocs = listofAllFiles
        # add the docs to training and testing dictionaries
        training[cls] = trainingDocs
        

    # train using training data
    global conditionalprobs # collection of all token conditional probabilities
    for key in training:
        filepathname = yourpath + "\\" + key
        classdic = SpecifyClasses(key, filepathname, {})
        probabilities = CalculateProbabilities(classdic)
        for token in probabilities:
            conditionalprobs[token] = probabilities[token]
    #{file:{'actualclass':'assignedclass'}, ...}
    compareresults = {} # dictionary of actual and assigned classes per file
    

    maxrank = 0.0
    assignedclass = ""
    #create the file with extracted posts 
    #getPosts()
    #save
    pathtofile='C:\Users\User\Documents\FinalYearProject\\finalYearProject\posts.txt'
    ranking = Classify(pathtofile)
    for rank in ranking:
        # find the max probability of a class given document
        if ranking[rank] > maxrank:
            maxrank = ranking[rank]
            assignedclass = rank
    
    return assignedclass
    





