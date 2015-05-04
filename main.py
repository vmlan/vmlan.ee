from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
@app.route("/miskusmillal")
def miskusmillal():
    return render_template('miskusmillal.html')

@app.route("/registreeru")
def registreeru():
    return render_template("registreeru.html")

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")

@app.route("/live")
def live():
    return render_template("live.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")