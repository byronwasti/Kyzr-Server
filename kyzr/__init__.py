from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/maps')
def maps():
    flightPlanCoordinates= [(37.772323, -122.214897),
        (21.291982, -157.821856),
        (-18.142599, 178.431),
        (-27.46758, 153.027892)]

    return render_template('maps.html', flightPlanCoordinates=flightPlanCoordinates)

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method=="POST":
        if "message" in request.form.keys():
            return request.form["message"][::-1]
        else:
            return "SOMETHING DONE GOOFED"

    return "No Request Sent"

@app.route('/full')
def map():
    return render_template('full_map.html')

@app.route('/line')
def line():
    return render_template('maps_old.html')

if __name__ == "__main__":
    app.run()
