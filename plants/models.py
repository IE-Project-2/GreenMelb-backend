from django.db import models

# Category model
class Category(models.Model):
    category_id = models.AutoField(db_column='CategoryID', primary_key=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        db_table = 'Categories_Plants'  # This matches your table name



class FloweringCategory(models.Model):
    flowering_id = models.AutoField(primary_key=True, db_column='FloweringID')
    flowering = models.CharField(max_length=255)

    def __str__(self):
        return self.flowering

    class Meta:
        db_table = 'FloweringCategories_Plants'


# MaintenanceType model
class MaintenanceType(models.Model):
    maintenance_id = models.AutoField(db_column='MaintenanceID', primary_key=True)
    maintenance = models.CharField(db_column='Maintenance', max_length=10)

    def __str__(self):
        return self.maintenance

    class Meta:
        db_table = 'MaintenanceTypes_Plants'




class Plant(models.Model):
    plant_id = models.AutoField(db_column='PlantID', primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    scientific_name = models.CharField(db_column='ScientificName', max_length=150)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, db_column='CategoryID')
    flowering_category = models.ForeignKey('FloweringCategory', on_delete=models.CASCADE, db_column='FloweringID')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, db_column='LocationID')
    maintenance_type = models.ForeignKey('MaintenanceType', on_delete=models.CASCADE, db_column='MaintenanceID')
    short_description = models.TextField(db_column='ShortDescription', blank=True, null=True)
    watering_frequency = models.CharField(db_column='WateringFrequency', max_length=50, blank=True, null=True)
    watering_schedule = models.TextField(db_column='WateringSchedule', blank=True, null=True)
    soil_type = models.CharField(db_column='SoilType', max_length=255, blank=True, null=True)
    fertilizer_frequency = models.CharField(db_column='FertilizerFrequency', max_length=50, blank=True, null=True)
    photo_url = models.CharField(db_column='PhotoURL', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'PlantsNew'




# Plant Needs model (could also be incorporated into the Plant model)
class PlantNeeds(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, primary_key=True)
    watering_schedule = models.CharField(max_length=255)
    soil_type = models.CharField(max_length=255)
    fertilizer = models.CharField(max_length=255)

    def __str__(self):
        return f"Needs for {self.plant.name}"

    class Meta:
        db_table = 'plants_plant_needs'

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, db_column='LocationID')
    location = models.CharField(max_length=20, db_column='Location')

    def __str__(self):
        return self.location

    class Meta:
        db_table = 'Locations_Plants'
