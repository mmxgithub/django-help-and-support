from rest_framework import serializers
from .models import Ticket, SystemUser, Client, Staff, TicketCategory, TicketComment, TicketHardware, TicketSoftware
from django.contrib.auth.models import Group

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = '__all__'


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = '__all__'
        read_only_fields = ('created_by',)


class TicketHardwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketHardware
        fields = '__all__'


class TicketSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketSoftware
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()
    # hardware = TicketHardwareSerializer(many=True)
    # software = TicketSoftwareSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ('company', 'project', 'software', 'title', 'category', 'description', 'contact_number',
                  'contact_email', 'status', 'assignee', 'source', 'created_by', 'updated_by', 'created_dt', 'updated_dt', 'comment')
        read_only_fields = ('created_by', 'updated_by', 'created_dt', 'updated_dt')

    def get_comment(self, obj):
        comments = TicketComment.objects.filter(ticket=obj)
        return TicketCommentSerializer(comments, many=True).data
    # def create(self, validated_data):
    #     validated_data.pop('hardware')
    #     validated_data.pop('software')
    #     return Ticket.objects.create(**validated_data)

class SystemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = ('username', 'password', 'is_staff',
                  'is_active', 'date_joined', 'last_login')
        read_only_fields = ('is_staff', 'date_joined', 'last_login')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ClientSerializer(serializers.ModelSerializer):
    user = SystemUserSerializer()

    class Meta:
        model = Client
        fields = ('user', )

    def create(self, validated_data):
        system_user = validated_data.get('user')
        system_user_obj = SystemUser.objects.create_user(
            is_staff=False, **system_user)
        client = Client.objects.create(user=system_user_obj)
        add_to_group(system_user_obj, 'Client')
        return client

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            super().update(instance.user, user_data)
        super().update(instance, validated_data)
        return instance


class StaffSerializer(serializers.ModelSerializer):
    user = SystemUserSerializer()

    class Meta:
        model = Staff
        fields = ('user', 'is_admin')

    def create(self, validated_data):
        system_user = validated_data.get('user')
        system_user_obj = SystemUser.objects.create_user(
            is_staff=True, **system_user)
        staff = Staff.objects.create(
            user=system_user_obj, is_admin=validated_data['is_admin'])
        if validated_data['is_admin']:
            add_to_group(system_user_obj, 'Admin')
        else:
            add_to_group(system_user_obj, 'Staff')
        return staff

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            super().update(instance.user, user_data)
        super().update(instance, validated_data)
        return instance

def add_to_group(user, group_name):
    group = Group.objects.get(name=group_name)
    user.groups.add(group)