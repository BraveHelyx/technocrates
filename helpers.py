#!/usr/bin/python

import datetime, db

def calculate_timer(p_time):
    return (p_time - datetime.datetime.now()).total_seconds()
