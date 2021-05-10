# import datetime
import difflib
import os
import string
import urllib
from itertools import islice

import io
import requests
import xlrd
import re

from django.core import mail
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib import messages
# from _mysql_exceptions import DataError, IntegrityError
from django.template import RequestContext

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_control
from numpy import long

import pandas as pd
import numpy as np

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from xlrd import XLRDError
from time import gmtime, strftime
import time
from openpyxl.styles import PatternFill

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django import forms
import sys
from django.core.cache import cache

import urllib.request
import urllib.parse
from random import randint
import random
import math

from pyfcm import FCMNotification
import stripe

from quetrip.models import Member
from quetrip.serializers import MemberSerializer


import pyrebase

config = {
    "apiKey": "AIzaSyC49viNs1_Y4ep4W0fVmKsOpRpPvnU69hs",
    "authDomain": "quetrip-260515.firebaseapp.com",
    "databaseURL": "https://quetrip-260515.firebaseio.com",
    "storageBucket": "quetrip-260515.appspot.com"
}

firebase = pyrebase.initialize_app(config)


############################################################################# Quetrip #################################################################################################################
############################################################################# Quetrip #################################################################################################################
############################################################################# Quetrip #################################################################################################################

def index(request):
    # return HttpResponse('<h1>Hello I am QUETRIP backend!</h1>')
    return render(request, 'quetrip/cutiealarmsupport.html')


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def registerCustomer(request):

    if request.method == 'POST':

        eml = request.POST.get('email', '')
        password = request.POST.get('password', '')

        users = Member.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = Member()
            member.email = eml
            member.picture_url = settings.URL + '/static/quetrip/images/anonymous.png'
            member.password = password
            member.role = 'customer'
            member.registered_time = str(int(round(time.time() * 1000)))
            member.save()

            fs = FileSystemStorage()

            i = 0
            for f in request.FILES.getlist('files'):
                # print("Product File Size: " + str(f.size))
                # if f.size > 1024 * 1024 * 2:
                #     continue
                i = i + 1
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                if i == 1:
                    member.picture_url = settings.URL + uploaded_url
                    member.save()
                    break

            sendEmailVerificationLink(eml)

            serializer = MemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            users = Member.objects.filter(email=eml, password=password)
            count = users.count()
            if count == 0:
                resp_er = {'result_code': '1'}
                return HttpResponse(json.dumps(resp_er))
            else:
                resp_er = {'result_code': '2'}
                return HttpResponse(json.dumps(resp_er))

    elif request.method == 'GET':
        pass


def sendEmailVerificationLink(email):

    message = 'Thank you for your joining to our QueTrip application.<br>Please click this link below to verify your email.<br><br>https://quetrip.pythonanywhere.com/quetrip_verify?email=' + email

    html =  """\
                <html>
                    <head></head>
                    <body>
                        <a href="https://quetrip.pythonanywhere.com/"><img src="https://quetrip.pythonanywhere.com/static/quetrip/images/logo.png" style="width:200px;height:120px; margin-left:25px;"/></a>
                        <h2 style="margin-left:10px; color:#02839a;">WELCOME TO QUETRIP APP!</h2>
                        <div style="font-size:16px; word-break: break-all; word-wrap: break-word;">
                            {mes}
                        </div>
                    </body>
                </html>
            """
    html = html.format(mes=message)

    fromEmail = 'gabrielfqr@gmail.com'
    toEmailList = []
    toEmailList.append(email)
    msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)


def quetrip_verify(request):
    email = request.GET['email']
    members = Member.objects.filter(email=email)
    member = members[0]
    member.auth_status = 'yes'
    member.save()
    return render(request, 'quetrip/welcome_verify.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        if password != '':
            members = Member.objects.filter(email=email, password=password, role='customer')
        else:
            members = Member.objects.filter(email=email, role='customer')
        resp = {}
        if members.count() > 0:
            member = members[0]
            serializer = MemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = Member.objects.filter(email=email, role='customer', auth_status='yes')
            if members.count() > 0:
                member = members[0]
                serializer = MemberSerializer(member, many=False)
                resp = {'result_code': '0', 'data':serializer.data}
                return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
            members = Member.objects.filter(email=email)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}
        return HttpResponse(json.dumps(resp))


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def sociallogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        members = Member.objects.filter(email=email, role='customer')
        resp = {}
        if members.count() > 0:
            member = members[0]
            serializer = MemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
        else:
            member = Member()
            member.email = email
            member.picture_url = settings.URL + '/static/quetrip/images/anonymous.png'
            member.role = 'customer'
            member.auth_status = 'yes'
            member.registered_time = str(int(round(time.time() * 1000)))
            member.save()
            serializer = MemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
        return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        usrs = Member.objects.filter(email=email)
        if usrs.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        message = 'You are allowed to reset your password from your request.<br>For it, please click this link to reset your password.<br><br>https://quetrip.pythonanywhere.com/resetpassword?email=' + email

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="https://quetrip.pythonanywhere.com/"><img src="https://quetrip.pythonanywhere.com/static/quetrip/images/logo.png" style="width:200px;height:120px; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">QUETRIP User's Security Update Information</h2>
                            <div style="font-size:16px; word-break: break-all; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = 'gabrielfqr@gmail.com'
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('We allowed you to reset your password', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))


def resetpassword(request):
    email = request.GET['email']
    return render(request, 'quetrip/resetpwd.html', {'email':email})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if len(password) < 8:
            return render(request, 'quetrip/result.html',
                          {'response': 'Please enter password of characters more than 8.'})
        if password != repassword:
            return render(request, 'quetrip/result.html',
                          {'response': 'Please enter the same password.'})
        members = Member.objects.filter(email=email)
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'quetrip/result.html',
                          {'response': 'Password has been reset successfully.'})
        else:
            return render(request, 'quetrip/result.html',
                          {'response': 'You haven\'t been registered.'})
    else: pass


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def updateCustomer(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')

        members = Member.objects.filter(id=member_id)
        if members.count() == 0:
            resp = {'result_code':'1'}
            return HttpResponse(json.dumps(resp))

        member = members[0]
        member.name = name
        if phone_number != '': member.phone_number = phone_number
        if address != '':
            member.address = address
            member.latitude = latitude
            member.longitude = longitude

        member.save()

        fs = FileSystemStorage()

        i = 0
        for f in request.FILES.getlist('files'):
            # print("Product File Size: " + str(f.size))
            # if f.size > 1024 * 1024 * 2:
            #     continue
            i = i + 1
            filename = fs.save(f.name, f)
            uploaded_url = fs.url(filename)
            if i == 1:
                member.picture_url = settings.URL + uploaded_url
                member.save()

        serializer = MemberSerializer(member, many=False)
        resp = {'result_code': '0', 'data':serializer.data}

        return HttpResponse(json.dumps(resp))



def getloc(request):
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut

    my_address = 'Mexico'

    geolocator = Nominatim(timeout=3)
    try:
        location = geolocator.geocode(my_address)
        return HttpResponse(location)
    except GeocoderTimedOut as e:
        return HttpResponse("Error: geocode failed on input %s with message %s"%(my_address, e.message))





################################################################## Jitsi Video Conference ######################################################################################################

def openJitsiVideo(request):
    return render(request, 'jitsi/index1.html')


################################################################## Admob Ads Test ######################################################################################################

def ads(request):
    return render(request, 'quetrip/admob_test.html')
































