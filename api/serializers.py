from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True},
                        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Las contraseñas son diferentes'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''), 
            last_name=validated_data.get('last_name', ''), 
            email=validated_data.get('email', '')            
        )

        try:
            group = Group.objects.get(name='Explorador')
            user.groups.add(group)
        except Group.DoesNotExist:
            raise serializers.ValidationError({'group': 'El grupo especificado no existe'})

        return user



