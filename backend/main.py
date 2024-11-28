from flask import Flask, render_template, request, redirect, url_for
from utils.hwio import getList

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

if __name__ == '__main__':
    app.run(debug=True)
