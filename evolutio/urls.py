from django.contrib import admin
from django.urls import path, include
from evolutioapi.urls import urlpatterns  # Correct import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evolutioapi/', include('evolutioapi.urls')),  # Use 'evolutioapi.urls'
]
