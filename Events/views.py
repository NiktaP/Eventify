from django.shortcuts import render
from .models import EventsModel,EventRegistration
from .Serializer import EventRegistrationSerializer,EventModelSerializer
# Create your views here.

class EventViewSet(viewsets.ModelViewSet):

    queryset = EventsModel.objects.all()
    serializer_class = EventsModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(Organizer=self.request.user)

    def delete(self,pk):
        try:
            event = EventsModel.objects.get(pk=pk)
        except EventsModel.DoesNotExist:
                return Response({"error" : "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        regestration_count=EventRegistration.objects.filter(event=event).count()
        if regestration_count==0:
            event.delete()
            return Response({"message": "Your registration has been successfully deleted."}, status=status.HTTP_200_OK)

        return Response({"error": "Event has registered users and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)




class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event = EventModel.objects.get(pk=pk)
        ticket_count = request.data.get('ticket_count',1)

        try:
            ticket_count = int(ticket_count)
            if ticket_count <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Ticket count must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        active_registrations = EventRegistration.objects.filter(
            user=user,
            event__event_status__in=['upcoming', 'active']
        ).count()

        if active_registrations >= user.event_limit:
            return Response({"error": "You have reached your event registration limit."}, status=status.HTTP_400_BAD_REQUEST)

        if event.registration_status != 'open':
            return Response({"error": "You cannot register for this event."}, status=status.HTTP_400_BAD_REQUEST)

        registration, created = EventRegistration.objects.get_or_create(
                event=event,
                user=request.user,
                defaults={'ticket_count': ticket_count}
            )

        if not created:
            return Response({"error": "You are already registered for this event."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self,request, pk):

        try:
            event = EventModel.objects.get(pk=pk)
        except EventModel.DoesNotExist:
            return Response({"error" : "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        registration = EventRegistration.objects.filter(
            user=user,
            event=event,
        )

        if registration.exists():
            registration.delete()
            return Response({"message": "Your registration has been successfully deleted."}, status=status.HTTP_200_OK)

        return Response({"error": "You are not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):

        user=request.user
        regestration=EventRegistration.objects.filter(
            user=user,
        )
        if not registrations.exists():
            return Response({"message": "No event registrations found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventRegistrationSerializer(registrations, many=True)

        return Response(serializer.data, status=status.HTTP_200)
















