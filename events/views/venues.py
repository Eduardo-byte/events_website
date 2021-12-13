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

#import pagination stuff
from django.core.paginator import Paginator



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


#Generate PDF file Venues List
def venue_pdf(request):
    #create a Bytestream buffer
    buf = io.BytesIO()
    
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    
    #Designate the model
    venues = Venue.objects.all()
    
    #Create blank list
    lines = []
    
    #Loop through and output
    for venue in venues:
        lines.append(f'Venue: {venue.name}')
        lines.append(f'Address: {venue.address}')
        lines.append(f'Post Code: {venue.post_code}')
        lines.append(f'Phone Number: {venue.phone}')
        lines.append(f'Email Address: {venue.email_address}')
        lines.append(f'Web Site: {venue.web}')
        lines.append(" ")
        
        
    #loop thorugh the array lines and write to the pdf
    for line in lines:
        textob.textLine(line)
    
    #finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    #return something
    return FileResponse(buf, as_attachment=True, filename="venues.pdf")
    
    
#Generate CSV/Excel file Venues List
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    
    #Create a csv writer
    writer = csv.writer(response)
    
    #Designate the model
    venues = Venue.objects.all()
    
    #add column headings to csv file
    writer.writerow(['Venue Name' , 'Address' , 'Post code' , 'Phone' , 'Email' , 'Web address'])

    #Loop through and output
    for venue in venues:
        writer.writerow([venue.name , venue.address , venue.post_code ,  venue.phone, venue.email_address , venue.web])
        
    return response

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            #form.save()
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
        
        p = Paginator(Venue.objects.all().order_by('name'), 2)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list,
            'venues': venues,
            'name': name,
            'address': address,
            'nums': nums,    
            })
    elif 'address' in request.GET:
        address = True
        venue_list = Venue.objects.all().order_by('address')
        
        p = Paginator(Venue.objects.all().order_by('address'), 2)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list,
            'venues': venues,
            'name': name,
            'address': address,
            'nums': nums,    
            })
    else:
        #venue_list = Venue.objects.all().order_by('?')
        venue_list = Venue.objects.all().order_by('name')
        
        #set up pagination
        p = Paginator(Venue.objects.all().order_by('name'), 2)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        return render(request,
            'events/venues.html',
            {
            'venue_list': venue_list,
            'venues': venues,
            'name': name,
            'address': address,
            'nums': nums,    
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
        updated = True
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