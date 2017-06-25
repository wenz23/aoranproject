from django.db import models
from django.contrib.postgres.fields import JSONField


class StateEnum(object):
    New             = 100
    InQueue         = 110
    Req_Success     = 200
    Req_Failed      = 400
    NotFound        = 404
    Parse_Success   = 600
    Parse_Failed    = 700


class SocialDetails(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True, db_index=True)
    social_id       = models.CharField(max_length=2000, blank=False, null=False, db_index=True)
    url_after_req   = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    source_type     = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    details         = JSONField(blank=True, null=True)
    parse_state     = models.PositiveIntegerField(default=StateEnum.New, db_index=True)
    tags            = JSONField(blank=True, null=True, db_index=True)
