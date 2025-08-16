from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/rides/', include('rides.urls')),
    path('api/emergency/', include('emergency.urls')),
    path('api/assistance/', include('assistance.urls')),
]
