from rest_framework import serializers
from accounts.models import User


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