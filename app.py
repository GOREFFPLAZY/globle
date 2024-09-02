from flask import Flask, render_template, redirect, session, request
from bs4 import BeautifulSoup
import requests, random

app = Flask(__name__)
app.secret_key = "gleezeborpglorp"

def distance(c1, c2):
    if c1.strip().lower() == c2.strip().lower():
        return "0"
    try:
        url = f"https://www.luftlinie.org/{c1}/{c2}"
        result = requests.get(url)
        doc = BeautifulSoup(result.content, "html.parser")

        title = doc.find(text="km")
        title = str(title.parent.parent)
        title = title.replace("<span class=\"headerAirline\">Entfernung: <span class=\"value km\">", "")
        title = title.replace("</span> <span class=\"unit km\">km</span></span>", "")

        return title[:-3]
    except:
        return "error"

def random_country():
    with open("countries.csv", "r") as file:
        countries = file.readlines()
        country = random.choice(countries)

    return country

@app.route("/")
def start():
    if "country" in session:
        pass
    else:
        session["country"] = random_country()
        session["guesses"] = list()

    return render_template("index.html", distance="distance in", won=False)

@app.route("/restart")
def restart():
    return redirect("/pop")

@app.route("/pop")
def pop():
    session.clear()
    return redirect("/")

@app.route("/play", methods=["POST"])
def play():
    # try:
    if session:
        icountry = request.form["country"]
    else:
        return redirect("/")
    
    km = distance(session["country"], icountry)

    #return f"{session['country']} und {icountry}"

    if km != "error":
        g = session["guesses"]
        if icountry.lower() not in g:
            g.extend([icountry.lower()])
            session["guesses"] = g
        if km == "0":
            return render_template("index.html", distance=km, guesses=g, won=True)
        else:
            return render_template("index.html", distance=km, guesses=g, won=False)
    else:
        return render_template("index.html", distance="NaN", error="Invalid country :(", won=False)
    # except:
    #     return 'vorp'
    #     return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, port=5500)