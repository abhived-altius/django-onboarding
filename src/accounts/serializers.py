from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True,required=True)
    
    
    class Meta:
        model = CustomUser
        fields = ['id','email','password']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
        