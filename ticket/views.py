from rest_framework import generics
from rest_framework.permissions import IsAdminUser
import django_filters.rest_framework
from . import models
from . import serializers
from . import permission

class TicketView(generics.ListCreateAPIView):
    serializer_class = serializers.TicketSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields  = [f.name for f in models.Ticket._meta.get_fields()]
    def get_queryset(self):
        if self.request.user.is_staff:
            return models.Ticket.objects.all()
        return models.Ticket.objects.filter(created_by=self.request.user.client)
    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user.client)
    
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TicketSerializer
    permission_classes = [IsAdminUser]
    queryset = models.Ticket.objects.all()
    def perform_update(self, serializer):
        req = serializer.context['request']
        serializer.save(updated_by=req.user.get_username())

class CommentView(generics.CreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.TicketCommentSerializer
    def perform_create(self, serializer):
        req = serializer.context['request']
        serializer.save(created_by=req.user.client)

class ClientView(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.ClientSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields  = [f.name for f in models.Client._meta.get_fields()]

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.ClientSerializer

class StaffView(generics.ListCreateAPIView):
    queryset = models.Staff.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.StaffSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields  = [f.name for f in models.Staff._meta.get_fields()]

class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Staff.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.StaffSerializer

class TicketCategoryView(generics.ListCreateAPIView):
    queryset = models.TicketCategory.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.TicketCategorySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields  = [f.name for f in models.TicketCategory._meta.get_fields()]

class TicketCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TicketCategory.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.TicketCategorySerializer