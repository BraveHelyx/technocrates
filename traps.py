#!/usr/bin/python

from flask import Blueprint, url_for, \
    render_template, request, escape, \
    session, redirect
import db, helpers, datetime
from random import randrange

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
        [datetime.datetime.now(), p_entry['p_id']])

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
            lock_use(p_entry)

        elif user_input == 'Stay home and work (Gain 30 seconds)':
            helpers.add_time(p_entry['p_id'],0,30)
            session['saved_time'] = check_saved_time() + 1
            lock_use(p_entry)
        response = redirect(url_for('traps.font_of_life'))
    return response

def gambler_get(timer):
    render_text = []
    time = timer
    render_text.append('Feelin\' lucky, friend? Why not try your hand at my     \
        game? Each card has can be one of three. I\'ll make it worthwhile       \
        for you! If you win, I\'ll give you over 10 times your bet in return!   \
        I\'ll even sweeten the deal for you, give you the first game free!')

    render_text.append('"Whattya say?"')
    render_input = 'submit'
    input_command = 'How bout it? Spend some time?'
    if int(session['num_gambles']) == 0:
        input_fields = ['Accept (Free)']
    else:
        input_fields = ['Accept (5s)']

    return render_template('gambler.html',
        render_time = time,
        render_text = render_text,
        render_input = render_input,
        input_command = input_command,
        input_fields = input_fields)

def gambler_post():
    render_text = []
    render_media = []
    cardImages = [ url_for('static', filename='img/1.jpg')
        , url_for('static', filename='img/2.jpg')
        , url_for('static', filename='img/3.jpg') ]

    # render_media.append(cardImages[range(0, 3)])

    if 'num_gambles' not in session:
        session['num_gambles'] = 0

    num_gambles = session['num_gambles']
    if num_gambles == 0:
        # Fix the win
        card1 = cardImages[randrange(0, 3)]

        render_media.append(card1)
        render_media.append(card1)
        render_media.append(card1)

        helpers.add_time(session['p_id'], 1, 0)
        p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)
        time = helpers.calculate_timer(p_entry['p_death_time'])
        render_log = 'You gained 1 minute from gambling'
        render_text.append('Wowee! What are the odds?! Look at you! Turning         \
            seconds into minutes! Bravo!')
        render_text.append('You keep this up and you might put me out of business!  \
            Haha!')
        render_text.append('Fancy another hand?')

        render_input = 'submit'
        input_command = 'How bout it? Spend some time?'
        input_fields = ['Accept (5s)']

        response = render_template('gambler.html',
            render_media = render_media,
            render_time = time,
            render_log = render_log,
            render_text = render_text,
            render_input = render_input,
            input_command = input_command,
            input_fields = input_fields)
    else:
        card1 = randrange(0, 3)
        card2 = randrange(0, 3)
        card3 = randrange(0, 3)

        # Bias to always lose. :)
        if (card1 == card2) and (card2 == card3):
            card3 = (card3 + 1) % 3

        render_media.append(cardImages[card1])
        render_media.append(cardImages[card2])
        render_media.append(cardImages[card3])

        # Rm and kill player
        if helpers.rm_time(session['p_id'], 0, 5):
            return redirect(url_for('reaper'))

        p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)
        time = helpers.calculate_timer(p_entry['p_death_time'])
        render_text.append('Ah, rough! Lady luck was on my side, this time! At  \
            least it\'s not like you bet very much though... Another hand?')

        render_input = 'submit'
        input_command = 'How bout it? Spend some time?'
        input_fields = ['Accept (5s)']

        response = render_template('gambler.html',
            render_media = render_media,
            render_time = time,
            render_text = render_text,
            render_input = render_input,
            input_command = input_command,
            input_fields = input_fields)
    session['num_gambles'] = num_gambles + 1
    return response

@traps.route('/professional_gaming', methods=['get','post'])
def gamble():
    # Redirect Unregistered Users
    if helpers.check_unreg():
        return redirect(url_for('io'))

    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

    # Check, set, redirect if dead
    if helpers.check_is_dead(p_entry):
        return redirect(url_for('reaper'))

    time = helpers.calculate_timer(p_entry['p_death_time'])

    if request.method == 'GET':
        response = gambler_get(time)
    elif request.method == 'POST':
        response = gambler_post()
    return response

@traps.route('/strange_interactions_with_strangers', methods=['get'])
def strangers():
    route = randrange(0, 3)
    render_text = []

    render_text.append('Not knowing the consequences of trusting others who advise  \
        you, you find that you are suddenly in a situation alone with this person.')

    randrange
    rand = randrange(0, 2)
    messages = ['They hold you up at knife point, and offer time or blood. You  \
        cannot refuse...',
        'You are standing at the aisle of staring this person in the eyes, mere \
        seconds before you vow to be married through life and death, sickness and\
        health.']

    render_text.append(messages[rand])

    log = ['You lose 2 minutes of time.','You lose 1 minute of time']
    render_log = log[rand]


