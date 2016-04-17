#!/bin/bash

# btenv/bin/gunicorn --workers 3 --bind unix:/tmp/btsite.sock -m 007 wsg
btenv/bin/gunicorn --workers 3 --bind unix:/tmp/btsite.sock -m 007 --error-logfile tmp/gunicorn_error_log.txt --access-logfile tmp/gunicorn_access_log.txt wsgi:cncApp &
