from django.db import models

# Create your models here.

########################## Quetrip #############################################################################

class Member(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    picture_url = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    registered_time = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    auth_status = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    fcm_token = models.CharField(max_length=1000)


########################## ImageAgent #######################################################################################

class Imember(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Folder(models.Model):
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    pics = models.CharField(max_length=11)
    created_at = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Pic(models.Model):
    folder_id = models.CharField(max_length=11)
    url = models.CharField(max_length=50)
    status = models.CharField(max_length=20)


########################## Rakubaru #######################################################################################

class Rmember(models.Model):
    admin_id = models.CharField(max_length=11)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    picture_url = models.CharField(max_length=1000)
    role = models.CharField(max_length=30)
    registered_time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Rpoint(models.Model):
    route_id = models.CharField(max_length=11)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    comment = models.CharField(max_length=1000)
    time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Rpin(models.Model):
    route_id = models.CharField(max_length=11)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    comment = models.CharField(max_length=1000)
    time = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

class Route(models.Model):
    member_id = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    reported_time = models.CharField(max_length=50)
    status = models.CharField(max_length=50)





















































