from django.db import models

class Starship(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    passengers = models.CharField(max_length=255)
    cargo_capacity = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name