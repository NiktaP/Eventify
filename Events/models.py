from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    event_limit = models.IntegerField(default=3)
    #active_event=models.IntegerField(default=0)


    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username

def get_today_date():
    return timezone.now().date()

class EventsModel(models.Model):

    name = models.CharField(max_length=25)
    Capacity = models.IntegerField()

    Description = models.CharField(max_length=200)
    date = models.DateField(default=get_today_date)
    start_time = models.TimeField(default=timezone.now,null=False,blank=False)
    created_at = models.DateField(default=get_today_date)
    location = models.CharField(max_length=255, null=False, blank=False)
    Organizer = models.ForeignKey(User, on_delete=models.CASCADE,default= 1)
    price = models.FloatField(null=False,blank = False,default=0.0)



    REGISTRATION_CHOICES = [
        ('full', 'full'),
        ('open', 'open'),
        ('pending', 'pending'),
    ]

    registration_status = models.CharField(
        max_length=10,
        choices=REGISTRATION_CHOICES,
        default='pending',
    )
    Type_CHOICES=[
        ('online', 'online'),
        ('in-person', 'In-person'),
    ]
    event_type=models.CharField(
        max_length=10,
        choices=Type_CHOICES,
        default='in-person',
    )

    Category = models.CharField(max_length=25)

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('cancelled', 'Canselled'),
        ('finished','Finished'),
    ]
    event_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='upcoming',
    )

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    event = models.ForeignKey(EventsModel, related_name='registrations', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    registered_at = models.DateTimeField(auto_now_add=True)
    ticket_count = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.user.username} registered for {self.event.name}'

    class Meta:
        unique_together = ('event', 'user')  # Ensure one registration per user per event




