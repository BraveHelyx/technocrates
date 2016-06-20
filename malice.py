#!/usr/bin/python

from flask import Blueprint, url_for, render_template, request, escape, session, redirect
import db, helpers

malice = Blueprint('malice', __name__, template_folder='templates')

@malice.route('/life_or_time', methods=['GET','POST'])
def thief():
    render_text = []

    # Redirect unregistered users
    if 'p_id' not in session:
        return redirect(url_for('io'))

    # Query player entry
    p_entry = db.query_db('select * from players where p_id = ?',
        [int(session['p_id'])], one=True)

    # Check, set, redirect if dead
    if helpers.check_is_dead(p_entry):
        if debug:
            print "Player is dead.\n"
        return redirect(url_for('reaper'))

    if request.method == 'GET':
        render_text.append('Before you even realise what is going on, you are   \
            ambushed by a masked man with a knife. He is far too strong for you,\
            pinning you against a wall with the blade pressed to your neck. You \
            can feel the edge against your jungular as you try not to move. You \
            make eye contact with the man, and he stares  deep, cold, green     \
            eyes that reveal indifference.')

        render_text.append('"Your money, or your time. Your call."')

        
    elif request.method == 'POST':


