from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.


class Pesticides(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    display = models.TextField()
    price = models.TextField()
    image = models.FileField(upload_to='media/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])],)
    
    def __str__(self):
        return self.name