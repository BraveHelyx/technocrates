#!/usr/bin/python

from flask import Flask, render_template, request, session, escape, redirect, url_for

cncApp = Flask(__name__)

def loadHeader(css):
    return render_template('header.html', css_resource=css)

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
        if 'victim' in session:
            pageHTML = render_template('welcome.html', name=escape(session['victim']), welcome='Welcome to the login page')
        else:   # Else, enlist them.
            pageHTML = render_template('enlist.html')
    else: # Handle POST requests
        if request.form['victim'] != "":
            session['victim'] = request.form['victim']
        pageHTML =  redirect(url_for('io'))
    return pageHTML

@cncApp.route('/io')
@cncApp.route('/io/logout', methods=['GET'])
def logout():
    session.pop('victim', None)
    return redirect(url_for('io'))

# Sequencing Page (Fibonacci)
@cncApp.route('/seq')
def sequence():
    returnHTML = ""
    sequenceImages = [ url_for('static', filename='1.gif')
        , url_for('static', filename='2.gif')
        , url_for('static', filename='3.gif')
        , url_for('static', filename='4.gif')
        , url_for('static', filename='5.gif') ]

    # returnHTML += "<p>"
    # returnHTML += str(sequenceImages) + '\n'
    NUM_ELEMENTS = len(sequenceImages)
    # returnHTML += str(NUM_ELEMENTS) + '\n'
    # returnHTML += "</p>"

    if 'seq' in session:
        index = session['seq']
        image = sequenceImages[int(index)]
        returnHTML += str(index)                                    # Grab index for debugging
        returnHTML += render_template('seq.html', img_url=image)    # Render seq.html template with correct image
        session['seq'] = (session['seq'] + 1) % NUM_ELEMENTS
    else:
        session['seq'] = 0;
        return redirect(url_for('sequence'))

    return returnHTML

# Page for listing all QR codes in use
@cncApp.route('/code_table')
def codeTable():
    return render_template('qr_table.html')

@cncApp.route('/All_Journeys_Must_Start_Somewhere')
def unregistered():
    return render_template('unregistered.html')

if __name__ == '__main__':
    cncApp.debug = True
    cncApp.run(host='0.0.0.0')
