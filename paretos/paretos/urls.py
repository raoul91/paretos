from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('store.urls')),
    path('', include('django.contrib.auth.urls')),  # using this for login
    path('admin/', admin.site.urls),
]
