from django.db import models
from datetime import datetime
from django.conf import settings

# Create your models here.
class Orders(models.Model):
	# Buy / Sell
	orderType = models.CharField(max_length=4)

	# Ticker Symbol e.g. $AAPL
	ticker = models.CharField(max_length=10)

	# Price
	price = models.DecimalField(max_digits=10, decimal_places=2)

	# Date
	transactionDate = models.DateTimeField("transaction date", default=datetime.now())

	# User
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', default=1, on_delete=models.CASCADE)

	def __str__(self):
		return self.ticker

	class Meta:
		verbose_name_plural = "Orders"