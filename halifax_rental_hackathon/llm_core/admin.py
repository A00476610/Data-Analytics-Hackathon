from django.contrib import admin
from .models import Apartment, Amenities, Location, Parking
# from .models import Location, Amenities, Apartment, Commercial, Parking, PredictionResults

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    # search_fields = ('address')

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Amenities._meta.fields if field.name != "id"]
    search_fields = ('num_parking', 'pet_friendly', 'furnished')

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rental_type', 'price', 'date_posted', 'move_in_date', 'agreement_type', 'num_bedrooms', 'num_bathrooms', 'size_sqft')
    search_fields = ('num_bedrooms', 'rental_type')
    list_filter = ('price', 'rental_type')

# @admin.register(Commercial)
# class CommercialAdmin(admin.ModelAdmin):
#     list_display = ('id', 'property_name', 'unit', 'type', 'rent', 'rent_includes', 'lease', 'tenant_pays', 'rentable_area', 'useable_area', 'number_of_units', 'amenities')
#     search_fields = ('property_name', 'type')
#     list_filter = ('type', 'amenities')

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'type', 'available', 'price', 'tenant_services_coordinator', 'resident_managers', 'commercial_property_manager', 'email', 'website', 'tel', 'fax', 'term', 'termination_policy', 'deposit')
    search_fields = ('price', 'type', 'available')
    list_filter = ('type',)

# @admin.register(PredictionResults)
# class PredictionResultsAdmin(admin.ModelAdmin):
#     list_display = ('id', 'location', 'predicted_price', 'confidence_interval_low', 'confidence_interval_high', 'prediction_date', 'apartment', 'commercial', 'parking')
#     search_fields = ('predicted_price', 'prediction_date')
#     list_filter = ('prediction_date',)
