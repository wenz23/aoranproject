from django.db import models
import jsonfield


class StateEnum(object):
    New         = 100
    InQueue     = 110
    Success     = 200
    NotFound    = 404
    Error       = 600


class URLDetails(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True)
    revisited_at    = models.DateTimeField(blank=True, null=True, db_index=True)
    url             = models.CharField(max_length=2000, blank=False, null=False, db_index=True)
    details         = jsonfield.JSONField(blank=True, null=True, db_index=True)
    parse_state     = models.PositiveIntegerField(default=StateEnum.New, db_index=True)
