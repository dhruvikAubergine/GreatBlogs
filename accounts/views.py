from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from accounts.serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
)
from accounts.models import User
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterView(APIView):
    """
    RegisterView is used to register user to the system.
    """
    def post(self, request):
        """
        RegisterView's post method is for create new user
        """
        serializer = RegisterSerializer(data=request.data)
        # Validation of fields using serializer
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data
            user = User.objects.get(email=user_data["email"])
            # Get access token from jwt
            token = RefreshToken.for_user(user).access_token
            # Fetch current site domain
            current_site = get_current_site(request).domain
            relativeLink = reverse("email-verify")
            absurl = "http://" + current_site + relativeLink + "?token=" + str(token)
            # Email body for send email activation link
            email_body = (
                "Hi "
                + user.username
                + " Use the link below to verify your email \n"
                + absurl
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Verify your email",
            }
            # Send email with data
            Util.send_email(data)

            return Response(
                {"msg": "You are register successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Something went wrong, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """
    LoginView used to authenticate user with jwt token.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        LoginView's post method for authenticate the user details.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            [{"msg": "You are login successfully"}, serializer.data],
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(APIView):
    """
    VerifyEmailView used to verify email for account activation.
    """
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        """
        VerifyEmailView's get method used to verify email.
        """
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                # Make is_verified field true if user click on the activation link.
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(APIView):
    """
    ChangePassword used for change the password of user's account.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        if not user.check_password(data["old_password"]):
            return Response(
                {"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(data["password"])
        user.save()
        return Response(
            [{"success": "Your password has been changed"}, serializer.data]
        )


class UpdateProfileView(APIView):
    """
    UpdateProfileView used for update the profile.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UpdateProfileSerializer(
            user, context={"request": self.context["request"]}, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                [{"success": "Your profile has been updated"}, serializer.data]
            )
        else:
            return Response(
                {"error": "Something went wrong, Please try again"},
                status=status.HTTP_400_BAD_REQUEST,
            )


