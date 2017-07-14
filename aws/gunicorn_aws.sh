#!/bin/bash

exec /usr/local/bin/gunicorn aoranproject.wsgi:application \
--name aoranproject \
--workers 3 \
--timeout 3600 \
--bind=unix:/var/Influencer_Tracking/aoranproject.sock \
--user=root \
--group=root \
--log-level=debug \
--log-file=/var/Influencer_Tracking/logs/debug.log
