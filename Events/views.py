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
    def list(self, request):
        events = EventsModel.objects.all()
        serializer = EventSerializer_user(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventOrganizerViewSet(viewsets.ModelViewSet):
    queryset = EventsModel.objects.all()
    serializer_class = EventSerializer_Organizer
    permission_classes = [permissions.IsAuthenticated]  # Fixed typo (permission_classes)
    def perform_create(self, serializer):
        serializer.save(Organizer=self.request.user)

    def destroy(self, request, pk=None):

        event=get_object_or_404(EventsModel, pk=pk)
        registration_count = EventRegistration.objects.filter(event=event).count()
        if registration_count == 0:
            event.delete()
            return Response({"message": "Your registration has been successfully deleted."}, status=status.HTTP_200_OK)

        return Response({"error": "Event has registered users and cannot be deleted."},
                        status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        print("User:", request.user)
        user = request.user
        events = EventsModel.objects.filter(Organizer=user)
        if not events.exists():
            return Response({"message": "No events found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer_Organizer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['put'])  # /events/{id}/update_event/
    def update_event(self, request, pk=None):
        event=get_object_or_404(EventsModel, pk=pk)

        if event.Organizer != request.user:
            return Response({'error': 'You are not the organizer of this event.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer_user(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = get_object_or_404(EventsModel, pk=pk)
        user = request.user


        if event.registration_status != 'open':
            return Response({"error": "Registration is closed for this event."},
                            status=status.HTTP_400_BAD_REQUEST)


        active_registrations = EventRegistration.objects.filter(
            user=user,
            event__event_status__in=['upcoming', 'active']
        ).count()

        if hasattr(user, 'event_limit') and active_registrations >= user.event_limit:
            return Response({"error": "You have reached your registration limit."},
                            status=status.HTTP_400_BAD_REQUEST)


        if EventRegistration.objects.filter(user=user, event=event).exists():
            return Response({"error": "You are already registered for this event."},
                            status=status.HTTP_400_BAD_REQUEST)


        data = {
            'user': user.id,
            'event': event.id,
            'ticket_count': request.data.get('ticket_count', 1)
        }

        serializer = EventRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        event=get_object_or_404(EventsModel, pk=pk)
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















