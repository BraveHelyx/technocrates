#!/usr/bin/python

from flask import Blueprint, url_for, render_template, request, escape, session, redirect
import db, helpers

signs = Blueprint('signs', __name__, template_folder='templates')

@signs.route('/future_wisdom', methods=['get','post'])
def scholar():
    render_text = []

    # Redirect Unregistered Users
    if helpers.check_unreg():
        return redirect(url_for('io'))

    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

    # Check, set, redirect if dead
    if helpers.check_is_dead(p_entry):
        return redirect(url_for('reaper'))

    time = helpers.calculate_timer(p_entry['p_death_time'])

    if 'lock_scholar' not in session:
        session['lock_scholar'] = 0
    if request.method == 'GET':
            if int(session['lock_scholar']) != 0:
                render_text.append('Before you could ask the man what he meant, \
                    you realised that there was no man to begin with. Just a \
                    machine.')
                response = render_template('profile_POST.html',
                    render_text=render_text,
                    render_time=time)
            else:
                render_text.append('You encounter an old man at the end of his time. He \
                    looks at you with an all knowing smile.')
                render_text.append('"You know, I may not look it...", he begins.')
                render_text.append('"...But I remember what it was like to be young. I  \
                    remember how serious and hopeless those problems looked as well..."')

                render_input = 'submit'

                input_fields = ['continue']
                input_id = 1
                response = render_template('profile_POST.html',
                    render_text=render_text,
                    render_time=time,
                    render_input=render_input,
                    input_id=input_id,
                    input_fields=input_fields)


    elif request.method == 'POST':
        render_text = []

        # Redirect Unregistered Users
        if helpers.check_unreg():
            return redirect(url_for('io'))

        p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

        # Check, set, redirect if dead
        if helpers.check_is_dead(p_entry):
            return redirect(url_for('reaper'))

        time = helpers.calculate_timer(p_entry['p_death_time'])
        input_id = int(request.form['input_id'])

        if input_id >= 0 and input_id < 3:
            if input_id == 1:
                render_text.append('The old man laughs playfully.')
                render_text.append('"Nowadays you young people have such different  \
                    problems. Your problems are whether or not people will like you \
                    and whether or not you can go on living with meaning... I don\'t\
                    envy you."')
                render_text.append('His eyes sparkle.')
                render_text.append('"You should be sceptical of what people think is\
                    best for you. After all, when people tell you things that you are,\
                    you never actually learn anything new about yourself. Of course,\
                    if you weren\'t trying to deceive yourself that you are something\
                    you are not, that would be the case!"')
                render_text.append('He winks at you with a childish grin, "And isn\'t\
                    deceiving ourselves something that we all can bond with in the end?"')

                render_input = 'submit'
                input_id = 2
                input_fields= ['continue']
                response = render_template('profile_POST.html',
                    render_text=render_text,
                    render_time=time,
                    render_input=render_input,
                    input_id=input_id,
                    input_fields=input_fields)
            elif input_id == 2:
                render_text.append('You think to yourself for a moment, wondering what he meant...\
                    Perhaps he is commenting on some sort of perversion of identity...')
                render_text.append('Then you think to yourself that maybe it was a perversion\
                    of identity, and in actual truth you were not thinking to yourself at all.')
                render_text.append('Perhaps what you were thinking of was never yours to\
                    choose at all. Perhaps you were thinking because you were told you\
                    were thinking.')

                session['lock_scholar'] = 1

                response = render_template('profile_POST.html',
                    render_text=render_text,
                    render_time=time)
    return response

