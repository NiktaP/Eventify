# Eventify
#Eventify is an API designed to manage events, event registration, and event organizers. This API allows users to register for events, manage their events.

Features

1) Events Management:

   Create, view, update, and delete events.

   List events for specific organizers.


2) Event Registration:

   Register users for events.

   Limit the number of registrations per user.

   Delete event registrations.

# API Views


1) EventViewSet (/events/):

This view handles general operations related to events. It provides the functionality to list all events that are open to the public.

Methods:

      GET /events/: Lists all events.

2) EventOrganizerViewSet (/events_organizer/):

This view is designed for event organizers. It provides functionalities for organizers to manage events (create, update, delete) that they are responsible for.

Methods:

      GET /events_organizer/: Lists all events organized by the logged-in user.
      
      POST /events_organizer/: Allows an event organizer to create a new event.
      
      PUT /events_organizer/{id}/update_event/: Updates an existing event.
      
      DELETE /events_organizer/{id}/: Deletes an event if there are no active registrations.

3) EventRegistrationViewSet (/registrations/):

This view handles event registrations. Users can register for events, view their registrations, and cancel their registrations.

Methods:

      GET /registrations/: Lists all events the logged-in user is registered for.
      
      POST /registrations/{id}/register/: Allows the logged-in user to register for a specific event.
      
      DELETE /registrations/{id}/: Allows the logged-in user to cancel their registration for an event.
      




Response Formats

The API returns JSON data in response to requests. Here are some example responses:

Event Registration Example:

      Request: POST /registrations/1/register/

json
Copy
Edit

      [
         {
           "ticket_count": 2
         }
      ]
Response:

json
Copy
Edit

      [
         {
           "user": 1,
           "event": 1,
           "ticket_count": 2
         }
      ]
Event List Example:
      
      Request: GET /events/

Response:

json
Copy
Edit

      [
        {
          "id": 1,
          "name": "Sample Event 1",
          "date": "2025-04-10",
          "location": "New York"
        },
        {
          "id": 2,
          "name": "Sample Event 2",
          "date": "2025-04-15",
          "location": "Los Angeles"
        }
      ]

# Authentication and Permissions
The API requires users to be authenticated in order to perform certain actions such as creating events, registering for events, and viewing user-specific data.

EventOrganizerViewSet and EventRegistrationViewSet use permissions.IsAuthenticated to ensure that only authenticated users can perform the associated actions.

Event organizers can only manage events they created.