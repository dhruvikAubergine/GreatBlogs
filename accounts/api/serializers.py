from rest_framework import serializers
from accounts.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField()
    country = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'age', 'country', 'gender', 'username']

    def save(self):
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        account = User(email=self.validated_data['email'],age=self.validated_data['age'],country=self.validated_data['country'],gender=self.validated_data['gender'], username=self.validated_data['username'],)
        account.set_password(self.validated_data['password'])
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name', 'groups', 'user_permissions']


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=555, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)