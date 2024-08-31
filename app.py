from flask import Flask, render_template, redirect, session, request
from bs4 import BeautifulSoup
import requests, random

app = Flask(__name__)
app.secret_key = "gleezeborpglorp"

def distance(c1, c2):
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
    if session:
        pass
    else:
        session["country"] = random_country()

    return render_template("index.html", distance="distance in")

@app.route("/restart")
def restart():
    session["country"] = random_country()
    return redirect("/")

@app.route("/play", methods=["POST"])
def play():
    try:
        if session:
            icountry = request.form["country"]
        else:
            return redirect("/")
        
        km = distance(session["country"], icountry)

        if km != "error":
            return render_template("index.html", distance=km)
        else:
            return render_template("index.html", distance="NaN", error="Invalid country :(")
    except:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5500)