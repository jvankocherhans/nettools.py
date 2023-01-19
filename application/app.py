from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def dashboard():
    return "dashboard"

@app.route("/template")
def template():
    return render_template("template.html")

@app.route("/poe-reboot")
def poeReboot():
    return render_template("poe-reboot.html")

if __name__ == "__main__":
    app.run(debug=True)