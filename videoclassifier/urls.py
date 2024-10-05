from django.urls import path
from .views import classify_image, video_feed, capture_and_classify_frame

urlpatterns = [
    path('classify_image/', classify_image, name='classify_image'),
    path('video_feed/', video_feed, name='video_feed'),
    path('capture_and_classify_frame/', capture_and_classify_frame, name='capture_and_classify_frame'),
]
