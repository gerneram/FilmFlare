from rest_framework import serializers
from .models import NewFilm

class TextItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewFilm
        fields = '__all__'