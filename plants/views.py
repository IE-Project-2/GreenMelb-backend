from django.http import JsonResponse
from django.db.models import Q
from .models import Plant
import random

def PlantRecommendation(request):
    if request.method == 'GET':
        # Get query parameters
        category = request.GET.get('category')
        flowering_category = request.GET.get('flowering_category')
        location = request.GET.get('location')
        maintenance_type = request.GET.get('maintenance_type')

        # Debug: Print incoming filter values
        print(f"Category: {category}, Flowering: {flowering_category}, Location: {location}, Maintenance: {maintenance_type}")

        # Filter plants based on the selected criteria
        recommended_plants = Plant.objects.all()

        if category:
            recommended_plants = recommended_plants.filter(category__category=category)
        if flowering_category:
            recommended_plants = recommended_plants.filter(flowering_category__flowering=flowering_category)
        if location:
            recommended_plants = recommended_plants.filter(location__location=location)
        if maintenance_type:
            recommended_plants = recommended_plants.filter(maintenance_type__maintenance=maintenance_type)

        # Debug: Print the SQL query to check filtering
        print(recommended_plants.query)

        # Get all matching plants and pick one randomly
        recommended_plants = list(recommended_plants)
        print(recommended_plants)
        if recommended_plants:
            selected_plant = random.choice(recommended_plants)
            plant_data = {
                'plant_id': selected_plant.plant_id,
                'name': selected_plant.name,
                'scientific_name': selected_plant.scientific_name,
                'description': selected_plant.short_description,
                'sunlight_needs': selected_plant.location.location,
                'watering_needs': selected_plant.watering_frequency,
                'photo_url': selected_plant.photo_url
            }
            return JsonResponse(plant_data, safe=False)
        else:
            return JsonResponse({'message': 'No matching plants found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
