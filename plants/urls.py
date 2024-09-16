from django.urls import path
from .views import PlantRecommendation,hello_world

urlpatterns = [
     path('PlantRecommendation/', PlantRecommendation, name='PlantRecommendation'),
     path('hello/', hello_world, name='hello_world'),
]
