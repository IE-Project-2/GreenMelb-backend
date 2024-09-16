# predictions/urls.py
from django.urls import path
from .views import WastePredictionView

urlpatterns = [
    path('', WastePredictionView.as_view(), name='predict'),  # Use '' so it's just /api/predict/
]
