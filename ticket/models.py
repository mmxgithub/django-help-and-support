from django.db import models
from django.contrib.auth.models import AbstractUser

class SystemUser(AbstractUser):
    pass

class Client(models.Model):
    user = models.OneToOneField(SystemUser, on_delete = models.CASCADE)
    # extra field to connect with company
    def __str__(self):
        return  self.user.get_username()

class Staff(models.Model):
    user = models.OneToOneField(SystemUser, on_delete = models.CASCADE)
    is_admin = models.BooleanField(default=False)
    # extra field to discribe staff eg. roles
    def __str__(self):
        return  self.user.get_username()

class TicketStatus(models.TextChoices):
    REQUESTED = 'Requested'
    ASSIGNED = 'Assigned'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'

class TicketCategory(models.Model):
    name = models.CharField(max_length = 50)

class Ticket(models.Model):

    company = models.CharField(max_length = 100)
    project = models.CharField(max_length = 100)
    title = models.CharField(max_length = 100)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    description = models.TextField(max_length = 1000, null=True)
    contact_number = models.CharField(max_length = 20)
    contact_email = models.CharField(max_length = 50)
    status = models.CharField(choices=TicketStatus.choices, default=TicketStatus.REQUESTED, max_length = 20)
    assignee = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length = 200)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.TextField(max_length = 1000)
    created_by = models.ForeignKey(SystemUser, null=True, on_delete=models.SET_NULL)
    created_dt = models.DateTimeField(auto_now_add=True)

class TicketSoftware(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    # can be forign key with software table

class TicketHardware(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    # can be forign key with hardware table