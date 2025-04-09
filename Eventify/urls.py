from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('Events.urls')),# Connects to the urls.py file in the events app
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
