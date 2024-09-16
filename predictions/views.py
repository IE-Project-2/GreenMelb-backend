from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pickle
from .serializers import WastePredictionInputSerializer

# Load the pre-trained model (path to your model)
model = pickle.load(open('backend/models/waste_prediction_model.pkl', 'rb'))

def estimate_waste(data):
    # Base estimates for different waste categories (kg per household)
    waste_estimates = {
        'public_litter_bins': 5,
        'dumped_rubbish': 2,
        'street_sweepings': 3,
        'mattresses': 0,
        'commingled_recycling': 4,
        'cardboard': 1.5,
        'hardwaste_to_landfill': 5,
        'hardwaste_recovered': 1,
        'green_waste': 2.5
    }

    # Scale based on household size
    household_size = data['household_size']
    for key in waste_estimates:
        waste_estimates[key] *= household_size / 2.5  # Adjust based on average household size

    # Adjust for recycling habits
    if data['recycling_habits'] == 'Rarely':
        waste_estimates['commingled_recycling'] *= 0.5
    elif data['recycling_habits'] == 'Regularly':
        waste_estimates['commingled_recycling'] *= 1.5

    # Adjust for composting
    if data['compost'] == 'Yes':
        waste_estimates['green_waste'] *= 0.7

    # Adjust for large item disposal (e.g., mattresses)
    if data['large_item_disposal'] == 'Once a year':
        waste_estimates['mattresses'] = 5
    elif data['large_item_disposal'] == 'Occasionally':
        waste_estimates['mattresses'] = 10

    # Return the waste estimates (by category)
    return waste_estimates

class WastePredictionView(APIView):
    def post(self, request):
        # Deserialize the input
        serializer = WastePredictionInputSerializer(data=request.data)
        if serializer.is_valid():
            # Get waste estimates for the user input
            user_input = serializer.validated_data
            waste_data = estimate_waste(user_input)
            
            return Response({'predicted_waste': waste_data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
