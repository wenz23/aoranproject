#!/bin/sh
# This is a comment!
echo Reset gunicorn	# This is a comment, too!
PID=`ps -ef | grep python | grep -v "grep" | awk '{print $2}'`
echo $PID
kill -9 $PID
. /var/Influencer_Tracking/gunicorn_aws.sh &>/dev/null &
service nginx restart
