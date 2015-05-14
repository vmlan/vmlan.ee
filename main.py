import uuid
get_uuid = lambda: str(uuid.uuid4())
from flask import Flask, render_template, request, g, session, flash
from pymongo import MongoClient
app = Flask(__name__)

app.secret_key = "leoadjaskjdfashfhadsfkjjasdfj"

ticketTypes = {
	"csgocomp": "CS: GO Võistleja pilet",
	"normcomp": "Tavavõistleja pilet",
	"spectator": "Pealtvaataja pilet"
}

@app.before_request
def before_request():
	if 'userid' in session:
		db = open_db()

@app.teardown_appcontext
def close_db(err=None):
	if hasattr(g, 'db'):
		g.db.close()

def open_db():
	g.db = MongoClient("mongo://127.0.0.1/")
	return g.db["vmlan"].teams


@app.route("/")
@app.route("/miskusmillal")
def miskusmillal():
	return render_template('miskusmillal.html')

@app.route('/mis')
def mis():
	return render_template('mis.html')

@app.route("/registreeru", methods=["POST", "GET"])
def registreeru():
	if request.method == 'POST':
		print(request.form)
		if "type" and "email" in request.form:
			return """Email kuhu saadetakse info: {}
Pileti tüüp: {}
Teie id (vaja LAN-il soodustuseks/lehel sisselogimiseks): {}""".format(request.form["email"], ticketTypes[request.form["type"]], get_uuid())
		else:
			if "type" not in request.form:
				flash("Te ei valinud pileti tüüpi!")
			elif "email" not in request.form:
				flash("Te ei kirjutanud oma emaili!")
			return render_template("registreeru.html")
	else:
		return render_template("registreeru.html")

@app.route("/kontakt")
def kontakt():
	return render_template("kontakt.html")

@app.route("/live")
def live():
	return render_template("live.html")

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
