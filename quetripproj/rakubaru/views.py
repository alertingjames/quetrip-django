import requests
from django.core.mail import EmailMultiAlternatives

from django.core.files.storage import FileSystemStorage
import json

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import time
from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from random import randint
from pyfcm import FCMNotification
import pyrebase

from quetrip.models import Rmember, Route, Rpoint, Rpin
from quetrip.serializers import RmemberSerializer, RouteSerializer, RpointSerializer, RpinSerializer


#################### User ###############################################################################################################################


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if password != '':
            members = Rmember.objects.filter(email=email, password=password)
        else:
            members = Rmember.objects.filter(email=email)
        resp = {}
        if members.count() > 0:
            member = members[0]
            if member.status == '':
                member.status = 'loggedin'
                member.save()
            serializer = RmemberSerializer(member, many=False)
            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            members = Rmember.objects.filter(email=email)
            if members.count() > 0:
                resp = {'result_code': '2'}
            else: resp = {'result_code':'1'}

        return HttpResponse(json.dumps(resp))



@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')

        members = Rmember.objects.filter(email=email)
        if members.count() == 0:
            return HttpResponse(json.dumps({'result_code': '1'}))

        member = members[0]

        message = 'You are allowed to reset your password from your request.<br><br><a href="https://quetrip.pythonanywhere.com/rakubaru/resetpassword?uid=' + str(member.pk) + '">パスワードをリセットするには、このリンクをクリックしてください</a>'

        html =  """\
                    <html>
                        <head></head>
                        <body>
                            <a href="#"><img src="https://quetrip.pythonanywhere.com/static/images/rakubaru/appicon.jpg" style="width:120px;height:120px;border-radius: 5%; margin-left:25px;"/></a>
                            <h2 style="margin-left:10px; color:#02839a;">らくばるメンバーのセキュリティ更新情報</h2>
                            <div style="font-size:14px; word-wrap: break-word;">
                                {mes}
                            </div>
                        </body>
                    </html>
                """
        html = html.format(mes=message)

        fromEmail = settings.RAKUBARU_ADMIN_EMAIL
        toEmailList = []
        toEmailList.append(email)
        msg = EmailMultiAlternatives('パスワードのリセットを許可しました', '', fromEmail, toEmailList)
        msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)

        return HttpResponse(json.dumps({'result_code': '0'}))



def resetpassword(request):
    member_id = request.GET['uid']
    member = Rmember.objects.get(id=int(member_id))
    return render(request, 'rakubaru/resetpwd.html', {'member':member})


@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def rstpwd(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '1')
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')
        if password != repassword:
            return render(request, 'rakubaru/result.html',
                          {'response': '同じパスワードを入力してください.'})
        members = Rmember.objects.filter(id=int(member_id))
        if members.count() > 0:
            member = members[0]
            member.password = password
            member.save()
            return render(request, 'rakubaru/result.html',
                          {'response': 'パスワードは正常にリセットされました'})
        else:
            return render(request, 'rakubaru/result.html',
                          {'response': 'あなたは登録されていません'})



@api_view(['GET', 'POST'])
def updatemember(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '0')
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')

        members = Rmember.objects.filter(id=int(member_id))
        count = members.count()
        if count > 0:

            member = members[0]
            member.name = name
            member.phone_number = phone_number
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

            serializer = RmemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)

        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))



@api_view(['GET', 'POST'])
def passwordupdate(request):

    if request.method == 'POST':

        member_id = request.POST.get('member_id', '0')
        password = request.POST.get('password', '')

        members = Rmember.objects.filter(id=int(member_id))
        count = members.count()
        if count > 0:

            member = members[0]
            member.password = password
            member.save()

            serializer = RmemberSerializer(member, many=False)

            resp = {'result_code': '0', 'data':serializer.data}
            return HttpResponse(json.dumps(resp), status=status.HTTP_200_OK)
        else:
            resp = {'result_code': '1'}
            return HttpResponse(json.dumps(resp))



@api_view(['GET', 'POST'])
def uploadreport(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id', '0')
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        start_time = request.POST.get('start_time', '0')
        end_time = request.POST.get('end_time', '0')
        duration = request.POST.get('duration', '0')
        speed = request.POST.get('speed', '0')
        distance = request.POST.get('distance', '0')

        points = request.POST.get('points', '')
        pins = request.POST.get('pins', '')

        route = Route()
        route.member_id = member_id
        route.name = name
        route.description = description
        route.start_time = start_time
        route.end_time = end_time
        route.duration = duration
        route.speed = speed
        route.distance = distance
        route.reported_time = str(int(round(time.time() * 1000)))
        route.status = 'reported'
        route.save()

        if points != '':
            try:
                decoded = json.loads(points)
                for data in decoded['points']:

                    lat = data['lat']
                    lng = data['lng']
                    comment = data['comment']
                    tm = data['time']

                    pnt = Rpoint()
                    pnt.route_id = route.pk
                    pnt.lat = lat
                    pnt.lng = lng
                    pnt.comment = comment
                    pnt.time = tm
                    pnt.save()
            except:
                print('Point data saving error')
                resp = {'result_code': '1'}
                return HttpResponse(json.dumps(resp))

        if pins != '':
            try:
                decoded = json.loads(pins)
                for data in decoded['pins']:

                    lat = data['lat']
                    lng = data['lng']
                    comment = data['comment']
                    tm = data['time']

                    pin = Rpin()
                    pin.route_id = route.pk
                    pin.lat = lat
                    pin.lng = lng
                    pin.comment = comment
                    pin.time = tm
                    pin.save()
            except:
                print('Pin data saving error')
                resp = {'result_code': '1'}
                return HttpResponse(json.dumps(resp))

        resp = {'result_code': '0'}
        return HttpResponse(json.dumps(resp))


























































################### Admin ##################################################################################################################################

def index(request):
    return redirect('/rakubaru/rahome')

@csrf_protect
@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def ralogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')

        # members = Rmember.objects.filter(email=settings.RAKUBARU_ADMIN_EMAIL, role='admin')
        members = Rmember.objects.filter(email=email, role='admin')
        # if members.count() == 0:
        #     member = Rmember()
        #     member.admin_id = '0'
        #     member.name = name
        #     member.email = email
        #     member.password = 'admin'
        #     member.role = 'admin'
        #     member.registered_time = str(int(round(time.time() * 1000)))
        #     member.save()
        #     request.session['adminID'] = member.pk
        #     return redirect('/rakubaru/rahome')
        if members.count() > 0:
            member = members[0]
            request.session['adminID'] = member.pk
            return redirect('/rakubaru/rahome')
        else:
            return render(request, 'rakubaru/result.html',
                          {'response': 'このサイトにアクセスする権限がありません。 別の資格情報で再試行してください。'})


def rahome(request):
    try:
        if request.session['adminID'] == 0 or request.session['adminID'] == '':
            return render(request, 'rakubaru/login.html')
    except KeyError:
        print('no session')
        return render(request, 'rakubaru/login.html')

    adminID = request.session['adminID']
    me = Rmember.objects.get(id=adminID)

    members = Rmember.objects.filter(admin_id=adminID).order_by('-id')

    return render(request, 'rakubaru/home.html', {'members':members, 'me':me})



def ralogout(request):
    request.session['adminID'] = 0
    return redirect('/rakubaru/')


@api_view(['GET', 'POST'])
def ranewemployee(request):
    try:
        if request.session['adminID'] == 0 or request.session['adminID'] == '':
            return render(request, 'rakubaru/login.html')
    except KeyError:
        print('no session')
        return render(request, 'rakubaru/login.html')

    adminID = request.session['adminID']
    me = Rmember.objects.get(id=adminID)

    if request.method == 'POST':

        name = request.POST.get('name', '')
        eml = request.POST.get('email', '')
        phone = request.POST.get('phone', '')

        users = Rmember.objects.filter(email=eml)
        count = users.count()
        if count == 0:
            member = Rmember()
            member.admin_id = str(me.pk)
            member.name = name
            member.email = eml
            member.password = generateRandomPassword(10)
            member.phone_number = phone
            member.picture_url = settings.URL + '/static/images/rakubaru/profile.png'
            member.registered_time = str(int(round(time.time() * 1000)))
            member.save()

            fs = FileSystemStorage()

            try:
                f = request.FILES['picture']
                filename = fs.save(f.name, f)
                uploaded_url = fs.url(filename)
                member.picture_url = settings.URL + uploaded_url
                member.save()
            except MultiValueDictKeyError:
                print('No exists')

            title = 'らくばるへようこそ'
            subject = 'らくばるへの招待'
            message = 'こんにちは ' + member.name + ',<br><br>おめでとうございます！ あなたはらくばるアプリを使用するように招待されています!<br>'
            message = message + '初めてアプリを開いてサインアップするときに、次の認証情報を使用してアプリにログインできます:<br><br>'
            message = message + 'パスワード： ' + member.password + '<br><br>'
            message = message + '最高の願いと幸せな焦点！<br><br>らくばるポスティング チーム'

            from_email = me.email
            to_emails = []
            to_emails.append(member.email)
            send_mail_message(from_email, to_emails, title, subject, message)

            return HttpResponse('success')

        else:
            return HttpResponse('existence')


def send_mail_message(from_email, to_emails, title, subject, message):
    html =  """\
                <html>
                    <head></head>
                    <body>
                        <a href="#"><img src="https://quetrip.pythonanywhere.com/static/images/rakubaru/appicon.jpg" style="width:120px;height:120px;border-radius: 5%; margin-left:25px;"/></a>
                        <h2 style="margin-left:10px; color:#02839a;">{title}</h2>
                        <div style="font-size:14px; white-space: pre-line; word-wrap: break-word;">
                            {mes}
                        </div>
                    </body>
                </html>
            """
    html = html.format(title=title, mes=message)

    msg = EmailMultiAlternatives(subject, '', from_email, to_emails)
    msg.attach_alternative(html, "text/html")
    msg.send(fail_silently=False)


import random
import string

def generateRandomPassword(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str



def radelemployee(request):
    member_id = request.GET['member_id']
    fs = FileSystemStorage()
    member = Rmember.objects.get(id=int(member_id))
    if member.picture_url != '':
        fname = member.picture_url.replace(settings.URL + '/media/', '')
        fs.delete(fname)
    member.delete()

    routes = Route.objects.filter(member_id=member_id)
    for route in routes:
        points = Rpoint.objects.filter(route_id=route.pk)
        for pnt in points:
            pnt.delete()
        pins = Rpin.objects.filter(route_id=route.pk)
        for pin in pins:
            pin.delete()
        route.delete()

    return redirect('/rakubaru/rahome')


def rapasswordchange(request):
    try:
        if request.session['adminID'] == 0 or request.session['adminID'] == '':
            return render(request, 'rakubaru/login.html')
    except KeyError:
        print('no session')
        return render(request, 'rakubaru/login.html')

    adminID = request.session['adminID']
    me = Rmember.objects.get(id=adminID)

    return  render(request, 'rakubaru/password_reset.html', {'me':me})


@api_view(['GET', 'POST'])
def rachangepassword(request):
    try:
        if request.session['adminID'] == 0 or request.session['adminID'] == '':
            return render(request, 'rakubaru/login.html')
    except KeyError:
        print('no session')
        return render(request, 'rakubaru/login.html')

    adminID = request.session['adminID']
    me = Rmember.objects.get(id=adminID)

    if request.method == 'POST':
        email = request.POST.get('email', '')
        oldpassword = request.POST.get('oldpassword', '')
        newpassword = request.POST.get('newpassword', '')

        if email == me.email and oldpassword == me.password:
            me.password = newpassword
            me.save()

        elif email == me.email and oldpassword != me.password:
            return render(request, 'rakubaru/result.html',
                          {'response': '古いパスワードが正しくありません。 正しいパスワードを入力してください'})

        else:
            members = Rmember.objects.filter(email=email)
            if members.count() > 0:
                return render(request, 'rakubaru/result.html',
                          {'response': '誰かがすでに同じメールを使用しています。 別のもので試してみてください'})
            me.email = email
            me.password = newpassword
            me.save()

        return redirect('/rakubaru/rahome')


def raallreports(request):
    routes = Route.objects.all().order_by('-id')
    reportList = getRouteListData(routes)
    return render(request, 'rakubaru/reports.html', {'reports':reportList})


def getRouteListData(routes):
    import datetime
    reportList = []
    for route in routes:
        route.start_time = datetime.datetime.fromtimestamp(float(int(route.start_time)/1000)).strftime("%m/%d/%y %H:%M")
        route.end_time = datetime.datetime.fromtimestamp(float(int(route.end_time)/1000)).strftime("%m/%d/%y %H:%M")
        route.reported_time = datetime.datetime.fromtimestamp(float(int(route.reported_time)/1000)).strftime("%m/%d/%y %H:%M")
        route.speed = round(float(route.speed), 2)
        route.distance = round(float(route.distance), 3)
        con_sec, con_min, con_hour = convertMillis(int(route.duration))
        route.duration = "{0}h {1}m {2}s".format(str(int(con_hour)).zfill(2), str(int(con_min)).zfill(2), str(int(con_sec)).zfill(2))
        members = Rmember.objects.filter(id=int(route.member_id))
        if members.count() > 0:
            member = members[0]
            data = {
                'member':member,
                'route':route,
            }
            reportList.append(data)
    return reportList



def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     hours=(millis/(1000*60*60))%24
     return seconds, minutes, hours

import math
def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier



def radelroute(request):
    route_id = request.GET['route_id']
    option = request.GET['option']
    route = Route.objects.get(id=int(route_id))
    points = Rpoint.objects.filter(route_id=route.pk)
    for pnt in points:
        pnt.delete()
    pins = Rpin.objects.filter(route_id=route.pk)
    for pin in pins:
        pin.delete()
    route.delete()

    if option == 'all':
        return redirect('/rakubaru/raallreports')
    elif option == 'user':
        member_id = request.GET['member_id']
        return redirect('/rakubaru/rauserreports?member_id=' + member_id)
    return redirect('/rakubaru/raallreports')


def rauserreports(request):
    member_id = request.GET['member_id']
    member = Rmember.objects.get(id=int(member_id))
    routes = Route.objects.filter(member_id=member.pk).order_by('-id')
    reportList = getRouteListData(routes)

    return render(request, 'rakubaru/reports.html', {'reports':reportList, 'member':member})


@api_view(['GET', 'POST'])
def rasearchreportbydate(request):
    if request.method == 'POST':
        key = request.POST.get('q', None)
        option = request.GET['option']
        if option == 'all':
            routes = Route.objects.all().order_by('-id')
            routeList = getroutessearchedbydate(routes, key)
            return render(request, 'rakubaru/reports.html', {'reports':getRouteListData(routeList)})
        elif option == 'user':
            member_id = request.GET['member_id']
            member = Rmember.objects.get(id=int(member_id))
            routes = Route.objects.filter(member_id=member_id).order_by('-id')
            routeList = getroutessearchedbydate(routes, key)
            return render(request, 'rakubaru/reports.html', {'reports':getRouteListData(routeList), 'member':member})


def getroutessearchedbydate(routes, keyword):
    from datetime import datetime
    routeList = []
    for route in routes:
        if keyword.isdigit():
            keyDateObj = datetime.fromtimestamp(int(keyword)/1000)
            routeDateObj = datetime.fromtimestamp(int(route.reported_time)/1000)
            if keyDateObj.year == routeDateObj.year and keyDateObj.month == routeDateObj.month and keyDateObj.day == routeDateObj.day:
                routeList.append(route)
            else:
                routeDateObj = datetime.fromtimestamp(int(route.start_time)/1000)
                if keyDateObj.year == routeDateObj.year and keyDateObj.month == routeDateObj.month and keyDateObj.day == routeDateObj.day:
                    routeList.append(route)
                else:
                    routeDateObj = datetime.fromtimestamp(int(route.end_time)/1000)
                    if keyDateObj.year == routeDateObj.year and keyDateObj.month == routeDateObj.month and keyDateObj.day == routeDateObj.day:
                        routeList.append(route)

    return routeList


def raopenroutemap(request):
    route_id = request.GET['route_id']
    routes = Route.objects.filter(id=route_id)
    if routes.count() > 0:
        route = routes[0]
        pnts = Rpoint.objects.filter(route_id=route.pk)
        pins = Rpin.objects.filter(route_id=route.pk)

        data = {
            'route':route,
            'points':pnts,
            'pins':pins
        }

        return render(request, 'rakubaru/route.html', {'report':data})














































