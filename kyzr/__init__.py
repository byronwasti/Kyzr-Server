from flask import Flask, render_template, request
import json

# pyMongodb wrapper
from kyzr_db import dbEditor
kyzr = dbEditor()

# Setup flask
app = Flask(__name__)

# Main homepage
# TODO: Add login ability and other inputs
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/class_notes')
def notes():
    return render_template('class_notes.html')

# Map page
# TODO: Merge with homepage (?)
#       Call map data from database
#       Have input from phone ID
#@app.route('/maps/<coords>')
@app.route('/maps', methods=['GET', 'POST'])
def maps():
    coords = []
    center = [0,0]
    zoom = 3
    torchID = ''
    error = False
    dist = ''
    username = '' 
    num_tran = '' 

    if(request.method=="POST"):
        if("id" in request.form.keys()):
            torchID = request.form["id"]

            if(torchID):
                user = kyzr.find_user(torchID)
                if(user is not None):
                    coords = user['locs']
                else:
                    error = True
            #else:
            #    return render_template('error.html')
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
        username = stats['TORCH']
        num_tran = stats['NUMTRANSACTION']


    return render_template('maps.html',
           coords=json.dumps(coords),
           center=json.dumps(center),
           zoom=json.dumps(zoom),
           torchID=torchID,
           dist=dist,
           torch_held=username,
           num_tran=num_tran,
           error=error)
#   return render_template('debug.html', 
#           coords=json.dumps(coords), 
#           center=json.dumps(center),
#           zoom=json.dumps(zoom))


@app.route('/verify', methods=['GET', 'POST'])
def verify():

    if request.method=="POST":
        if ("search_id" in request.form.keys()):
            if( ' ' in request.form["search_id"]):
                return "Username cannot contain spaces."

            user = kyzr.find_user(request.form["search_id"])

            if(user is None):
                return "False"
            return "True"
    return "Invalid Search"


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
            if ' ' in username:
                return "False"

            user = kyzr.verify_user(pid, username)

            if(user is None):
                kyzr.add_user(pid, username, lat, lng)
                return "True"
            else:
                return "False"
    return "Invalid Search"


# Next two functions are for database 
# adding/receiving for the android phones
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

@app.route('/stats', methods=['GET', 'POST'])
def stats():

    if request.method=="POST":
        if ("phone_id" in request.form.keys()):
            phone_id = request.form["phone_id"]

            #stats = sc.compute_stats(user)
            stats = kyzr.compute_stats(phone_id)

            return json.dumps(stats)
            
    return "Request failed."

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

if __name__ == "__main__":
    app.run()
