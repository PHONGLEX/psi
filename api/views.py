from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, views
from rest_framework.response import Response

from datetime import datetime
from .serializers import PsiSerializer, AirTemperatureSerializer
from .models import Psi, AirTemperature

import pytz

utc=pytz.UTC


class PsiViewSet(ModelViewSet):
	queryset = Psi.objects.all()
	serializer_class = PsiSerializer
	permission_classes = [IsAuthenticated,]


class AirTemperatureViewSet(ModelViewSet):
	queryset = AirTemperature.objects.all()
	serializer_class = AirTemperatureSerializer
	permission_classes = [IsAuthenticated,]


# class PsiSearchView(views.APIView):
# 	serializer_class = PsiSerializer

# 	def get(self, request, **kwargs):
# 		date = kwargs.get("date")
# 		date_obj = datetime.strptime(date, '%Y-%m-%d')
# 		raw_data = Psi.objects.filter(updated_timestamp__date__gte=date)[:6]
		
# 		if len(raw_data) > 0:
# 			# serializer = PsiSerializer(data=list(raw_data)
# 			# 	, many=isinstance(list(raw_data), list))
# 			# serializer.is_valid(raise_exception=True)
# 			# import pdb
# 			# pdb.set_trace()

# 			return Response({'psi': list(raw_data)})
# 		return Response([])

class PsiSearchView(generics.ListAPIView):
	serializer_class = PsiSerializer
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		date = self.kwargs.get("date")
		date_obj = datetime.strptime(date, '%Y-%m-%d')
		data = Psi.objects.filter(updated_timestamp__date__gte=date)[:6]
		return data



# class AirTemperatureSearchView(generics.GenericAPIView):

# 	def get(self, request):
# 		date = request.GET.get('date')

# 		raw_data = AirTemperature.objects.filter(timestamp__gte=date)[:1]

# 		if len(raw_data) > 0:
# 			result = PsiSerializer(data=raw_data)

# 			return Response(result.data, status=status.HTTP_200_OK)	
# 		return Response([], status=status.HTTP_200_OK)	

class AirTemperatureSearchView(views.APIView):

	serializer_class = AirTemperatureSerializer
	# permission_classes = (IsAuthenticated,)

	def get(self, request, **kwargs):

		# import pdb
		# pdb.set_trace()
		date = self.kwargs.get("date")
		date_obj = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S')
		air_temperature = AirTemperature.objects.latest('timestamp')

		air_temperature.timestamp = air_temperature.timestamp.replace(tzinfo=utc)
		date_obj = date_obj.replace(tzinfo=utc)
		
		if air_temperature.timestamp >= date_obj:
			return Response({'data': air_temperature})	

		return Response({})

