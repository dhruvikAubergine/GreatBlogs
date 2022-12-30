from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.core.validators import EmailValidator


class RegisterSerializer(serializers.ModelSerializer):
    """
    RegisterSerializer used to validate fields.
    """
    age = serializers.IntegerField()
    country = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ["id", "email", "password", "age", "country", "gender", "username"]

    def save(self):
        """
        Save method is used to save the user details into the database.
        """
        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists!"})

        account = User(
            email=self.validated_data["email"],
            age=self.validated_data["age"],
            country=self.validated_data["country"],
            gender=self.validated_data["gender"],
            username=self.validated_data["username"],
        )
        account.set_password(self.validated_data["password"])
        account.save()
        return account


class EmailVerificationSerializer(serializers.ModelSerializer):
    """
    EmailVerificationSerializer is used to validate the user's email.
    """
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    """
    LoginSerializer is used to validate fields.
    """
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=555, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        # Validate user with email id and password
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {"email": user.email, "username": user.username, "tokens": user.tokens}


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    ChangePasswordSerializer used to validate old and new password.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "password"]


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    UpdateProfileSerializer used to validate updated fields.
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "age", "country", "gender", "username"]
        extra_kwargs = {"email": {"validators": [EmailValidator]}}

    def update(self, instance, validated_data):
        # Update profile details with validated data
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.age = validated_data["age"]
        instance.gender = validated_data["gender"]
        instance.country = validated_data["country"]

        instance.save()
        return instance