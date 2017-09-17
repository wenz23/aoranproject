from django.shortcuts import render


class InstagramMap(models.Model):
    created_at              = models.DateTimeField(auto_now_add=True, db_index=True)
    ins_id                  = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    latest_crawl_at         = models.DateTimeField(blank=True, null=True, db_index=True)
    latest_crawl_state      = models.PositiveIntegerField(default=StateEnum.New, blank=False, null=False, db_index=True)
    latest_similar_at       = models.DateTimeField(blank=True, null=True, db_index=True)
    latest_follower_count   = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    latest_username         = models.CharField(max_length=2000, blank=True, null=True, db_index=True)
    ins_find_similar        = models.BooleanField(default=False, db_index=True)
    ins_tags                = JSONField(blank=True, null=True, db_index=True)
    ins_growth              = JSONField(blank=True, null=True, db_index=True)
    ins_growth_meta         = JSONField(blank=True, null=True)
