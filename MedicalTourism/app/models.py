from django.db import models

# Create your models here.
class Patient(models.Model):
    p_id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=500)

    def __str__ (self):
        return str(self.p_id) + '. ' + str(self.name)

class Disease(models.Model):
    id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=100)
    kg_id = models.CharField(max_length=100)

    def __str__ (self):
        return str(self.kg_id) + '. ' + str(self.disease_name)


class Temp_info_1(models.Model):
    city = models.CharField(max_length=100, default = '')
    distance = models.CharField(max_length=100, default = '')
    time = models.CharField(max_length=100, default = '')
    
    def __str__ (self):
        return str(self.city)


class Temp_info(models.Model):
    city_info = models.CharField(max_length=100, default = '')
    price_info = models.CharField(max_length=100, default = '')
    
    def __str__ (self):
        return str(self.city_info)