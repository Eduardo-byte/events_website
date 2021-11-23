from django.shortcuts import render, redirect
import calendar 
from calendar import HTMLCalendar
from datetime import datetime
#from time import gmtime, strftime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
# to pass the variables/the content to be used on the html file you always need to : 
#or import from another file, like from .forms import VenueForm, and then on the context dictionary pass it when calling the html file.
#the same with variables, create them on the def view and pass them on the dictionary.

#Generate text file Venues List
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    
    #Designate the model
    venues = Venue.objects.all()
    
    #Create blank list
    lines = []
    
    #Loop through and output
    for venue in venues:
        lines.append(f'Venue: {venue.name}\nAddress: {venue.address}\nPhone: {venue.phone}\nPost-code: {venue.post_code}\nEmail: {venue.email_address}\nWebsite: {venue.web}\n\n\n')
        
    
    #lines = ["this is line 1 \n" , "this is line 2 \n" , "this is lie 3 \n\n" , "Eduardo is awesome! \n"]
    
    #Write to TextFile
    response.writelines(lines)
    return response

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 
        'events/add_venue.html', 
        {
        'form': form,
        'submitted': submitted
        })

def list_venues(request):
    name = False
    address = False
    if 'name' in request.GET:
        name = True
        venue_list = Venue.objects.all().order_by('name')
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list, 
            'name': name,
            'address': address,   
            })
    elif 'address' in request.GET:
        address = True
        venue_list = Venue.objects.all().order_by('address')
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list, 
            'name': name,
            'address': address,  
            })
    else:
        venue_list = Venue.objects.all().order_by('?')
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list,
            'name': name,
            'address': address,    
            })

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    event_list = Event.objects.all()
    count = 0
    event_from_venue = []
    for event in event_list:
        if count == 0:
            count = 0
        if event.venue == None:
            count = 0
        else:
            if event.venue.name == venue.name:
                count += 1
                event_from_venue.append(event)
    return render(request, 
        'events/show_venue.html', 
        {
        'venue': venue,
        'event_from_venue': event_from_venue,
        'count': count,
        })

def search_venues(request):
    if request.method == "POST":
        contains = False
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        if venues:
            contains = True
            return render(request, 
                'events/search_venues.html', 
                {
                'searched':searched,
                'venues': venues,
                'contains': contains,
                })
        else:
            contains = False
            return render(request, 
                'events/search_venues.html', 
                {
                'searched':searched,
                'venues': venues,
                'contains': contains,
                })
    else:
        return render(request, 
            'events/search_venues.html', 
            {
            })
        
def venue_updated(request):
    updated = False
    if 'updated' in request.GET:
        updated= True
    else:
        updated= False
    return render(request, 
        'events/venue_updated.html', 
        {
        'updated': updated,
        })
    
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/venue_updated?updated')
        #return redirect('list-venues')
    return render(request, 
        'events/update_venue.html', 
        {
        'venue': venue,
        'form': form,
        })

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

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

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Eduardo"

    # convert to capitalize
    # month = month.title()
    month = month.capitalize()
    #convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create calendar
    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )

    #get current year
    now = datetime.now()
    current_year = now.year

    #get current time
    time = now.strftime('%-I:%M %p')

    return render(request, 
        'events/home.html', 
        {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
        })