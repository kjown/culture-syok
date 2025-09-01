from django.urls import path
from .views import GCSJsonView

urlpatterns = [
    path('api/<str:platform>/', GCSJsonView.as_view(), name='gcs-json'),
]