from django.db import models


class ContactInfo(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True)
    contact_name    = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    contact_email   = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    contact_content = models.CharField(max_length=2000, blank=True, null=True, db_index=True)

    contact_is_partner = models.BooleanField(default=False, db_index=True)
    contact_is_detail = models.BooleanField(default=False, db_index=True)
    contact_is_product = models.BooleanField(default=False, db_index=True)
