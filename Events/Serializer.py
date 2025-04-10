from rest_framework import serializers
from .models import EventsModel, EventRegistration
from django.contrib.auth.models import User

class EventSerializer_Organizer(serializers.ModelSerializer):

    class Meta:
        model = EventsModel
        fields = [
            'id', 'name', 'Capacity', 'Description', 'date', 'start_time',
            'created_at', 'location', 'registration_status', 'event_type',
            'Category', 'event_status','Organizer'
        ]
        extra_kwargs = {
            'Organizer': {'read_only': True}  # کاربر به‌طور خودکار تنظیم شود.
        }
class EventSerializer_user(serializers.ModelSerializer):
    class Meta:
        model=EventsModel
        fields = [
            'id','name','Description', 'date', 'start_time',
            'event_type','location', 'registration_status',
            'Category', 'event_status', 'Organizer'
        ]

class EventRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventRegistration

        fields = ['user', 'registered_at','event','ticket_count']

    def validate_ticket_count(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ticket count must be a positive integer.")
        return value

