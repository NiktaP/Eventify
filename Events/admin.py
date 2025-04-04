from django.contrib import admin
from .models import EventsModel,EventRegistration
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'Capacity', 'date', 'start_time', 'event_status', 'registration_status', 'event_type')
    list_filter = ('event_status', 'event_type', 'registration_status')
    search_fields = ('name', 'description', 'location')

admin.site.register(EventsModel,EventAdmin)

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'registered_at')
    list_filter = ('event','user')
    search_fields = ('event__name','user__name')

admin.site.register(EventRegistration, EventRegistrationAdmin)