[![alt tag](https://raw.githubusercontent.com/byronwasti/Kyzr-Server/master/kyzr/static/images/TheKyzrProject.png)](http://www.thekyzrproject.com/)
===
# Welcome to The Kyzr Project's Server Repo

##FAQ

### What is The Kyzr Project?
It is a cool project

### How do I play?
Download the app!

### Where can I check my Torch's location?
[thekyzrproject.com](www.thekyzrproject.com)


How the server is run
===
Our server is a full-stack implementation of a LAMP server setup.
We are running Debian 7, Apache server, Mongodb and python-Flask.

For mapping the travel of the torch we are using Google Maps API, with on-the-fly javascript creation.

Updating the database is done via POST requests.

What do I need to run the server?
===
####This is for people who want to create their own implementation of the server code.
###The dependencies this project is built off of are:
  * python-2.7
  * python-flask (latest version)
  * pyMongo-3.0 (or later)
  * Mongodb-ALL-2.0.6 (or later)
  * Apache2-server

###Installation
To install the code onto your server you will first need to set up Apache2-server with Flask. A good tutorial on this can be found on [DigitalOceans website](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps).

Once that is set up, simply copy this code into the `/var/www/` folder.
