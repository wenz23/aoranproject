from django.db import models


class ContactInfo(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True)
    contact_name    = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    contact_email   = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    contact_type    = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    contact_content = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
