from django.http import JsonResponse, StreamingHttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import torch
import cv2
import os
import numpy as np

# Load YOLOv5 model when the server starts
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    print("YOLOv5 model loaded successfully")
except Exception as e:
    print(f"Error loading YOLOv5 model: {str(e)}")

# Waste categories dictionary

waste_categories = {
    'recyclable': [
        'bottle', 'can', 'paper', 'cardboard', 'plastic', 'cup', 'glass bottle', 'tin', 
        'aluminum', 'foil', 'plastic bag', 'straw', 'food container', 'magazine', 
        'newspaper', 'catalog', 'jar', 'milk carton', 'juice carton', 'soda can', 
        'water bottle', 'metal', 'shampoo bottle', 'detergent bottle', 'wrapping paper', 
        'plastic utensils', 'egg carton', 'cardboard box', 'envelope', 'aluminum can', 
        'metal can', 'steel', 'tin can', 'takeout container', 'plastic lid', 'card'
    ],
    'ewaste': [
        'cell phone', 'laptop', 'remote', 'tablet', 'computer', 'keyboard', 'mouse', 
        'charger', 'headphones', 'earbuds', 'monitor', 'television', 'printer', 'scanner', 
        'fax machine', 'camera', 'smartwatch', 'game console', 'dvd player', 'blu-ray player', 
        'router', 'modem', 'hard drive', 'flash drive', 'memory card', 'cord', 'cable', 
        'microwave', 'oven', 'stereo', 'speakers', 'projector', 'calculator', 'battery', 'batteries'
    ],
    'organic': [
        'apple', 'banana', 'carrot', 'orange', 'broccoli', 'lettuce', 'cucumber', 'tomato', 
        'grape', 'strawberry', 'pear', 'pineapple', 'peach', 'plum', 'kiwi', 'cherry', 
        'watermelon', 'mango', 'spinach', 'onion', 'pepper', 'avocado', 'potato', 'sweet potato', 
        'corn', 'peas', 'beans', 'eggplant', 'beet', 'celery', 'mushroom', 'zucchini', 
        'garlic', 'lemon', 'lime', 'ginger', 'cabbage', 'pumpkin', 'squash', 'radish', 'coconut',
        'eggshell', 'egg', 'coffee grounds', 'tea leaves', 'bread', 'cereal', 'pasta', 'rice', 'oatmeal',
        'chicken bone', 'fish bone', 'meat scraps'
    ]
}


# Classify waste
def classify_waste(label):
    for category, items in waste_categories.items():
        if label.lower() in items:
            return category
    return None

# Detect and classify waste in an image
def detect_and_classify_waste_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise Exception(f"Failed to read image from path: {image_path}")

        results = model(img)
        detected_objects = results.pandas().xyxy[0]

        waste_classification_counts = {'recyclable': 0, 'ewaste': 0, 'organic': 0}
        for idx, obj in detected_objects.iterrows():
            label = obj['name']
            confidence = obj['confidence']
            if confidence > 0.2: 
                category = classify_waste(label)
                if category:
                    waste_classification_counts[category] += 1

        results.render()
        output_image_path = image_path.replace('.jpg', '_result.jpg')
        cv2.imwrite(output_image_path, np.squeeze(results.ims))

        return waste_classification_counts, output_image_path
    except Exception as e:
        print(f"Error during classification: {str(e)}")
        raise e

# API to classify an image
def classify_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)

            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            counts, output_image_path = detect_and_classify_waste_image(image_path)
            response_data = {
                'counts': counts,
                'output_image_url': os.path.join(settings.MEDIA_URL, os.path.basename(output_image_path))
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request, no image provided'}, status=400)

@csrf_exempt
def capture_and_classify_frame(request):
    if request.method == 'POST':
        try:
            # Open video capture
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Error: Could not open video device")
            
            # Capture the frame
            ret, frame = cap.read()
            if not ret:
                raise Exception("Error: Failed to capture frame")

            # Define file name and paths
            filename = 'snapshot.jpg'
            snapshot_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Save the captured frame as a snapshot
            cv2.imwrite(snapshot_path, frame)

            # Run YOLOv5 model on the frame
            results = model(frame)

            # Extract detected objects
            detected_objects = results.pandas().xyxy[0]

            # Process each detected object
            total_classifications = {'recyclable': 0, 'ewaste': 0, 'organic': 0}
            detected_categories = set()  # To store detected categories for the frontend

            font_scale = 0.6
            font_thickness = 2

            for idx, obj in detected_objects.iterrows():
                label = obj['name']
                confidence = obj['confidence']
                xmin, ymin, xmax, ymax = int(obj['xmin']), int(obj['ymin']), int(obj['xmax']), int(obj['ymax'])

                # Only classify objects with confidence > 0.3
                if confidence > 0.3:
                    # Classify the object into a waste category
                    category = classify_waste(label)
                    
                    # If a valid waste category is found, draw bounding box and label
                    if category:
                        total_classifications[category] += 1
                        detected_categories.add(category)

                        # Draw bounding box
                        class_color = background_colors.get(category, (0, 255, 0))  # Default to green if category not found
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), class_color, 2)

                        # Create label text and calculate text size
                        predicted_class_label = f"{category.capitalize()}"
                        text_size = cv2.getTextSize(predicted_class_label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
                        text_x, text_y = xmin, max(ymin - 10, text_size[1] + 10)

                        # Create a filled rectangle for the text background
                        box_coords = ((text_x, text_y - text_size[1] - 10), (text_x + text_size[0] + 10, text_y + 5))
                        cv2.rectangle(frame, box_coords[0], box_coords[1], class_color, cv2.FILLED)

                        # Put text on the filled rectangle
                        cv2.putText(frame, predicted_class_label, (text_x, text_y), 
                                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

            # Save the processed image with bounding boxes
            processed_filename = f"processed_{filename}"
            processed_image_path = os.path.join(settings.MEDIA_ROOT, processed_filename)
            cv2.imwrite(processed_image_path, frame)

            # Use Django's FileSystemStorage to get the accessible URL
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            processed_file_url = fs.url(processed_filename)

            # Convert the set of detected categories into a readable format for frontend
            categories_detected = ', '.join([category.capitalize() for category in detected_categories])

            # Return response with the file URL and classifications
            return JsonResponse({
                'status': 'file processed successfully',
                'processed_file_url': processed_file_url,  # Return the accessible URL of the processed image
                'classifications': total_classifications,  # Return the total classifications
                'detected_categories': categories_detected  # Return detected categories
            }, status=201)
        
        except Exception as e:
            print(f"Error during capture and classification: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)


# Define background colors for each waste category
background_colors = {
    'ewaste': (255, 153, 153),    # Light red for E-Waste
    'organic': (153, 255, 153),   # Light green for Organic
    'recyclable': (153, 153, 255) # Light blue for Recyclable
}


# Process the frame for live video streaming
def process_frame(frame):
    try:
        results = model(frame)
        detected_objects = results.pandas().xyxy[0]

        for idx, obj in detected_objects.iterrows():
            label = obj['name']
            confidence = obj['confidence']
            if confidence > 0.2:
                category = classify_waste(label)
                if category:
                    box_color = background_colors.get(category, (0, 255, 0))
                    x1, y1, x2, y2 = int(obj['xmin']), int(obj['ymin']), int(obj['xmax']), int(obj['ymax'])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
                    cv2.putText(frame, f'{category}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, box_color, 3)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Error processing frame: {str(e)}")
        return None

# API for live video feed
def video_feed(request):
    cap = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame_with_bounding_boxes = process_frame(frame)
            if frame_with_bounding_boxes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_with_bounding_boxes + b'\r\n\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
