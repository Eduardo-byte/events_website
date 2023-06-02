from django.shortcuts import render, redirect
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
#from time import gmtime, strftime
from ..models import Event, Venue
from ..forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse
import csv
from django.contrib import messages

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
#import pagination stuff
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model


def my_events(request):
    if request.user.is_authenticated:
        events = Event.objects.filter(attendees = request.user.id)
        return render(request, 
        'events/my_events.html', 
        {
        'events': events
        })
    else:
        messages.success(request, (" You need to be be looged in "))
        return redirect('list-events')

def add_event(request):
    submitted = False
    user = request.user
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.manager = request.user
            stock.save()
            #form.fields['manager'] = user
            #form.save()
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
    if request.method == "POST":
        contains = False
        clicked = True
        searched = request.POST['searched']
        event_search = Event.objects.filter(name__contains=searched)
        if event_search:
            if searched == "":
                messages.success(request, (" You search is empty "))
                return render(request, 
                    'events/event_list.html', 
                    {
                    'searched':searched,
                    'event_search': event_search,
                    'contains': contains,
                    'clicked': clicked,
                    })
            else:
                contains = True
                messages.success(request, (" You searched for " + searched))
                return render(request, 
                    'events/event_list.html', 
                    {
                    'searched':searched,
                    'event_search': event_search,
                    'contains': contains,
                    'clicked': clicked,
                    })
        else:
            contains = False
            messages.success(request, (" No Event based on your search"))
            return render(request, 
                'events/event_list.html', 
                {
                'searched':searched,
                'event_search': event_search,
                'contains': contains,
                'clicked': clicked,
                })
    else:
        event_list = Event.objects.all().order_by('name')
        p = Paginator(Event.objects.all().order_by('name'), 1)
        page = request.GET.get('page')
        events = p.get_page(page)
        nums = "a" * events.paginator.num_pages
        
        return render(request, 
            'events/event_list.html', 
            {
            'event_list': event_list,
            'events': events,
            'nums': nums,
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
        messages.success(request, (" Event Updated successfully "))
        return redirect('list-events')
    return render(request, 
        'events/update_event.html', 
        {
        'event': event,
        'form': form,
        })

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    user = request.user
    manag = event.manager
    if request.user.is_authenticated:
        if user == manag:
            event.delete()
            messages.success(request, (" Event deleted successfully "))
            return redirect('list-events')
        else:
            messages.success(request, (" You don't have permissions to delete this event "))
            return redirect('list-events')

def regist_user_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    attendees_event = event.attendees.all()
    user = request.user
    registered = False
    for i in event.attendees.all():   
        if i.id == user.id:
            registered = True
        else:
            registered = False
    if registered:
        messages.success(request, (" you already registered "))
        return redirect('list-events')
    elif request.user.is_authenticated:
        messages.success(request, (" Registered for the event successfully "))
        event.attendees.add(str(user.id))
        return redirect('list-events')
    else:
        messages.success(request, (" You don't have permissions to regist events "))
        return redirect('list-events')