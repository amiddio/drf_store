from django.urls import path, include
from catalog.routers import router

urlpatterns = [
    path('', include(router.urls)),
]
