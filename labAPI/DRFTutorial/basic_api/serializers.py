from rest_framework import serializers
from .models import DRFPost
from .models import dosen
from .models import mahasiswa

class DRFPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRFPost
        fields = '__all__'

class dosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = dosen
        fields = '__all__'

class mahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = mahasiswa
        fields = '__all__'
