#!/usr/bin/python

from flask import Flask, render_template, request, session, escape, redirect, url_for

cncApp = Flask(__name__)

# Index Route
@cncApp.route('/')
def helloWorld():
    return 'Hello World\n'

# This route is for handling requests to IO
@cncApp.route('/io', methods=['GET', 'POST'])
def io():
    # Handle GET requests
    if request.method == 'GET':
        #Check if user in session
        if 'name' in session:
            response = render_template('welcome.html', name=escape(session['name']), welcome='Welcome to the login page')
        else:   # Else, enlist them.
            response = render_template('enlist.html')
    else: # Handle POST requests
        if request.form['victim'] != "":
            session['name'] = request.form['victim']
        response =  redirect(url_for('io'))
    return response

@cncApp.route('/io')
@cncApp.route('/io/logout', methods=['GET'])
def logout():
    session.pop('name', None)
    return redirect(url_for('io'))

# Sequencing Page (Fibonacci)
@cncApp.route('/seq')
def sequence():
    sequenceImages = [ url_for('static', filename='1.gif')
        , url_for('static', filename='2.gif')
        , url_for('static', filename='3.gif')
        , url_for('static', filename='4.gif')
        , url_for('static', filename='5.gif') ]

    NUM_ELEMENTS = len(sequenceImages)

    if 'seq' in session:    # Return and Iterate Through Seq
        index = session['seq']
        image = sequenceImages[int(index)]
        response = render_template('seq.html', img_url=image)    # Render seq.html template with correct image
        session['seq'] = (session['seq'] + 1) % NUM_ELEMENTS
    else:                   # If first visit
        session['seq'] = 0;
        response = redirect(url_for('sequence'))
    return response

# Page for listing all QR codes in use
@cncApp.route('/code_table')
def codeTable():
    return render_template('qr_table.html')

@cncApp.route('/All_Journeys_Must_Start_Somewhere')
def unregistered():
    return render_template('unregistered.html')

# Page for render IO to users.
@cncApp.route('/profile', methods=['GET', 'POST'])
def userProfile():
    if 'name' in session:   # Registered Users
        if request.method == 'GET':
            user_time = 24
            response = render_template('profile_GET.html', name=escape(session['name']), time=user_time)
        elif request.method == 'POST':
            user_time = 42
            response = render_template('profile_GET.html', name=escape(session['name']), time=user_time)
    else:                   # Unregistered Users
        response = redirect(url_for('io'))
    return response

if __name__ == '__main__':
    cncApp.debug = True
    cncApp.run()
