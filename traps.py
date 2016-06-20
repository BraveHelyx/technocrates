#!/usr/bin/python

from flask import Blueprint, url_for, \
    render_template, request, escape, \
    session, redirect
import db, helpers, datetime


traps = Blueprint('traps', __name__, template_folder='templates')

def can_use(p_entry):
    res = 0
    last_used = p_entry['p_time']
    difference = (datetime.datetime.now() - last_used).total_seconds()
    if difference >= 150: # Wait 2:30 minutes
        res = 1
    return res

def check_num_drinks():
    num_drinks = 0
    # Check and Create num_drinks in session.
    if 'num_drinks' in session:
        num_drinks = int(session['num_drinks'])
    else:
        session['num_drinks'] = 0
    return num_drinks

def check_saved_time():
    saved_time = 0
    # Check and Create num_drinks in session.
    if 'saved_time' in session:
        saved_time = int(session['saved_time'])
    else:
        session['saved_time'] = 0
    return saved_time

def lock_use(p_entry):
    db.insert_db('update players set p_time = ? where p_id = ?',
        [datetime.datetime.now(), int(p_entry['p_id'])])

@traps.route('/font_of_life', methods=['get', 'post'])
def font_of_life():
    render_text = []

    # Redirect Unregistered Users
    if helpers.check_unreg():
        return redirect(url_for('io'))

    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

    # Check, set, redirect if dead
    if helpers.check_is_dead(p_entry):
        return redirect(url_for('reaper'))

    time = helpers.calculate_timer(p_entry['p_death_time'])

    if request.method == 'GET':
        if can_use(p_entry):
            render_text.append('You are working from home on a Monday afternoon when you \
                suddenly receive a call from your best friend. He says that a few   \
                friends of his are getting together to the local pub and invites you\
                to join them.')

            input_command = 'Will you go out?'
            input_fields = ['Go out drinking (Gain 45 seconds)', 'Stay home and work (Gain 30 seconds)']

            response = render_template('profile_POST.html',
                render_text=render_text,
                render_time=time,
                render_input='button',
                input_command=input_command,
                input_fields=input_fields)
        else: # If used recently
            render_text.append('You are at work.')
            render_text.append('Your boss tells you to Quit day dreaming!')
            response = render_template('profile_POST.html',
                render_text=render_text,
                render_time=time)
    elif request.method == 'POST':
        user_input = escape(request.form['input'])
        if user_input == 'Go out drinking (Gain 45 seconds)':
            helpers.add_time(p_entry['p_id'],0,45)
            session['num_drinks'] = check_num_drinks() + 1
            db.insert_db('update players set p_time = ? where p_id = ?',
                (datetime.datetime.now(), session['p_id']))
            # lock_use(p_entry)

        elif user_input == 'Stay home and work (Gain 30 seconds)':
            helpers.add_time(p_entry['p_id'],0,30)
            session['saved_time'] = check_saved_time() + 1
            db.insert_db('update players set p_time = ? where p_id = ?',
                [datetime.datetime.now(), p_entry['p_id']])
            # lock_use(p_entry)
        response = redirect(url_for('traps.font_of_life'))
    return response

