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

class TicketSource(models.TextChoices):
    WEBSITE = 'Website'
    LINEBOT = 'Line bot'
    PHONECALL = 'Phone call'
    EMAIL = 'Email'

class TicketCategory(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return  self.name

class Software(models.Model):
    name = models.CharField(max_length = 50)
    version = models.CharField(max_length = 20)

    def __str__(self):
        return  self.name + ' ' + self.version
        
class Ticket(models.Model):

    company = models.CharField(max_length = 100)
    project = models.CharField(max_length = 100)
    software = models.ForeignKey(Software, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length = 100)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    description = models.TextField(max_length = 1000, null=True)
    contact_number = models.CharField(max_length = 20)
    contact_email = models.CharField(max_length = 50)
    status = models.CharField(choices=TicketStatus.choices, default=TicketStatus.REQUESTED, max_length = 20)
    assignee = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)
    source = models.CharField(choices=TicketSource.choices, default=TicketSource.PHONECALL, max_length = 20)
    created_by = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    updated_by = models.CharField(max_length = 200)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.title

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.TextField(max_length = 1000)
    created_by = models.ForeignKey(SystemUser, null=True, on_delete=models.SET_NULL)
    created_dt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  self.ticket.title + ' #' + str(self.id)

class TicketSoftware(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    # can be forign key with software table

class TicketHardware(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    # can be forign key with hardware table