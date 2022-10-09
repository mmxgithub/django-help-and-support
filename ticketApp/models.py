from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicketStatus(models.TextChoices):
    REQUESTED = 'Requested'
    ASSIGNED = 'Assigned'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'

class SourceOfProblem(models.TextChoices):
    WEBSITE = 'Website'
    LINEBOT = 'Linebot'
    OTHERS = 'Others'

class Ticket(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(max_length = 1000)
    requestor = models.CharField(max_length = 200)
    contact_number = models.CharField(max_length = 20)
    contact_email = models.CharField(max_length = 50)
    status = models.CharField(choices=TicketStatus.choices, default=TicketStatus.REQUESTED, max_length = 20)
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    source = models.CharField(choices=SourceOfProblem.choices, max_length = 20)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

