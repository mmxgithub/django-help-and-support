from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from .models import Ticket
from .serializers import TicketSerializer, CreateTicketSerializer, UpdateTicketSerializer, RegisterSerializer, ChangePasswordSerializer, UserSerializer
from .permission import StaffSelfAdminAll, Admin

class TicketCreator(generics.CreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = CreateTicketSerializer

class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all().order_by('-created_dt')
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]

class StaffTicketList(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]
    def get_queryset(self):
       return Ticket.objects.filter(assignee=self.request.user)

class TicketUpdator(generics.UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = UpdateTicketSerializer
    permission_classes = [StaffSelfAdminAll]

class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [Admin]
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [Admin]
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [Admin]
    serializer_class = UserSerializer