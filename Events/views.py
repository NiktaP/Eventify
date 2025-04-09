from django.shortcuts import render
from .models import EventsModel,EventRegistration
from .Serializer import EventRegistrationSerializer,EventSerializer_Organizer,EventSerializer_user
from rest_framework import viewsets , permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

class EventViewSet(viewsets.ModelViewSet):
    queryset = EventsModel.objects.all()
    serializer_class = EventSerializer_Organizer
    permission_classes = [permissions.IsAuthenticated]  # Fixed typo (permission_classes)
    def perform_create(self, serializer):
        serializer.save(Organizer=self.request.user)

    def destroy(self, request, pk=None):
        # چاپ برای دیباگ
        print(f"Looking for event with pk: {pk}")

        try:
            event = EventsModel.objects.get(pk=pk)
            print(f"Looking for event with pk: {event.name}")
        except EventsModel.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # بررسی تعداد ثبت‌نام‌ها
        registration_count = EventRegistration.objects.filter(event=event).count()
        if registration_count == 0:
            event.delete()
            return Response({"message": "Your registration has been successfully deleted."}, status=status.HTTP_200_OK)

        return Response({"error": "Event has registered users and cannot be deleted."},
                        status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        print("User:", request.user)
        user = request.user  # یوزر لاگین شده

        # فیلتر ایونت‌ها فقط برای یوزر لاگین شده
        events = EventsModel.objects.filter(Organizer=user)

        if not events.exists():
            return Response({"message": "No events found."}, status=status.HTTP_404_NOT_FOUND)

        # سریالایز کردن ایونت‌ها
        serializer = EventSerializer_Organizer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_all_events(self, request):
        events = EventsModel.objects.all()
        serializer = EventSerializer_user(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        try:
            event = EventsModel.objects.get(pk=pk)
        except EventsModel.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        ticket_count = request.data.get('ticket_count', 1)

        try:
            ticket_count = int(ticket_count)
            if ticket_count <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Ticket count must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        active_registrations = EventRegistration.objects.filter(
            user=user,
            event__event_status__in=['upcoming', 'active']
        ).count()

        if hasattr(user, 'event_limit') and active_registrations >= user.event_limit:
            return Response({"error": "You have reached your event registration limit."}, status=status.HTTP_400_BAD_REQUEST)

        if event.registration_status != 'open':
            return Response({"error": "You cannot register for this event."}, status=status.HTTP_400_BAD_REQUEST)

        registration, created = EventRegistration.objects.get_or_create(
            event=event,
            user=user,
            defaults={'ticket_count': ticket_count}
        )

        if not created:
            return Response({"error": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            event = EventsModel.objects.get(pk=pk)
        except EventsModel.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        registration = EventRegistration.objects.filter(user=user, event=event)

        if registration.exists():
            registration.delete()
            return Response({"message": "Your registration has been successfully deleted."}, status=status.HTTP_200_OK)

        return Response({"error": "You are not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        user = request.user
        registrations = EventRegistration.objects.filter(user=user)

        if not registrations.exists():
            return Response({"message": "No event registrations found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)















