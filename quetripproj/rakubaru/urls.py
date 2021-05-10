from django.conf.urls import url
from . import views

app_name='rakubaru'

urlpatterns=[

    ######################## Admin ###########################################################################################################

    url(r'^$', views.index, name='index'),
    url(r'ralogin', views.ralogin, name='ralogin'),
    url(r'rahome', views.rahome, name='rahome'),
    url(r'ralogout', views.ralogout, name='ralogout'),
    url(r'ranewemployee', views.ranewemployee, name='ranewemployee'),
    url(r'radelemployee', views.radelemployee, name='radelemployee'),
    url(r'^rapasswordchange', views.rapasswordchange, name='rapasswordchange'),
    url(r'^rachangepassword', views.rachangepassword, name='rachangepassword'),
    url(r'^raallreports', views.raallreports, name='raallreports'),
    url(r'^radelroute', views.radelroute, name='radelroute'),
    url(r'^rauserreports', views.rauserreports, name='rauserreports'),
    url(r'^rasearchreportbydate', views.rasearchreportbydate, name='rasearchreportbydate'),
    url(r'^raopenroutemap', views.raopenroutemap, name='raopenroutemap'),


    ######################### User #################################################################################################################

    url(r'login', views.login, name='login'),
    # url(r'signup', views.signup, name='signup'),
    url(r'forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'resetpassword', views.resetpassword, name='resetpassword'),
    url(r'rstpwd', views.rstpwd, name='rstpwd'),
    url(r'updatemember', views.updatemember, name='updatemember'),
    url(r'passwordupdate', views.passwordupdate, name='passwordupdate'),
    url(r'uploadreport', views.uploadreport, name='uploadreport'),


]