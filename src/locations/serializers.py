from rest_framework import serializers
from .models import Country, State, City
from drf_writable_nested.serializers import WritableNestedModelSerializer

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'country_code',
            'curr_symbol',
            'phone_code',
            'my_user'
        ]
        
        read_only_fields= ['my_user']

class StateSerializer(serializers.ModelSerializer):
    my_country_name = serializers.SerializerMethodField(read_only=True)
    my_user_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = State
        fields = [
            'id',
            'name',
            'state_code',
            'gst_code',
            'my_country', 
            'my_country_name', 
            'my_user_name' 
        ]

    def get_my_country_name(self, obj: State) -> str:
        return obj.my_country.name

    def get_my_user_name(self, obj: State) -> str:
        return obj.my_country.my_user.email

    def validate(self, data: dict) -> dict:
        country = data.get('my_country', self.instance.my_country)
        name = data.get('name', self.instance.name)

        queryset = State.objects.filter(
            my_country=country,
            name__iexact=name
        ).exclude(pk=getattr(self.instance, 'pk', None))

        if queryset.exists():
            raise serializers.ValidationError(
                f"A state with the name '{name}' already exists in {country.name}."
            )
        return data
    
class CitySerializer(serializers.ModelSerializer):
    my_state_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'city_code',
            'phone_code',
            'population',
            'avg_age',
            'num_of_adult_males',
            'num_of_adult_females',
            'my_state', # Foreign key to the parent State
            'my_state_name', # Our custom field
        ]

    def get_my_state_name(self, obj: City) -> str:
        return obj.my_state.name

    def validate(self, data: dict) -> dict:
        state = data.get('my_state', getattr(self.instance, 'my_state', None))
        name = data.get('name', getattr(self.instance, 'name', None))
        city_code = data.get('city_code', getattr(self.instance, 'city_code', None))
        population = data.get('population', getattr(self.instance, 'population', None))
        males = data.get('num_of_adult_males', getattr(self.instance, 'num_of_adult_males', 0))
        females = data.get('num_of_adult_females', getattr(self.instance, 'num_of_adult_females', 0))

        if population <= (males + females):
            raise serializers.ValidationError(
                "Population must be greater than the sum of adult males and females."
            )

        queryset = City.objects.filter(my_state=state).exclude(pk=getattr(self.instance, 'pk', None))

        if queryset.filter(name__iexact=name).exists():
            raise serializers.ValidationError(
                f"A city with the name '{name}' already exists in {state.name}."
            )

        # 3. Unique city code check
        if queryset.filter(city_code__iexact=city_code).exists():
            raise serializers.ValidationError(
                f"A city with the code '{city_code}' already exists in {state.name}."
            )

        return data
    
class NestedCitySerializer(WritableNestedModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'city_code', 'phone_code', 'population', 'avg_age', 'num_of_adult_males', 'num_of_adult_females']
    
    def validate(self, data):
        """
        Check that population is greater than the sum of adults.
        """
        # Get the relevant fields from the data dictionary for this city
        population = data.get('population')
        males = data.get('num_of_adult_males', 0)
        females = data.get('num_of_adult_females', 0)

        # Check if population was provided and if the validation fails
        if population is not None and population <= (males + females):
            # Raise an error associated with the 'population' field
            raise serializers.ValidationError({
                "population": "Population must be greater than the sum of adult males and females."
            })
        
        # Always return the full validated data dictionary
        return data



class NestedStateSerializer(WritableNestedModelSerializer):
    cities = NestedCitySerializer(many=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'state_code', 'gst_code', 'cities']



class NestedCountrySerializer(WritableNestedModelSerializer):
    states = NestedStateSerializer(many=True)

    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code', 'my_user', 'states']
        read_only_fields = ['my_user']