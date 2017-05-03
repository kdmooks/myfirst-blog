from django.conf.urls import url
from . import views
urlpatterns=[
     url(r'homePage/$',views.homePage,name='homePage'),
     url(r'^signUpPage/$',views.signUpPage,name='signUpPage'),
     url(r'^loginPage/$',views.loginPage,name='loginPage'),
     url(r'^patient_Info/$',views.patient_info,name='patient_info'),
     url(r'^dataAnalysis/$',views.data_analysis,name='data_analysis'),
     url(r'^patientsInfo/$',views.patients_info,name='patients_info'),
     url(r'^restricted/$',views.restricted,name='restricted'),
     url(r'^logout/$',views.user_logout,name='logout'),
     url(r'^get_data/$',views.get_data,name='get_data'),

]