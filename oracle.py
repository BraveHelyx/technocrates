#!/usr/bin/python

from flask import Blueprint, url_for, render_template, request, escape, session, redirect
import db, helpers

# This object is the routing Blueprint that btsite.py imports.
oracle = Blueprint('oracle', __name__, template_folder='templates')

# Bitwise locks for the oracle
ACCESS_LOCK =       0b10000000
VISITED =           0b00000001
HOMELESS_LOCK =     0b00000010
GIRL_LOCK =         0b00000100
GIRL_CAUGHT=        0b01000000
GIRL_TRAP =         0b00100000

# Toggle for debugging output
debug = 1

##
# Get's p_oracle_state from user's db entry
# Returns a dict that can be used in
def oracle_state():
    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)
    oracle_lock = p_entry['p_oracle_state']

    if debug:
        print "Oracle Lock Value: %d" % oracle_lock

    return oracle_lock

def oracle_homeless(p_entry):
    time = helpers.calculate_timer(p_entry['p_death_time'])
    render_text = []

    oracle_state = p_entry['p_oracle_state']

    render_text.append('As you continued walking, you encounter a man sitting   \
        sitting upon a milk crate, wrapped up in a dirty blue sleeping bag.')
    render_text.append('He notices you walk past, lifting his head but not his  \
        his gaze to follow your shoes across the pavement.')
    if oracle_state & GIRL_TRAP:
        render_text.append('He looks as if he wants to say something, but he    \
            says nothing')
    else:
        render_text.append('"Spare a moment of your time?", he asks quietly.')

    # Input fields for the page
    input_fields = ['Continue walking on.','Give the man a moment of your time.']
    response = render_template('profile_POST.html',
        render_media=url_for('static', filename='img/the_homeless_man.jpg'),
        render_time=time,
        render_text=render_text,
        input_fields=input_fields,
        render_input='button',
        input_command='What will you do?')
    return response

def oracle_girl(p_entry):
    time = helpers.calculate_timer(p_entry['p_death_time'])
    render_text = []
    render_text.append('As you were walking down the street, your path becomes \
    obstructed by a high-school girl holding a clip board. From the trim of her blazer, \
    she\'s probably a student attending one of the nearby, private catholic        \
    schools. She makes eye contact with you and smiles.')
    render_text.append('"Excuse me! May I have a little bit of your time for a school survey\
        I\'m conducting for an assignment? It won\'t take very long!"')

    # Fill input parameters
    input_fields=['Continue walking on.', 'Give the girl a moment of your time.']

    response = render_template('profile_POST.html',
        render_time=time,
        render_text=render_text,
        input_fields=input_fields,
        render_input='button',
        input_command='What will you do?')
    return response

def oracle_girl_trap(p_entry):
    time = helpers.calculate_timer(p_entry['p_death_time'])
    render_text = []
    render_text.append('I\'m enlisting signatures for "Locals Against       \
        Homeless", a group formed after the recent decision by the state    \
        to relocate the homeless away from city areas. If the state council \
        gets their way, it could ruin our town\'s prestige. We want to lobby\
        against that decision by having them relocated to another town,     \
        and we will donate a reasonable sum to the shelter.')
    render_text.append('The girl smiles at you, sweetly. "After all... we   \
        only want what\'s best for them. Better a shelter in town over, than\
        a park bench right here, right?"')

    input_command = 'If you could just sign right there...'
    input_fields = ['Sign', 'Dont Sign']
    response = render_template('profile_POST.html',
        render_media=url_for('static', filename='img/the_homeless_man.jpg'),
        render_time=time,
        render_text=render_text,
        render_input='button',
        input_fields=input_fields)
    return response

# Will reward a player for compromising themselves
@oracle.route('/a_moment_of_your_time', methods=['get', 'post'])
def surveyor():
    render_log = []
    render_text = []

    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

    # Check and set if dead
    if helpers.check_is_dead(p_entry):
        if debug:
            print "Player is dead.\n"
        return redirect(url_for('reaper'))

    # Get resource state
    res_state = oracle_state()
    wr_state = res_state

    if request.method == 'GET':
        # Read state if get request
        if res_state & GIRL_LOCK:       # When the Girl has been bypassed
            if res_state & HOMELESS_LOCK: # When the homeless man has finished
                response = redirect(url_for('io'))
            else:
                response = oracle_homeless(p_entry)
        else: # Default / When currently engaged with the Girl
            if res_state & GIRL_CAUGHT:
                response = oracle_girl_trap(p_entry)   # Try to trap them.
            else:
                response = oracle_girl(p_entry)        # Girl Introduces herself
        return response
    else:
        # POST request
        user_input = escape(request.form['input'])

        if (user_input):
            if res_state & GIRL_LOCK: # Girl locked
                if user_input == 'Continue walking on.':
                    wr_state |= HOMELESS_LOCK
                    wr_state |= ACCESS_LOCK
                # elif user_input == 'Give the man a moment of your time.':

                if res_state & HOMELESS_LOCK: # Girl and Homeless man locked
                    return redirect(url_for('io'))
            elif res_state & GIRL_CAUGHT:   # When you give an answer to the girl's trap.
                if user_input == 'Sign':
                    wr_state |= GIRL_TRAP
                    wr_state |= GIRL_LOCK
                elif user_input == 'Dont Sign':
                    wr_state |= GIRL_LOCK
            else: # Default / When currently engaged with the Girl
                if user_input == 'Continue walking on.':
                    wr_state |= GIRL_LOCK   # Bar them from seeing the girl.
                elif user_input == 'Give the girl a moment of your time.':
                    render_log.append('The girl took 30 seconds of your time.')
                    wr_state |= GIRL_CAUGHT # Trap them in the girl.

            # Write the new oracle state
            db.insert_db('update players set p_oracle_state = ? where p_id = ?', (wr_state, session['p_id']))
            response = redirect(url_for('oracle.surveyor'))
        else:
            response = render_template('error.html', errors=['Invalid submission passed with form.'])
        return response

