#!/bin/bash

exec /usr/local/bin/gunicorn aoranproject.wsgi:application \
--name aoranproject \
--workers 3 \
--timeout 3600 \
--bind=unix:/var/aoranproject/aoranproject.sock \
--user=root \
--group=root \
--log-level=debug \
--log-file=/var/aoranproject/logs/debug.log
