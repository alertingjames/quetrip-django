from rest_framework import serializers
from .models import Member, Imember, Folder, Pic, Rmember, Route, Rpoint, Rpin


################# Quetrip #####################################################################

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

################# ImageAgent #######################################################################################

class ImemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imember
        fields = ('__all__')

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ('__all__')

class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ('__all__')


################# Rakubaru #######################################################################################

class RmemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rmember
        fields = ('__all__')

class RpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rpoint
        fields = ('__all__')

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('__all__')

class RpinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rpin
        fields = ('__all__')




























































