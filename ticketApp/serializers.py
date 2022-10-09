from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class CreateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ('status', 'assignee', 'created_dt', 'updated_dt')

class UpdateTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('status','assignee')

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'is_staff', 'is_active', 'is_superuser')

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
            is_superuser=validated_data['is_superuser']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, default="")

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if user.is_superuser:
            return value
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance