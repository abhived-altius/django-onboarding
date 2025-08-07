from django.db import models
from accounts.models import CustomUser
import uuid

# Create your models here.

class Country(models.Model):
    id             = models.UUIDField(primary_key = True, default = uuid.uuid4, editable=False)
    name           = models.CharField(max_length=100)
    country_code   = models.CharField(max_length =10,unique=True)
    curr_symbol    = models.CharField(max_length =5)
    phone_code     = models.CharField(max_length =10, unique=True)
    my_user        = models.ForeignKey(CustomUser, null=True,on_delete=models.SET_NULL)
    def __str__(self) -> str:
        return self.name


class State(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name            = models.CharField(max_length=100)
    state_code      = models.CharField(max_length=10, unique=True)
    gst_code        = models.CharField(max_length=3, null=True,blank=True)
    my_country      = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="states")

    def __str__(self) -> str:
        return self.name

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                    = models.CharField(max_length=100)
    city_code               = models.CharField(max_length=100)
    phone_code              = models.CharField(max_length=10)
    population              = models.PositiveIntegerField()
    avg_age                 = models.FloatField()
    num_of_adult_males      = models.PositiveIntegerField()
    num_of_adult_females    = models.PositiveIntegerField()
    my_state                = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    def __str__(self) -> str:
        return self.name
    
    