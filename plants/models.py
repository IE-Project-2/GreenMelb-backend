from django.db import models

class Plant(models.Model):
    plant_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    flowering_category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    maintenance_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.URLField(max_length=255)
    watering_needs = models.CharField(max_length=255)
    sunlight_needs = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Plants'  # Custom table name in the database

class Plant_Needs(models.Model):
    need_id = models.IntegerField(primary_key=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)  # ForeignKey to the Plant model
    watering_schedule = models.CharField(max_length=255)
    soil_type = models.CharField(max_length=255)
    fertilizer = models.CharField(max_length=255)

    def __str__(self):
        return f"Needs for {self.plant.name}"

    class Meta:
        db_table = 'Plant_Needs'  # Custom table name in the database
