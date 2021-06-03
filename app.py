from flask import *
import requests
import time

class Data():
    def __init__(self):
        self.xdata = []
        self.ydata = []
        self.start = False

    def setXdata(self, x):
        self.xdata = x

    def getXdata(self):
        return self.xdata

    def setYdata(self, y):
        self.ydata = y

    def getYdata(self):
        return self.ydata

    def setStart(self, start):
        self.start = start

    def getStart(self):
        return self.start

data = Data()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/single", methods=["GET"])
def single():
    try:
        r = requests.get("http://flaskosa.herokuapp.com/cmd/START")
        r = requests.get("http://flaskosa.herokuapp.com/cmd/TRACE")
        r = r.json()
        data.setXdata(r['xdata'])
        data.setYdata(r['ydata'])
        r = requests.get("http://flaskosa.herokuapp.com/cmd/STOP")
    except:
        print("Unable to fetch at the moment please try again")
    return render_template('index.html')


@app.route("/fetch/<action>", methods=["GET"])
def fetch(action):
    if action == "start":
        try:
            if(data.getStart() == False):
                data.setStart(True)
                requests.get("http://flaskosa.herokuapp.com/cmd/START")
            r = requests.get("http://flaskosa.herokuapp.com/cmd/TRACE")
            r = r.json()
            data.setXdata(r['xdata'])
            data.setYdata(r['ydata'])
        except:
            print("Unable to fetch at the moment please try again")
        return render_template('index.html', response="Start")
    else:
        try:
            requests.get("http://flaskosa.herokuapp.com/cmd/STOP")
            data.setStart(False)
        except:
            time.sleep(1)
            requests.get("http://flaskosa.herokuapp.com/cmd/STOP")
            data.setStart(False)
        return render_template('index.html')


@app.route("/api", methods=["GET"])
def cmd():
    try:
        r = requests.get("http://flaskosa.herokuapp.com/cmd/").text
    except:
        r = ""
    return r

@app.route("/api/<command>", methods=["GET"])
def api(command):
    try:
        r = requests.get("http://flaskosa.herokuapp.com/cmd/" + command).text
    except:
        r = ""
    return requests.get("http://flaskosa.herokuapp.com/cmd/" + command).text

@app.route("/cmd", methods=["GET"])
def command():
    try:
        r = requests.get("http://flaskosa.herokuapp.com/cmd/" + request.args.get('command')).text
    except:
        r = ""
    return requests.get("http://flaskosa.herokuapp.com/cmd/" + request.args.get('command')).text

@app.route("/graph")
def graph():
    return render_template('plotly_graph.html')

@app.route("/data", methods=["GET"])
def graphUpdate():
    return {"xdata": data.getXdata(), "ydata":data.getYdata()}
