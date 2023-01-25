from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/poe-reboot")
def poeReboot():
    return render_template("poe-reboot.html")

if __name__ == "__main__":
    app.run(debug=True, port=55555)