from django.db import models
from django.contrib.postgres.fields import JSONField


class Gyms(models.Model):
    created_at              = models.DateTimeField(auto_now_add=True, db_index=True)
    revisited_at            = models.DateTimeField(blank=True, null=True, db_index=True)
    gym_name                = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    street_address          = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    city                    = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    zip_code                = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    hours                   = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    holiday                 = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    phone                   = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    gym_url = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    employment = models.CharField(max_length=2000, blank=True, null=True, db_index=True)


