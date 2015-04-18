from flask import Flask, render_template, request
from pymongo import MongoClient
import json

# Setup Mongodb connection
client = MongoClient()

# The collection to be used
users = client.kyzr.users 

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

# coords=[(37.772323, -122.214897),
#         (21.291982, -157.821856),
#         (-18.142599, 178.431),
#         (-27.46758, 153.027892),
#         (-37.772323, -122.214897)]

    coords = []
    if(request.method=="POST"):
        print request.form.keys()
        if("id" in request.form.keys()):
            id_request = request.form["id"]
            user_data = users.find_one({'_id':id_request})

            if(user_data is not None):
                coords = user_data['transactions']

    return render_template('maps.html', coords=json.dumps(coords))


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

            first_user_data = users.find_one({'_id':phone1_id})
            second_user_data = users.find_one({'_id':phone2_id})

            if(first_user_data is not None):
                torch1_id = first_user_data['curr_torch']
            else:
                torch1_id = phone1_id

            if(second_user_data is not None):
                torch2_id = second_user_data['curr_torch']
            else:
                torch2_id = phone2_id

            # updates existing document and creates a new one if it doesn't exist
            users.update_one(
                {'_id':phone1_id}, 
                {
                    '$set':{'curr_torch':torch2_id}
                },
                True    # upsert
            )

            users.update_one(
                {'_id':phone2_id}, 
                {
                    '$set':{'curr_torch':torch1_id}
                },
                True    # upsert
            )

            users.update_one(
                {'_id':torch1_id},
                {
                    '$push':{'transactions':[lat,lng]}
                },
                True
            )

            users.update_one(
                {'_id':torch2_id},
                {
                    '$push':{'transactions':[lat,lng]}
                },
                True
            )

            #users.update_one({'_id':id1}, {'$set':{'curr_torch':id2}, '$push':{'transactions':[lat,lng]}}, True)
            
            return "Success"
    return "Request method failed."

def dbreturn():
    if request.method=="POST":
        if "id" in request.form.keys():
            phone_id = request.form["id"]
            # TODO: Get database info on current torch held and return it
            #users.find_one({'_id':phone_id})

            return "success!"
    return "Request failed: Return failed"

if __name__ == "__main__":
    app.run(debug=True)
