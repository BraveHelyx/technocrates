#!/usr/bin/python

from flask import session
import datetime, db
import json

def calculate_timer(p_time):
    return (p_time - datetime.datetime.now()).total_seconds()

# Function to return a 1 if player is dead, or 0 if alive
# If dead, updates the registry
def check_is_dead(p_entry):
    ret = 0
    if p_entry['p_is_alive'] != 0:
        if (p_entry['p_death_time'] - datetime.datetime.now()).total_seconds() <= 0:  #Recently Died
            db.insert_db('update players set p_is_alive = 0 where p_id = ?', [int(p_entry['p_id'])])
            ret = 1
    else:
        ret = 1
    return ret

# Function for adding positive time to player deadline
def add_time(p_id, minutes, seconds):
    print "ADD TIME ENTERED"
    err = 1
    p_entry = db.query_db('select * from players where p_id = ?', [p_id], one=True)

    # Will transact and return 0 if player is not dead
    if not check_is_dead(p_entry):
        p_deadline = p_entry['p_death_time']
        p_deadline += datetime.timedelta(minutes=int(minutes), seconds=int(seconds))
        db.insert_db('update players set p_death_time = ? where p_id = ?',
            [p_deadline, p_id])
        err = 0
    return err

# Function to remove time from a player.
# Knows if player is dead on execution
# If offset kills player, will set player to dead
# Returns a 1 if player is dead, and a zero otherwise.
def rm_time(p_id, minutes, seconds):
    err = 0
    p_entry = db.query_db('select * from players where p_id = ?', [p_id], one=True)

    # Don't do anything for already dead players
    if not check_is_dead(p_entry):
        p_deadline = p_entry['p_death_time']
        timeleft = p_deadline - datetime.datetime.now()
        # If result kills player, death time is current time.
        if (timeleft - datetime.timedelta(minutes=minutes, seconds=seconds)).total_seconds() <= 0:
            db.insert_db('update players set p_is_alive = 0, p_death_time = ? where p_id = ?',
                [datetime.datetime.now(), p_id])
            err = 1
        else:
            # Player remains alive after time offset, apply it.
            new_time = p_deadline - datetime.timedelta(minutes=minutes, seconds=seconds)
            db.insert_db('update players set p_death_time = ? where p_id = ?',
                [new_time, p_id])
    else: # Otherwise, player is already dead.
        err = 1
    return err

# Append to a user's log
def append_to_full_log(p_id, log_entry):
    p_entry = db.query_db('select * from players where p_id = ?', [p_id], one=True)
    logs = json.load(p_entry['p_full_log'])
    logs.append(log_entry)
    write_to_full_log(p_id, logs)

def write_to_full_log(p_id, new_log):
    db.insert_db('update players set p_full_log = ? where p_id = ?', [json.dump(new_log), p_id])

def get_log(p_id):
    p_entry = db.query_db('select * from players where p_id = ?', [p_id], one=True)
    return json.load(p_entry['p_full_log'])

# Checks to see if the user is unregistered.
def check_unreg():
    err = 1;
    if 'p_id' in session:
        err = 0
    return err