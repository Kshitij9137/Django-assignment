from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signals/', include('signals_demo.urls')),
    path('custom/', include('custom_classes.urls')),
]
