from django.urls import path
from .views import PlantRecommendation

urlpatterns = [
    path('PlantRecommendation/', PlantRecommendation, name='plant-recommendation'),
]
