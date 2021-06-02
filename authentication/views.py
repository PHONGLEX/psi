from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import views

from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UserSerializer, EmailVerificationSerializer, LoginSerializer
from .utils import Util
from .models import User

import jwt


class RegisterView(generics.GenericAPIView):
	serializer_class = UserSerializer

	def post(self, request):
		# create user
		user = request.data
		serializer = UserSerializer(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# send email
		user_data = serializer.data
		user = User.objects.get(email=user_data['email'])
		token = RefreshToken.for_user(user).access_token
		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
		email_body = "Hi" + user.username + \
					" Use the link below to verify your email \n" + absurl
		data = {
			'email_body': email_body,
			'email_to': user.email,
			'email_subject': 'Verify your email'
		}
		Util.send_mail(data)

		return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerifyView(views.APIView):

	serializer_class = EmailVerificationSerializer

	token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,
											description='Description', type=openapi.TYPE_STRING)

	@swagger_auto_schema(manual_parameters=[token_param_config])
	def get(self, request):
		token = request.GET.get('token')
		try:
			payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
			user = User.objects.get(id=payload['user_id'])
			
			if not user.is_verified:
				user.is_verified = True
				user.save()
			return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

		except jwt.ExpiredSignatureError as e:
			return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
		except jwt.exceptions.DecodeError as e:
			return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


