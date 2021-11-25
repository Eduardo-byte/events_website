from django.shortcuts import render, redirect
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
#from time import gmtime, strftime
from ..models import Event, Venue
from ..forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 
        'events/add_event.html', 
        {
        'form': form,
        'submitted': submitted
        })

def all_events(request):
    event_list = Event.objects.all().order_by('name')
    
    return render(request, 
        'events/event_list.html', 
        {
        'event_list': event_list,
        })

def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 
        'events/show_event.html', 
        {
        'event': event,
        })

def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 
        'events/update_event.html', 
        {
        'event': event,
        'form': form,
        })

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')