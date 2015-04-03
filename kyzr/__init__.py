from flask import Flask, render_template, request
from pymongo import MongoClient
import json

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/maps/<coords>')
def maps(coords=[(37.772323, -122.214897),
        (21.291982, -157.821856),
        (-18.142599, 178.431),
        (-27.46758, 153.027892),
        (-37.772323, -122.214897)]):

    return render_template('maps.html', coords=json.dumps(coords))

@app.route('/dbadd', methods=['GET','POST'])
def dbadd():
    if request.method=="POST":
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
                id1 = request.form[key]
            elif key == "id2":
                id2 = request.form[key]

        # TODO: Add database addition here
        
        return "Success"
    return "Request method failed."

def dbreturn():
    if request.method=="POST":
        if "id" in request.form.keys():
            phone_id = request.form["id"]
            # TODO: Get database info on current torch held and return it

            return "success!"
    return "Request failed: Return failed"

@app.route('/full')
def map():
    return render_template('full_map.html')

@app.route('/line')
def line():
    return render_template('maps_old.html')

if __name__ == "__main__":
    app.run()
