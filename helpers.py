#!/usr/bin/python

import datetime, db

def calculate_timer(p_time):
    return (p_time - datetime.datetime.now()).total_seconds()

# Function to return a 1 if player is dead, or 0 if alive
# If dead, updates the registry
def check_is_dead(p_entry):
    ret = 0
    if p_entry['p_is_alive'] != 1:
        if (p_entry['p_death_time'] - datetime.datetime.now()).total_seconds() <= 0:  #Recently Died
            db.insert_db('update players set p_is_alive = 0 where p_id = ?', [int(p_entry['p_id'])])
            ret = 1
    return ret
