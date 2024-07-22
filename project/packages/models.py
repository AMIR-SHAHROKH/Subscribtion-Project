from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.IntegerField(help_text="Length of the subscription in days")
    description = models.TextField()

    def __str__(self):
        return self.name

