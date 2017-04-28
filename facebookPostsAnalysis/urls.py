from django.conf.urls import url
from . import views
urlpatterns=[
     url(r'^$',views.patient_Info,name='patient_Info'),
]