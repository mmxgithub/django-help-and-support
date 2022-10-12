from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from . import models
from . import serializers
from . import permission

# Create your views here.
class TicketView(generics.ListCreateAPIView):
    serializer_class = serializers.TicketSerializer
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

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.ClientSerializer

class StaffView(generics.ListCreateAPIView):
    queryset = models.Staff.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.StaffSerializer

class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Staff.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.StaffSerializer

class TicketCategoryView(generics.ListCreateAPIView):
    queryset = models.TicketCategory.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.TicketCategorySerializer

class TicketCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TicketCategory.objects.all()
    permission_classes = [permission.IsSystemAdmin]
    serializer_class = serializers.TicketCategorySerializer