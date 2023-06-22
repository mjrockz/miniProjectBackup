from django.db import models

# Create your models here.
class Certificate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.CharField(max_length=100)
    file = models.ImageField(upload_to="images/", blank=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner}"

