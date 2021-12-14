from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event

#admin.site.register(Venue)
admin.site.register(MyClubUser)
class MyClubUserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2',)
    # exclude = ['password1', 'password2',]    
    
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'attendees',)
    list_display = ('name', 'event_date', 'venue',)
    list_filter = ('event_date', 'venue',)
    ordering = ('event_date',)


