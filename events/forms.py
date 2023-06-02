from django import forms  
from django.forms import ModelForm, widgets
from .models import Venue, Event, MyClubUser, Image

#Create a venue Form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        #fields = "__all__"
        fields = ('name', 'address', 'post_code', 'phone', 'web', 'email_address', 'venue_image' )
        labels = {
            'name': '',
            'address': '',
            'post_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue image': '',
            
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'post_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone number'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email address'})
        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description' )
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue' : 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': ''
        } 
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'event_date': forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            'venue' : forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
            'manager': forms.HiddenInput(),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description'})
        }
        
class MyClubUserForm(ModelForm):
    class Meta:
        model = MyClubUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
        # exclude = ["password1"]
        
class ImageForm(forms.ModelForm):
    """Form for the image model"""
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ('image',)
        

