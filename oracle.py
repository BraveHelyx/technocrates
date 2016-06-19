#!/usr/bin/python

from flask import Blueprint, url_for, render_template, request, escape, session
import db

# This object is the routing Blueprint that btsite.py imports.
oracle = Blueprint('oracle', __name__, template_folder='templates')

# Bitwise locks for the oracle
access_lock =       0b10000000
visited =           0b00000001
homeless_lock =     0b00000010
girl_lock =         0b00000100

##
# Get's p_oracle_state from user's db entry
# Returns a dict that can be used in
def oracle_state(oracle_lock):
    oracle_state = {
        'access_locked':oracle_lock & access_lock,
        'visited':oracle_lock & visited,
        'girl_locked':oracle_lock & girl_lock,
        'homeless_locked':oracle_lock & homeless_lock
        }
    return oracle_state

def oracle_homeless():
    render_text = []

    render_text.append('As you continued walking, you encounter a man sitting   \
        sitting upon a milk crate, wrapped up in a dirty blue sleeping bag.')

    render_text.append('He notices you walk past, lifting his head but not his \
        his gaze to follow your shoes across the pavement.')
    render_text.append('"Spare a moment of your time?", he asks quietly.')

    # Input fields for the page
    input_fields = ['Continue walking on.','Give the man a moment of your time.']
    response = render_template('profile_POST.html',
        render_media=url_for('static', filename='img/the_homeless_man.jpg'),
        render_text=render_text,
        input_fields=input_fields,
        render_input='button',
        input_command='What will you do?')
    return response

def oracle_girl():
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
        render_text=render_text,
        input_fields=input_fields,
        render_input='button',
        input_command='What will you do?')
    return response

# Will reward a player for compromising themselves
@oracle.route('/a_moment_of_your_time', methods=['get', 'post'])
def surveyor():
    response = ''
    render_text = []
    user = db.query_db('select * from players where p_name = ?', [session['p_name']], one=True)

    # Get resource state
    res_state = oracle_state(0)

    if (request.method == 'GET'):
        response = oracle_girl()
    else:
        # POST request
        user_input = escape(request.form['input'])
        if (user_input):

            if user_input == 'Continue walking on.':
                response = oracle_homeless()

            elif user_input == 'Give the girl a moment of your time.':

                render_text.append('You gave the girl some time.')

                response = render_template('profile_POST.html',
                render_media=url_for('static', filename='img/the_homeless_man.jpg'),
                render_text=render_text)
        else:
            response = render_template('error.html', errors=['Invalid submission passed with form.'])
    return response
