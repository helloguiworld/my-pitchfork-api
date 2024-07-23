from rest_framework import serializers
from ..models import SearchClick

class SearchClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchClick
        fields = '__all__'