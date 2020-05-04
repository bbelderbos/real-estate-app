from django.db import models


class PropertyForRent(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    source_site = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    added_on = models.DateTimeField(blank=True, null=True)
    price = models.IntegerField()
    rooms = models.IntegerField(blank=True, null=True)
    living_area = models.FloatField(blank=True, null=True)
    url = models.CharField(max_length=255)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)
    private_offer = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.rooms} rooms in {self.address}"
