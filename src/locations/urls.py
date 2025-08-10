from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CityListCreateAPIView,
    CityRetrieveUpdateDestroyAPIView,
    CountryListCreateAPIView,
    CountryRetrieveUpdateDestroyAPIView,
    StateListCreateAPIView,
    StateRetrieveUpdateDestroyAPIView,
    CountryNestedViewSet,
)

app_name = 'locations'

router = DefaultRouter()
router.register(r'nested-countries', CountryNestedViewSet, basename='nested-country')


urlpatterns = [
    # Country URLs
    path('countries/', CountryListCreateAPIView.as_view(), name='country-list'),
    path('countries/<uuid:pk>/', CountryRetrieveUpdateDestroyAPIView.as_view(), name='country-detail'),

    # State URLS
    path('countries/<uuid:country_pk>/states/', StateListCreateAPIView.as_view(), name='state-list'),
    path('countries/<uuid:country_pk>/states/<uuid:pk>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),
    path('countries/<uuid:country_pk>/states/', StateListCreateAPIView.as_view(), name='state-list'),
    path('countries/<uuid:country_pk>/states/<uuid:pk>/', StateRetrieveUpdateDestroyAPIView.as_view(), name='state-detail'),
    path('countries/<uuid:country_pk>/states/<uuid:state_pk>/cities/', CityListCreateAPIView.as_view(), name='city-list'),
    path('countries/<uuid:country_pk>/states/<uuid:state_pk>/cities/<uuid:pk>/', CityRetrieveUpdateDestroyAPIView.as_view(), name='city-detail'),
]

urlpatterns += router.urls
