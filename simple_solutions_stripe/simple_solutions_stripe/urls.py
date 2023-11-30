from django.contrib import admin
from django.urls import path, include

import items.urls as items_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(items_urls))
]
