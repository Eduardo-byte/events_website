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