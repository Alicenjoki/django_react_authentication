from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'username', 'email', ]
        read_only_fields = ['id']


# pair serializer creates access and refresh token if a valid username and password exists
class MyTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        token['verified'] = user.profile.verified

        return token
    
#register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True,)
    print('Password')
    class Meta:
        model = User
        fields = ['email', 'username','password', 'password2']


def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError(
            {"password": "Password fields does not match"}
        )
    return attrs



def Create(self, validated_data):
    user = User.objects.create(
        username = validated_data['username'],
        email = validated_data['email'],
    )
    user.set_password(validated_data['password'])
    user.save()

    return user