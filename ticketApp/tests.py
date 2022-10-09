from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from . serializers import TicketSerializer
from . models import Ticket


class ObjectiveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(username='superuser')
        self.staff_user = User.objects.create_user(
            username='staff', is_staff=True)
        self.client_user = User.objects.create_user(
            username='client', is_staff=False)

    def test_superuser_can_create_user(self):
        self.client.force_authenticate(user=self.superuser)
        payload = {
            "username": "test_create_user",
            "password": "P@ssw9rd",
            "password2": "P@ssw9rd",
            "is_staff": False,
            "is_active": True,
            "is_superuser": False
        }
        res = self.client.post('/user/register/', data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_client_can_create_ticket(self):
        self.client.force_authenticate(user=self.client_user)
        payload = {
            "title": "test create ticket",
            "description": "description for test ticket",
            "requestor": "client",
            "contact_number": "0865505666",
            "contact_email": "client@email.com",
            "source": "Website"
        }
        res = self.client.post('/ticket/create/', data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_superuser_can_monitor_ticket(self):
        Ticket.objects.create(title='mock1', description='desc mock1', requestor='req mock1',
                              contact_number='111', contact_email='mock1@email.com', source='Website')
        Ticket.objects.create(title='mock2', description='desc mock2', requestor='req mock2',
                              contact_number='222', contact_email='mock2@email.com', source='Website')
        tickets = Ticket.objects.all().order_by('-created_dt')
        serializer = TicketSerializer(tickets, many=True)
        self.client.force_authenticate(user=self.superuser)
        res = self.client.get('/ticket/all/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_superuser_can_assign(self):
        self.client.force_authenticate(user=self.superuser)
        Ticket.objects.create(title='mock1', description='desc mock1', requestor='req mock1',
                              contact_number='111', contact_email='mock1@email.com', source='Website')
        res = self.client.patch('/ticket/update/1', {"assignee": "2"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ticket = Ticket.objects.get(pk=1)
        assignee = User.objects.get(pk=2)
        self.assertEqual(ticket.assignee, assignee)
