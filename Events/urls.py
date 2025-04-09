from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventRegistrationViewSet

# Create a router to register the viewsets
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'registrations', EventRegistrationViewSet, basename='eventregistration')

# Add the router's URLs to urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Includes all registered routes
]
