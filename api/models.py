from django.db import models



class Psi(models.Model):
	region = models.CharField(max_length=10)
	o3_sub_index = models.FloatField()
	pm10_twenty_four_hourly = models.FloatField()
	pm10_sub_index = models.FloatField()
	co_sub_index = models.FloatField()
	pm25_twenty_four_hourly = models.FloatField()
	so2_sub_index = models.FloatField()
	updated_timestamp = models.DateTimeField()

	def __str__(self):
		return self.region + '-' + updated_timestamp.strftime("%m/%d/%Y, %H:%M:%S")


class AirTemperature(models.Model):
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=255)
	timestamp = models.DateTimeField()
	temperature = models.FloatField()

	def __str__(self):
		return self.code + '-' + timestamp.strftime("%m/%d/%Y, %H:%M:%S")
