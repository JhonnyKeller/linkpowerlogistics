from django.db import models

# Create your models here.
class information(models.Model):
    business_name = models.CharField(max_length=254)
    email = models.EmailField()
    phone_number = models.CharField(max_length=254,default='0')
    business_location_zip_code = models.CharField(max_length=8)
    weight_price_per_kg = models.FloatField()
    volume_price_per_cm_cubic = models.FloatField()
    activate_dimension_prices = models.BooleanField(default=0)
    price_per_mile = models.FloatField()
    open_time = models.CharField(max_length=64,default='09:00h')
    closing_time = models.CharField(max_length=64,default='19:00h')
    open_days_message = models.CharField(max_length=64,default='We don\'t work in the weekends')
    def __str__(self):
        return self.business_name
