from flask import Flask, render_template, request
import json

# Supported characters for usernames
import string
ACC = string.ascii_letters + string.digits + "-_"
# No-no words!
CURSE_WORDS = ['fuck','bitch','cunt','shit','nigger','asshole','faggot','gay','fag']

# pyMongodb wrapper
from kyzr_db import dbEditor
kyzr = dbEditor()

# Setup flask
app = Flask(__name__)

# Main homepage
@app.route('/')
def index():
    return render_template('index.html')

# Page for about_Kyzr
@app.route('/class_notes')
def notes():
    return render_template('class_notes.html')

# Map page
@app.route('/maps', methods=['GET', 'POST'])
def maps():
    # A bunch of prototypes so things don't break
    coords = []
    center = [0,0]
    zoom = 3
    torchID = ''
    error = False
    dist = ''
    username = '' 
    num_tran = '' 
    torch = ''

    # If a username is entered
    if(request.method=="POST"):
        if("id" in request.form.keys()):
            torchID = request.form["id"]

            if(torchID):
                user = kyzr.find_user(torchID)
                if(user is not None):
                    coords = user['locs']
                else:
                    error = True

    # If that username is found in the db
    if coords:
        lats = [ coords[j][0] for j in xrange(len(coords))]
        lons = [ coords[j][1] for j in xrange(len(coords))]
        center = [ float(sum(i)/len(i)) for i in (lats, lons) ]
        zoom = max( [ max(lats) - min(lats), max(lons)-min(lons)])
        for i in xrange(0,15,2):
            if zoom < 0.005:
                zoom = 15-i
                break
            zoom = zoom/7.0
        stats = kyzr.compute_stats(torchID)
        dist = stats['DISTANCE']
        torcher = stats['CURRENTOWNER']
        num_tran = stats['NUMTRANSACTION']
        torch = stats['TORCH']


    return render_template('maps.html',
           coords=json.dumps(coords),
           center=json.dumps(center),
           zoom=json.dumps(zoom),
           torchID=torchID,
           dist=dist,
           torch_holding=torch,
           torch_held=torcher,
           num_tran=num_tran,
           error=error)

# Used by Android app to see if username is
# taken or not, and whether the username is
# valid
@app.route('/verify', methods=['GET', 'POST'])
def verify():

    if request.method=="POST":
        if ("search_id" in request.form.keys()):

            # Check to make sure all characters in requested
            # username check are allowed
            for i in request.form["search_id"]:
                if i not in ACC:
                    return "Not valid characters"
            for i in CURSE_WORDS:
                if i in request.form["search_id"]:
                    return "Naughty word!"

            # TODO: Implement length checking Android side
            # This breaks because on startup Android uses
            # verify to check if device exists already
            # and sends in phone ID (which is longer than
            # 11 characters!)
            '''
            if len(request.form["search_id"]) > 11:
                return "Username is too long!"
            '''

            user = kyzr.find_user(request.form["search_id"])

            if(user is None):
                return "False"
            return "True"
    return "Invalid Search"


# Used by Android App
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():

    if request.method=="POST":
        print request.form.keys()
        if("pid" in request.form.keys() and 
            "username" in request.form.keys() and
            "lat" in request.form.keys() and
            "lng" in request.form.keys()):

            pid = request.form["pid"]
            username = request.form["username"].lower()
            lat = float(request.form["lat"])
            lng = float(request.form["lng"])
            for i in string.punctuation:
                if i in username:
                    return "False"
            
            # Double check (?)
            # TODO: Figure out if we need this line
            user = kyzr.verify_user(pid, username)

            if(user is None):
                kyzr.add_user(pid, username, lat, lng)
                return "True"
            else:
                return "False"
    return "Invalid Search"


# Database adding for the android phones
@app.route('/dbadd', methods=['GET','POST'])
def dbadd():

    if request.method=="POST":
        if("lat" in request.form.keys() and "lng" in request.form.keys() and 
            "id1" in request.form.keys() and "id2" in request.form.keys()):

            for key in request.form.keys():
                if key == "lat":
                    try:
                        lat = float(request.form[key])
                    except:
                        return "Request Failed: latitude was not a float"
                elif key == "lng":
                    try:
                        lng = float(request.form[key])
                    except:
                        return "Request Failed: longitude was not a float"
                elif key == "id1":
                    phone1_id = request.form[key]
                elif key == "id2":
                    phone2_id = request.form[key]

            kyzr.swap_torch(phone1_id, phone2_id, lat, lng)
            
            return "Success"
    return "Request method failed."


# Get Dem Stats
@app.route('/stats', methods=['GET', 'POST'])
def stats():

    if request.method=="POST":
        if ("phone_id" in request.form.keys()):
            phone_id = request.form["phone_id"]
            stats = kyzr.compute_stats(phone_id)

            return json.dumps(stats)
            
    return "Request failed."


# TODO: Merge with stats() request
@app.route('/currtorch', methods=['GET', 'POST'])
def currtorch():

    if request.method=="POST":
        if ("phone_id" in request.form.keys()):
            phone_id = request.form["phone_id"]
            user = kyzr.find_user(phone_id)
            if user is not None:
                torch = user['torch']
                torchowner = kyzr.find_user(torch)
                return torchowner['username']

    return "Cannot find username."


# General debugging page
@app.route('/debug')
def debugging():
    queue = kyzr.get_queue()
    return render_template('debug.html',
                            queue=queue)

if __name__ == "__main__":
    app.run()
