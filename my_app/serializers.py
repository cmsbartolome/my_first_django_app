from rest_framework import serializers
from my_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']
        
class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    class Meta:
        model = Notes
        fields = ['id', 'description', 'createdOn', 'updatedOn', 'owner', 'title', 'status']
 



        