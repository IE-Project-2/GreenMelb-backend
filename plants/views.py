from django.shortcuts import render
from .models import Plant,Plant_Needs
from django.http import JsonResponse
from .models import Plant

def PlantRecommendation(request):
    if request.method == 'GET':
        # Get query parameters
        category = request.GET.get('category')
        sunlight_needs = request.GET.get('sunlight_needs')
        watering_needs = request.GET.get('watering_needs')

        # Filter plants based on the selected criteria
        recommended_plants = Plant.objects.all()
        if category:
            recommended_plants = recommended_plants.filter(category=category)
        if sunlight_needs:
            recommended_plants = recommended_plants.filter(sunlight_needs=sunlight_needs)
        if watering_needs:
            recommended_plants = recommended_plants.filter(watering_needs=watering_needs)

        # Serialize plant data
        plants_data = list(recommended_plants.values())

        return JsonResponse(plants_data, safe=False)

    # Return an empty JSON response or error if not a GET request
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def hello_world(request):
    return JsonResponse({'message': 'Hello, World!'})
