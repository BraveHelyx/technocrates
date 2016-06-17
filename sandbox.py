#!/usr/bin/python

from flask import Flask,                \
    render_template, request, session,  \
    escape, redirect, url_for,          \
    g
import random, datetime, sqlite3
from contextlib import closing

random.seed('0xdeadbeef')

# Database Config
DEBUG = True
SECRET_KEY = 'super_secret_key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/oracles')