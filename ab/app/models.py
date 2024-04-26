from django.db import models

# Create your models here.

class UserData(models.Model):
    name=models.TextField(max_length=50)
    email=models.EmailField(blank=False)
    password=models.TextField(blank=False,max_length=250)
    cartItems=models.JSONField(default={})

    class Meta:
        db_table='Users'

class Products(models.Model):
    name=models.TextField(max_length=50)
    description=models.TextField(max_length=120)
    price=models.IntegerField()
    pImage=models.ImageField(upload_to='images')
    
