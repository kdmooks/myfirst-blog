from django.conf.urls import url
from . import views
urlpatterns=[
     url(r'homePage/$',views.homePage,name='homePage'),
     url(r'^signUpPage/$',views.signUpPage,name='signUpPage'),
     url(r'^loginPage/$',views.loginPage,name='loginPage'),
     url(r'^patient_Info/$',views.patient_Info,name='patient_Info'),
     url(r'^dataAnalysis/$',views.dataAnalysis,name='dataAnalysis'),
     url(r'^patientsInfo/$',views.patientsInfo,name='patientsInfo'),
     url(r'^restricted/$',views.restricted,name='restricted'),
     url(r'^logout/$',views.user_logout,name='logout'),

]