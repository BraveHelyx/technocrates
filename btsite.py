#!/usr/bin/python

from flask import Flask,                \
    render_template, request, session,  \
    escape, redirect, url_for,          \
    g
import random, datetime, sqlite3
from contextlib import closing
from oracle import oracle

random.seed('0xdeadbeef')

# Database Config
USER_DB = './tmp/users.db'
DEBUG = True
SECRET_KEY = 'super_secret_key'

cncApp = Flask(__name__)
cncApp.config.from_object(__name__)
cncApp.register_blueprint(oracle)

#####################
# Application Views #
#####################
# Index Route
@cncApp.route('/')
def helloWorld():
    return 'Hello World\n'

# This route is for handling requests to the gate keeper
@cncApp.route('/technocrates', methods=['GET', 'POST'])
def io():
    # Handle GET requests
    if request.method == 'GET':
        #Check if user in session
        if 'p_id' in session:
            # Query Database Object with client's cookie name
            p_entry = query_db('select * from players where p_id = ?', [session['p_id']], one=True)

            # Check client entry name
            if p_entry['p_name'] is not None:
                time = calculate_timer()
                response = render_template('user_output.html', render_media=url_for('static', filename='img/qr/qr_io.png'), render_time=time)
            else:
                response = render_template('error.html', errors=['p_entry returned none but session["p_name"] supplied.', [session['p_name']]])
        else:   # Else, enlist them.
            response = render_template('enlist.html')
    else: # Handle POST requests
        p_name = escape(request.form['victim']) # Set User's Name
        p_time = datetime.datetime.now() + datetime.timedelta(minutes=15) # Give user 15 minutes

        # Check for legitimacy of input
        if p_name != "":
            p_ID = add_new_player(p_name, p_time) # Add to player database
            print 'p_ID of New Player: %d' % p_ID
            #Set User Cookies
            session['p_id'] = p_ID      # Index in DB Entry
            session['p_name'] = p_name    # Sanitized Player Name
            response =  redirect(url_for('io'))
        else:
            response = render_template('error.html', errors=['p_name is invalid. No length.', p_name])
    return response

@cncApp.route('/logout', methods=['GET'])
def logout():
    session.pop('p_id', None)
    session.pop('p_name', None)
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

# Route for Unregistered Strangers
@cncApp.route('/talking_with_strangers')
def unregistered():
    message = ["You approach me, expecting something for nothing... Are you surprised you got nothing for something? Speak to Zeus",
        "Just because you knock on a door does not imply it will open of its own accord... Speak to Zeus.",
        "Even though you are willing, I may never be... Not without the master's word.",
        "I am but a mere minister, who shall speak not without their master's permission. Please see my master in the main entry, he will till you more.",
        "Enthusiastic, I see. Motivated by curiosity, adverse to the obvious? Please see my master, at the entrance and we may converse."]
    index = random.randrange(0, len(message))
    return render_template('unregistered.html', message=message[index])

# Page for render IO to users.
@cncApp.route('/profile', methods=['GET', 'POST'])
def userProfile():
    if 'p_name' in session:   # Registered Users
        if request.method == 'GET':
            user_time = 24
            response = render_template('profile_GET.html', name=escape(session['p_name']), time=user_time)
        elif request.method == 'POST':
            user_time = 42
            response = render_template('profile_GET.html', name=escape(session['name']), time=user_time)
    else:                   # Unregistered Users
        response = redirect(url_for('unregistered'))
    return response

####
# DEBUG ROUTES
##############
@cncApp.route('/dbentries', methods=['GET'])
def show_db_entries():
    db = query_db('select * from players')
    return render_template('dbentries.html', entries=db)

@cncApp.route('/scoreboard', methods=['GET'])
def scoreboard():
    db = query_db('select * from players where p_is_alive = 1')
    return render_template('dbentries.html', entries=db)

####
# DATABASE FUNCTIONS
####################
def connect_db():
    return sqlite3.connect(cncApp.config['USER_DB'], detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

# Make connection (if necessary) and get db and
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
        db.row_factory = sqlite3.Row    # Make dict from results
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with closing(connect_db()) as db:
        with cncApp.open_resource('userSchema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@cncApp.before_request
def before_request():
    g.db = connect_db()

@cncApp.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

##
# HELPER FUNCTIONS
##################
def add_new_player(p_name, p_time):
    death_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
    g.db.execute('insert into players (p_name, p_time, p_status, p_is_alive, p_birth_time, p_death_time, p_oracle_state) values (?, ?, -1, 1, ?, ?, 0)', \
        (p_name, p_time, p_time, death_time))
    g.db.commit()
    p_ID = g.db.cursor().lastrowid
    return p_ID

def calculate_timer():
    if 'p_id' in session:
        p_time = query_db('select p_time from players where pid = ?', session['p_id'])
        # (deadline time - current time in seconds)
        return (p_time - datetime.datetime.now()).total_seconds()


if __name__ == '__main__':
    cncApp.run()
