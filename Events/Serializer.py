from rest_framework import serializers
from .models import EventsModel, EventRegistration
from django.contrib.auth.models import User

class EventModelSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'id', 'name', 'Capacity', 'Description', 'date', 'start_time',
            'created_at', 'location', 'registration_status', 'event_type',
            'Category', 'event_status', 'registrations'
        ]
        extra_kwargs = {
            'Organizer': {'read_only': True}  # کاربر به‌طور خودکار تنظیم شود.
        }


class EventRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventRegistration
        fields = ['user', 'registered_at']

