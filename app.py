from flask import Flask, render_template, redirect, session, request
from bs4 import BeautifulSoup
import requests, random
import json

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

def random_city():
    with open("cities.csv", "r") as file:
        cities = file.readlines()
        city = random.choice(cities)

    return city

def update(name, guesses):
    with open('leaderboard.json', 'r') as file:
        data = json.load(file)

    temp = data["leaderboard"]
    temp.append([name, guesses])
    data["leaderboard"] = sorted(temp, key=lambda x: x[1])

    with open('leaderboard.json', 'w') as file:
        json.dump(data, file, indent=4)

def leaderboard():
    with open('leaderboard.json', 'r') as file:
        data = json.load(file)

    return data["leaderboard"][:10]

@app.route("/")
def start():
    if "name" not in session:
        return render_template("name.html")
    else:  
        return redirect("/country")
    
@app.route("/name", methods=["POST"])
def name():
    name = request.form["name"]
    session["name"] = name
    return redirect("/country")

@app.route("/country")
def country():
    if "country" in session and "name" in session:
        if session["country"] != None and session["name"] != None:
            pass
        else:
            session["country"] = random_country()
            session["guesses"] = list()
    else:
        session["country"] = random_country()
        session["guesses"] = list()

    return render_template("country.html", distance="distance in", won=False)

@app.route("/city")
def city():
    if "city" in session and "name" in session:
        if session["city"] != None and session["name"] != None:
            pass
        else:
            session["city"] = random_city()
            session["guesses"] = list()
    else:
        session["city"] = random_city()
        session["guesses"] = list()

    return render_template("city.html", distance="distance in", won=False)

@app.route("/restart")
def restart():
    return redirect("/pop")

@app.route("/pop")
def pop():
    session["country"] = None
    session["city"] = None
    return redirect("/")

@app.route("/popall")
def popall():
    session.clear()
    return redirect("/")

@app.route("/country/play", methods=["POST"])
def country_play():
    # try:
    if "country" in session:
        icountry = request.form["country"]
    else:
        return redirect("/")
    
    km = distance(session["country"], icountry)

    #return f"{session['country']} und {icountry}"

    if km != "error":
        g = session["guesses"]
        g.extend([icountry.lower()])
        session["guesses"] = g
        if km == "0":
            update(session["name"], len(session["guesses"]))
            return render_template("country.html", distance=km, guesses=g, won=True, leaderboard=leaderboard())
        else:
            return render_template("country.html", distance=km, guesses=g, won=False, c=session["country"], leaderboard=leaderboard())
    else:
        return render_template("country.html", distance="NaN", error="Invalid country :(", won=False, leaderboard=leaderboard())
    # except:
    #     return 'vorp'
    #     return redirect("/")

@app.route("/city/play", methods=["POST"])
def city_play():
    # try:
    if "city" in session:
        icity = request.form["city"]
    else:
        return redirect("/")
    
    km = distance(session["city"], icity)

    #return f"{session['country']} und {icountry}"

    if km != "error":
        g = session["guesses"]
        g.extend([icity.lower()])
        session["guesses"] = g
        if km == "0":
            update(session["name"], len(session["guesses"]))
            return render_template("city.html", distance=km, guesses=g, won=True, leaderboard=leaderboard())
        else:
            return render_template("city.html", distance=km, guesses=g, won=False, c=session["city"], leaderboard=leaderboard())
    else:
        return render_template("city.html", distance="NaN", error="Invalid city :(", won=False, leaderboard=leaderboard())
    # except:
    #     return 'vorp'
    #     return redirect("/")

if __name__ == "__main__":
    app.run(debug=False, port=5500)