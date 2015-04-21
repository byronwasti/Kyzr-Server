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

# Map page
# TODO: Merge with homepage (?)
#       Call map data from database
#       Have input from phone ID
#@app.route('/maps/<coords>')
@app.route('/maps', methods=['GET', 'POST'])
def maps():
    coords = []
    center = [0,0]
    if(request.method=="POST"):
        if("id" in request.form.keys()):
            user = kyzr.find_user(request.form["id"])

            if(user is not None):
                coords = user['locs']
            else:
                return "ID: " + id_request + " not found"
    if coords:
        center = [ float(sum(i)/len(i)) for i in ([coords[j][0] for j in coords], [coords[k][1] for k in coords]) ]
        #center = [10,10]
    #center = [42.2927482,   -71.2640407]
    #return render_template('maps.html', coords=json.dumps(coords), center=json.dumps(center))
    return render_template('error.html', coords=json.dumps(coords), center=json.dumps(center))
    #return render_template('error.html', coords=coords, center=center)


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

if __name__ == "__main__":
    app.run()
