from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

# Configure Admin titles
admin.site.site_header = "My Club | Admin page"
admin.site.site_title = "My Club"
admin.site.index_title = "Admin Area"