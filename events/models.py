from django.db import models
from django.contrib.auth.models import User
import datetime
from django import forms

class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    post_code = models.CharField('Post Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')
    
    def __str__(self):
        return self.name
    
class MyClubUser(models.Model):
    #user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=30, default="default")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')
    password1 = models.CharField(max_length=200, default="eduardo_1234")
    password2 = models.CharField(max_length=200, default="eduardo_1234")

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    #venue = models.CharField(max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.SET_NULL, default="No venue for this event")
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    
        
    def __str__(self):
        return self.name
   

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255, default='')