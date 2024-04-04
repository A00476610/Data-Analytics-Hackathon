from django.db import models
from django.utils.timezone import now

class Location(models.Model):
    address = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        db_table = 'location'


class Amenities(models.Model):
    num_parking = models.FloatField(default=False)
    pet_friendly = models.CharField(default=False)
    furnished = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    smoking_permitted = models.CharField(default=False)
    barrier_free_entrances_ramps = models.CharField(default=False)
    visual_aids = models.CharField(default=False)
    accessible_washrooms_in_suite = models.CharField(default=False)
    heat = models.BooleanField(default=False)
    hydro = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    cable_tv = models.BooleanField(default=False)
    internet = models.BooleanField(default=False)
    laundry_unit = models.BooleanField(default=False)
    laundry_building = models.BooleanField(default=False)
    dishwasher = models.BooleanField(default=False)
    fridge_freezer = models.BooleanField(default=False)
    yard = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    building_security = models.BooleanField(default=False)
    building_elevator = models.BooleanField(default=False)
    building_gym = models.BooleanField(default=False)
    bycycle_parking = models.BooleanField(default=False)
    storage_space = models.BooleanField(default=False)

    class Meta:
        db_table = 'amenities'

class Apartment(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, default='')
    # unit = models.CharField(max_length=255, blank=True, default='')
    rental_type = models.CharField(max_length=255, blank=True, default='')
    price = models.FloatField(blank=True, null=True, default=0.0)
    date_posted = models.DateTimeField(blank=True, null=True, default=now)
    move_in_date = models.DateTimeField(blank=True, null=True, default=now)
    agreement_type = models.CharField(max_length=255, blank=True, default='')
    num_bedrooms = models.FloatField(blank=True, null=True, default=0)
    num_bathrooms = models.FloatField(blank=True, null=True, default=0)
    # image_link = models.URLField(blank=True, default='')
    size_sqft = models.CharField(blank=True, null=True, default=0)
    postal_code = models.CharField(blank=True, null=True, default=0)
    rate_per_sqft = models.FloatField(blank=True, null=True, default=0)
    lat = models.CharField(blank=True, null=True, default=0)
    long = models.CharField(blank=True, null=True, default=0)
    region = models.CharField(blank=True, null=True, default=0)
    # number_of_units = models.IntegerField(blank=True, null=True, default=0)
    amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    predicted_price = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'apartment'

# class Commercial(models.Model):
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#     property_name = models.CharField(max_length=255, blank=True, null=True, default='')
#     unit = models.CharField(max_length=255, blank=True, null=True, default='')
#     type = models.CharField(max_length=255, blank=True, null=True, default='')
#     rent = models.FloatField(blank=True, null=True, default=0)
#     rent_includes = models.CharField(max_length=255, blank=True, null=True, default='')
#     image_link = models.CharField(max_length=255, blank=True, null=True, default='')
#     lease = models.CharField(max_length=255, blank=True, null=True, default='')
#     tenant_pays = models.CharField(max_length=255, blank=True, null=True, default='')
#     rentable_area = models.FloatField(blank=True, null=True, default=0)
#     useable_area = models.FloatField(blank=True, null=True, default=0)
#     number_of_units = models.IntegerField(blank=True, null=True, default=0)
#     amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE)

class Parking(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    # property_name = models.CharField(max_length=255, blank=True, null=True, default='')
    type = models.CharField(max_length=255, blank=True, null=True, default='')
    available = models.CharField(blank=True, null=True, default=now)
    # image_link = models.CharField(max_length=255, blank=True, null=True, default='')
    price = models.FloatField(blank=True, null=True, default=0)
    tenant_services_coordinator = models.CharField(max_length=255, blank=True, null=True, default='')
    resident_managers = models.CharField(max_length=255, blank=True, null=True, default='')
    commercial_property_manager = models.CharField(max_length=255, blank=True, null=True, default='')
    email = models.CharField(max_length=255, blank=True, null=True, default='')
    website = models.CharField(max_length=255, blank=True, null=True, default='')
    tel = models.CharField(max_length=255, blank=True, null=True, default='')
    fax = models.CharField(max_length=255, blank=True, null=True, default='')
    term = models.CharField(max_length=255, blank=True, null=True, default='')
    termination_policy = models.CharField(max_length=255, blank=True, null=True, default='')
    deposit = models.CharField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'parking'

# class PredictionResults(models.Model):
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
#     predicted_price = models.FloatField(blank=True, null=True, default=0)
#     confidence_interval_low = models.FloatField(blank=True, null=True, default=0)
#     confidence_interval_high = models.FloatField(blank=True, null=True, default=0)
#     prediction_date = models.DateTimeField(blank=True, null=True, default=now)
#     apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True, blank=True)
#     commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE, null=True, blank=True)
#     parking = models.ForeignKey(Parking, on_delete=models.CASCADE, null=True, blank=True)

class Construction(models.Model):
    STATUS_CHOICES = (
        ('Proposed', 'Proposed'),
        ('Under Development', 'Under Development'),
        ('Completed', 'Completed'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('Condo', 'Condo'),
        ('Rental', 'Rental'),
    )

    property_name = models.CharField(max_length=200)
    civic_address = models.CharField(max_length=200)
    floors = models.IntegerField()
    units = models.IntegerField()
    developer = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    website = models.URLField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)
    completion_estimate = models.CharField(max_length=50, blank=True)
    retail_sq_ft = models.IntegerField(null=True, blank=True)
    district = models.CharField(max_length=100)
    image_url = models.URLField(max_length=250)

    class Meta:
        db_table = 'construction'