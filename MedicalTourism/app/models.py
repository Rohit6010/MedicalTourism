from django.db import models

# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=500)

    def __str__ (self):
        return str(self.id) + '. ' + str(self.name)

class Disease(models.Model):
    id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=100)
    kg_id = models.CharField(max_length=100)

    def __str__ (self):
        return str(self.kg_id) + '. ' + str(self.disease_name)

