# predictions/serializers.py

from rest_framework import serializers

class WastePredictionInputSerializer(serializers.Serializer):
    household_size = serializers.IntegerField()
    recycling_habits = serializers.ChoiceField(choices=[('Rarely', 'Rarely'), ('Occasionally', 'Occasionally'), ('Regularly', 'Regularly')])
    compost = serializers.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    large_item_disposal = serializers.ChoiceField(choices=[('Never', 'Never'), ('Occasionally', 'Occasionally'), ('Once a year', 'Once a year')])
