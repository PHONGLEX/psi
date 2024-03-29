from django.urls import path, include

from rest_framework import routers


from . import views

routes = routers.DefaultRouter()
routes.register("psi", views.PsiViewSet, basename="employee")
routes.register("air-temperature", views.AirTemperatureViewSet, basename="employee")

urlpatterns = [ 
	path('', include(routes.urls)),
	path('psi-search/<date>', views.PsiSearchView.as_view()),
	path('air-temperature-search/<date>', views.AirTemperatureSearchView.as_view()),
]