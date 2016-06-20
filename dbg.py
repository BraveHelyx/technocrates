#!/usr/bin/python

from flask import Blueprint, url_for, render_template, request, escape, session, redirect
import db, helpers

dbg = Blueprint('dbg', __name__, template_folder='templates')

@dbg.route('/dbg/time_arithmetic', methods=['GET', 'POST'])
def test_time():
    p_entry = db.query_db('select * from players where p_id = ?', [int(session['p_id'])], one=True)

    if request.method == 'GET':
        response = render_template('debugger.html', render_time=helpers.calculate_timer(p_entry['p_death_time']))
    elif request.method == 'POST':

        # print 'add_min=%d\nadd_sec=%d\n\nrm_min=%d\nrm_sec=%d' % (request.form['add_min'],
        #     request.form['add_sec'],
        #     request.form['rm_min'],
        #     request.form['rm_sec'])

        if request.form['add_min'] or request.form['add_sec']:
            minutes = request.form['add_min']
            seconds = request.form['add_sec']
            helpers.add_time(p_entry['p_id'], minutes, seconds)
        # elif request.form['submit'] == 'RM_TIME':
        #     minutes = request.form['rm_min']
        #     seconds = request.form['rm_sec']
        #     helpers.rm_time(p_entry['p_id'], int(minutes), int(seconds))
        response = redirect(url_for('dbg.test_time'))
    return response
