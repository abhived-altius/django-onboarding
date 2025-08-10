from django.urls import path
from .views import (
    CountryListCreateAPIView,
    CountryRetrieveUpdateDestroyAPIView,
    StateListCreateAPIView,
    StateRetrieveUpdateDestroyAPIView
)

app_name = 'locations'

urlpatterns = [
    # Country URLs
    path('countries/', CountryListCreateAPIView.as_view(), name='country-list'),
    path('countries/<uuid:pk>/', CountryRetrieveUpdateDestroyAPIView.as_view(), name='country-detail'),

    # State URLS
    path('countries/<uuid:country_pk>/states/', StateListCreateAPIView.as_view(), name='state-list'),
    path('countries/<uuid:country_pk>/states/<uuid:pk>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),
]

