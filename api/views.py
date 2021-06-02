from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .serializers import PsiSerializer, AirTemperatureSerializer
from .models import Psi, AirTemperature


class PsiViewSet(ModelViewSet):
	queryset = Psi.objects.all()
	serializer_class = PsiSerializer
	permission_classes = []



class AirTemperatureViewSet(ModelViewSet):
	queryset = AirTemperature.objects.all()
	serializer_class = AirTemperatureSerializer
	permission_classes = []
