from django.db import models
from django.contrib.postgres.fields import JSONField


class StateEnum(object):
    New             = 100
    Req_Success     = 200
    Req_Failed      = 400
    Parse_Success   = 600
    Parse_Failed    = 700
    Standby         = 500
    User_Not_Exist  = 404
    Other_Error     = 405


class InstagramMap(models.Model):
    created_at              = models.DateTimeField(auto_now_add=True, db_index=True)
    ins_id                  = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    latest_crawl_at         = models.DateTimeField(blank=True, null=True, db_index=True)
    latest_crawl_state      = models.PositiveIntegerField(default=StateEnum.New, blank=False, null=False, db_index=True)
    latest_similar_at       = models.DateTimeField(blank=True, null=True, db_index=True)
    latest_follower_count   = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    latest_username         = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_find_similar        = models.BooleanField(default=False, db_index=True)
    ins_tags                = JSONField(default=dict, blank=True, null=True, db_index=True)
    ins_growth              = JSONField(default=dict, blank=True, null=True, db_index=True)
    ins_growth_meta         = JSONField(default=dict, blank=True, null=True)
    project_info            = JSONField(default=dict, blank=True, null=True)


class InstagramTracking(models.Model):
    created_at              = models.DateTimeField(auto_now_add=True, db_index=True)
    profile_url             = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_username            = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_fullname            = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_id                  = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_follower_count      = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_following_count     = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_media_count         = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    ins_biography           = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_external_url        = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_recent_12_meta      = JSONField(default=dict, blank=True, null=True)
    ins_verified            = models.BooleanField(default=False, db_index=True)
    ins_private             = models.BooleanField(default=False, db_index=True)
    ins_json                = JSONField(default=dict, blank=True, null=True)


