from flask import Flask, flash, render_template, request, redirect, url_for, session, Response, flash, jsonify, json
import os

from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import hashlib
import flask
from flask_mysqldb import MySQL
import array as arr
import os
# import mysql.connector
# from mysql import connector
from werkzeug.utils import secure_filename
import pandas as pd
import collections
import html
import base64
from bs4 import BeautifulSoup
# csv export
import io
import csv

# mail


## mail sender
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

UPLOAD_FOLDER = r'app/static/uploads/pdf'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg'}
app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config["IMG_FOLDER"] = "/root_flask_app/static/img/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
updir = app.config["IMG_FOLDER"]
app.url_map.strict_slashes = False
app.secret_key = 'your secret key'

# app.config['MYSQL_HOST'] = '10.30.10.41'
# app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_USER'] = 'cloud'
# app.config['MYSQL_PASSWORD'] = 'cloud@123'
# app.config['MYSQL_DB'] = 'school_management'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fleet-management'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select count(*) as vehicle from trip_entry")
    vehicle_count=cursor.fetchall()
    vehicle_count=vehicle_count[0]['vehicle']
    print(vehicle_count)
    return render_template('index.html',vehicle_count=vehicle_count)


from app.code import fuel_entry, issue_entry, trip_entry
