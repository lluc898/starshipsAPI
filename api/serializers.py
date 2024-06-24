from rest_framework import serializers
from api.models import Starship

class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = '__all__'