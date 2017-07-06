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
    created_at          = models.DateTimeField(auto_now_add=True, db_index=True)
    social_id           = models.CharField(max_length=2000, blank=False, null=False, db_index=True)
    url_after_req       = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    source_type         = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    details             = JSONField(blank=True, null=True)
    parse_state         = models.PositiveIntegerField(default=StateEnum.New, db_index=True)
    tags                = JSONField(blank=True, null=True, db_index=True)


class SocialTracking(models.Model):

    # General
    created_at          = models.DateTimeField(auto_now_add=True, db_index=True)
    social_media_type   = models.CharField(max_length=20, blank=False, null=False, db_index=True)
    tags                = JSONField(blank=True, null=True, db_index=True)
    url                 = models.CharField(max_length=2000, blank=True, null=True, db_index=True)

    # Instagram
    ins_fullname        = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_id              = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_follower_count  = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_following_count = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_post_count      = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_biography       = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_external_url    = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_recent_12_meta  = JSONField(blank=True, null=True, db_index=True)
    ins_json            = JSONField(blank=True, null=True, db_index=True)

    # YouTube
    ytb_username        = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ytb_subscribers     = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ytb_views           = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ytb_description     = models.CharField(max_length=3000, blank=True, null=True, db_index=True)
    ytb_business        = models.BooleanField(default=False, db_index=True)
    ytb_country         = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ytb_related_links   = JSONField(blank=True, null=True, db_index=True)
