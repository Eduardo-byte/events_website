from django.urls import path, re_path
from . import views

urlpatterns = [
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique indentifier

    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_event', views.add_event, name="add-event"), 
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('show_event/<event_id>', views.show_event, name="show-event"), 
    path('regist_event/<event_id>', views.regist_user_event, name="regist-event"), 
    path('my_events/', views.my_events, name="my-events"), 
    
    path('add_venue', views.add_venue, name="add-venue"), 
    path('list_venues', views.list_venues, name="list-venues"), 
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"), 
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('venue_updated', views.venue_updated, name="venue-updated"),
    path('search_venues', views.search_venues, name="search-venues"), 
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    
    path('converter_png', views.converter_png, name='converter-png'),
    path('download_images/', views.download_images, name='download_images'),
    # path('image_png', views.download, name='image-png'),
    ]
