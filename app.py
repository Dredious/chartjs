
from random import sample
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config['MONGO_DBNAME'] = "brcsqm_data"
app.config["MONGO_URI"] = "mongodb://desktop-mjhm34r.penv.internal:27017/brcsqm_data"
mongo = PyMongo(app)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/devices", methods=['GET'])
def get_devices():
    # return render_template("index.html")
    devices = mongo.db.all_packets.distinct("device_id")
    
    # output = []
    # for q in devices.find():
    #     output.append({'device_id': q['device_id']})

    return jsonify({'result' : devices})

@app.route("/device/<device_id>", methods=['GET'])
def get_device(device_id):
    devices = mongo.db.all_packets

    output = []
    for q in devices.find({'device_id' : device_id}):
        output.append({'device_id': q['device_id'], 'SQM_Value' : q['SQM_Value'], 'amp_temp' : q['amb_temp'], 'sky_temp' : q['sky_temp'], 'time' : q['time']})

    return jsonify({'result' : output})

@app.route("/device_data", methods=['GET']) #Dangerous, too much data.
def get_device_data():
    devices = mongo.db.all_packets

    output = []
    for q in devices.find({}):
        output.append({'device_id': q['device_id'], 'SQM_Value' : q['SQM_Value'], 'amp_temp' : q['amb_temp'], 'sky_temp' : q['sky_temp'], 'time' : q['time']})

    return jsonify({'result' : output})

@app.route("/device/<device_id>/time/<time>", methods=['GET'])
def get_device_and_time(device_id, time):
    devices = mongo.db.all_packets

    q = devices.find_one({'device_id' : device_id, 'time' : time})
    if q:
        output = {'device_id' : q['device_id'], 'SQM_Value' : q['SQM_Value'], 'amp_temp' : q['amb_temp'], 'sky_temp' : q['sky_temp'], 'time' : q['time']}
    else:
        output = "No results found"

    return jsonify({'result' : output})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.50.135')