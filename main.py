#import uuid
#get_uuid = lambda: str(uuid.uuid4())
import random
from flask import Flask, render_template, request, g, session, flash, redirect, url_for
from pymongo import MongoClient
app = Flask(__name__)

app.secret_key = "leoadjaskjdfashfhadsfkjjasdfj"

def get_uuid():
	db = open_db()
	while 1:
		a=""
		for k in random.sample(range(1, 100), 3):
			a+="{}".format(k)
		if not db.find_one({"id": a}):
			break
	return a

@app.before_request
def before_request():
	if 'userid' in session:
		db = open_db()
		if db.find_one({"id": session["userid"]}) == None:
			session.pop('userid')

@app.teardown_appcontext
def close_db(err=None):
	if hasattr(g, 'db'):
		g.db.close()

def open_db():
	if not hasattr(g, 'db'):
		g.db = MongoClient()
	return g.db["vmlan"]["teams"]


@app.route("/")
@app.route("/miskusmillal")
def miskusmillal():
	return render_template('miskusmillal.html')

@app.route('/mis')
def mis():
	return render_template('mis.html')

@app.route("/registreeru", methods=["POST", "GET"])
def registreeru():
	if 'userid' in session:
		return redirect(url_for("registreeritud"))
	if request.method == 'POST':
		print(request.form)
		if not 'g-recaptcha-response' in request.form:
			flash("Ära jäta captchat vahele! :)")
			return render_template("registreeru.html")
		elif 'g-recaptcha-response' in request.form and len(request.form['g-recaptcha-response']) < 1:
			flash("Ära jäta captchat vahele! :)")
			return render_template("registreeru.html")
		if "type" and "email" in request.form:
			if len(request.form["type"]) < 1 or len(request.form["email"]) < 1:
				flash("Esines viga, proovige uuesti")
				return render_template("registreeru.html")
			else:
				info = {
					"type": request.form['type'],
					"email": request.form['email'],
					"id": get_uuid(),
					"moneypaid": False,
					"team": {
						"teamName": None,
						"leader": False,
						"members": {
						}
					}
				}
				db = open_db()
				if db.find_one({"email": request.form["email"]}):
					flash("Antud email on juba kasutusel")
					return render_template("registreeru.html")
				db.insert(info)
				session["userid"] = info["id"]
				return redirect(url_for("registreeritud"))
		else:
			if "type" not in request.form:
				flash("Te ei valinud pileti tüüpi!")
			elif "email" not in request.form:
				flash("Te ei kirjutanud oma emaili!")
			return render_template("registreeru.html")
	return render_template("registreeru.html")

@app.route("/registreeritud", methods=["POST", "GET"])
def registreeritud():
	regcode = (request.form['regcode'] if 'regcode' in request.form else (session['userid'] if 'userid' in session else None))
	if regcode == None:
		flash("Sessiooni pole, palun logige sisse või registreeruge")
		return redirect("/registreeru")
	session["userid"] = regcode
	db = open_db()
	info = db.find_one({"id": regcode})
	if not info:
		flash("Antud koodi pole registreeritud")
		return redirect(url_for("registreeru"))
	return render_template("registreeritud.html", info=info)


@app.route("/tiimid")
def tiimid():
	regcode = (session['userid'] if 'userid' in session else None)
	if regcode == None:
		flash("Sessiooni pole, palun logige sisse või registreeruge")
		return redirect("/registreeru")
	db = open_db()
	if not db.find_one({"id": regcode})["type"] == "csgocomp":
		return "teil pole CS:GO võistleja pilet, et hallata tiime"
	else:
		return "herro"

@app.route("/cancel")
def cancel():
	regcode = (session.pop('userid') if 'userid' in session else None)
	if regcode == None:
		flash("Sessiooni pole, palun logige sisse või registreeruge")
		return redirect("/registreeru")
	db = open_db()
	info = db.find_one({"id": regcode})
	if not info:
		flash("Pole sellist piletit")
	elif info["moneypaid"] == True:
		flash("Makstud piletit ei saa enam kahjuks tühistada")
	else:
		flash("Pilet tühistatud")

	return redirect(url_for("miskusmillal"))

@app.route("/lahku")
def logout():
	if 'userid' in session:
		session.pop('userid')
	return redirect(url_for("miskusmillal"))

@app.route("/kontakt")
def kontakt():
	return render_template("kontakt.html")

@app.route("/live")
def live():
	return render_template("live.html")

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
