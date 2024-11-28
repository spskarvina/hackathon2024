from flask import Flask
from flask import render_template
from utils.hwio import getList

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route('/settings')
def settings():
    devices = getList()  # Zavolání funkce getList pro získání zařízení
    return render_template("settings2.html", devices=devices)
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

    