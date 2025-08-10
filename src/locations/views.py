from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, pagination
from .models import Country, State, City
from .serializers import CountrySerializer, StateSerializer, CitySerializer, NestedCountrySerializer
from rest_framework.pagination import CursorPagination

# Create your views here.

# Add this new pagination class
class CountryCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'  # Order by the 'id' field, which is a unique UUID and always exists


class CountryListCreateAPIView(generics.ListCreateAPIView):
    """
    API View to list all countries for a user or to create a new one
    """
    
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CountryCursorPagination  # <-- ADD THIS LINE
        
    def get_queryset(self):
        return Country.objects.filter(my_user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(my_user=self.request.user)
    
class CountryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Country.objects.filter(my_user=self.request.user)
    
class StateListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list or create states for a specific country.
    """
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        country_pk = self.kwargs['country_pk']
        return State.objects.filter(
            my_country__pk=country_pk,
            my_country__my_user=self.request.user
        )

    def perform_create(self, serializer):
        country_pk = self.kwargs['country_pk']
        country = get_object_or_404(Country, pk=country_pk, my_user=self.request.user)
        serializer.save(my_country=country)


class StateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        country_pk = self.kwargs['country_pk']
        return State.objects.filter(
            my_country__pk=country_pk,
            my_country__my_user=self.request.user
        )
class CityListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list or create cities for a specific state.
    """
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        state_pk = self.kwargs['state_pk']
        return City.objects.filter(
            my_state__pk=state_pk,
            my_state__my_country__my_user=self.request.user
        )

    def perform_create(self, serializer):
        country_pk = self.kwargs['country_pk']
        state_pk = self.kwargs['state_pk']
        state = get_object_or_404(
            State,
            pk=state_pk,
            my_country__pk=country_pk,
            my_country__my_user=self.request.user
        )
        serializer.save(my_state=state)


class CityRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        state_pk = self.kwargs['state_pk']
        return City.objects.filter(
            my_state__pk=state_pk,
            my_state__my_country__my_user=self.request.user
        )


class CountryNestedViewSet(viewsets.ModelViewSet):
    serializer_class = NestedCountrySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CountryCursorPagination
    
    def get_queryset(self):
        return Country.objects.filter(my_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(my_user=self.request.user)