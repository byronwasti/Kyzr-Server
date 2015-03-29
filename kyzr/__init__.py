from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/maps')
def maps():
    return render_template('maps.html')

@app.route('/info')
def info():
    pass

if __name__ == "__main__":
    app.run()
