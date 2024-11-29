from flask import Flask, render_template, request, redirect, url_for
from utils.hwio import getList
from datetime import datetime
import subprocess
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route('/settings')
def settings():
    devices = getList()  # Zavolání funkce getList pro získání zařízení
    return render_template("settings.html", devices=devices)

@app.route('/rename', methods=['POST'])
def rename_device():
    device_id = request.form['device_id']
    new_alias = request.form['new_alias']
    subprocess.run(["bch", "node", "rename", device_id, new_alias])
    return redirect(url_for('settings'))

@app.route('/delete', methods=['POST'])
def delete_device():
    device_id = request.form['device_id']
    subprocess.run(["bch", "node", "remove", device_id])
    return redirect(url_for('settings'))


@app.route('/oxidesensors')
def oxidesensors():
    try:
        response = requests.get('http://localhost:8080/api/getCO2Concentration')
        data = response.json()
        dt_object = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    except requests.exceptions.JSONDecodeError:
        response = requests.get("http://localhost:8080/api/latestCO2Concentration")
        data = response.json()
        return render_template("oxidesensors.html", concetration=data["concentration"], timestamp=data["time"])
    return render_template('oxidesensors.html', concentration=data["concentration"], timestamp=formatted_time)

@app.route("/temperaturesensors")
def temperaturesensors():
    try:

        response = requests.get("http://localhost:8080/api/getTemperature")
        data = response.json()
        dt_object = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    except requests.exceptions.JSONDecodeError:

        response = requests.get("http://localhost:8080/api/latestTemperature")
        data = response.json()

        return render_template("temperatures.html", temperature=data["latest_temperature"], timestamp=data["time"])
    return render_template("temperatures.html", temperature=data["temperature"], timestamp=formatted_time)

@app.route("/lightsensors")
def lightsensors():
    try:
        response = requests.get("http://192.168.50.100:8080/api/getIlluminance")
        data = response.json()
        dt_object = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%S.%f")
        formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    except requests.exceptions.JSONDecodeError:
        response = requests.get("http://localhost:8080/api/latestIlluminance")
        data = response.json()
        return render_template("lightsensors.html", intensity=data["concentration"], timestamp=data["time"])
    return render_template("lightsensors.html", intensity=data["concentration"], timestamp=formatted_time)
    

if __name__ == '__main__':
 app.run(host="0.0.0.0", debug=True)
