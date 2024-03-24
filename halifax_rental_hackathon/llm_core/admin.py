from django.contrib import admin
from .models import Location, Amenities, Apartment, Commercial, Parking, PredictionResults

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'geographic_location', 'address', 'longitude', 'latitude', 'region', 'area')
    search_fields = ('address', 'region', 'area')

@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Amenities._meta.fields if field.name != "id"]
    search_fields = ('parking_included', 'pet_friendly', 'furnished')

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_name', 'unit', 'type', 'monthly_rent', 'lease_term', 'num_bedrooms', 'num_bathrooms', 'available_date', 'size_sqft', 'number_of_units', 'amenities')
    search_fields = ('property_name', 'type', 'available_date')
    list_filter = ('type', 'available_date', 'amenities')

@admin.register(Commercial)
class CommercialAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_name', 'unit', 'type', 'rent', 'rent_includes', 'lease', 'tenant_pays', 'rentable_area', 'useable_area', 'number_of_units', 'amenities')
    search_fields = ('property_name', 'type')
    list_filter = ('type', 'amenities')

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_name', 'type', 'parking', 'available', 'price', 'tenant_services_coordinator', 'resident_managers', 'commercial_property_manager')
    search_fields = ('property_name', 'type', 'available')
    list_filter = ('type',)

@admin.register(PredictionResults)
class PredictionResultsAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'predicted_price', 'confidence_interval_low', 'confidence_interval_high', 'prediction_date', 'apartment', 'commercial', 'parking')
    search_fields = ('predicted_price', 'prediction_date')
    list_filter = ('prediction_date',)
