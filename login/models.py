from django.db import models

# Create your models here.


class TempUser(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=200)
    email_reg = models.EmailField(max_length=200)
    category = models.CharField(max_length=50)
    dob = models.DateField()


