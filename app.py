from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
import base64
from dotenv import load_dotenv
import requests

load_dotenv()

user = os.getenv("user")
pword = os.getenv("pword")
app = Flask(__name__)
app.secret_key = os.getenv("skey")

diffurls = {
    'easy': 'https://opentdb.com/api.php?amount=1&difficulty=easy&type=boolean&encode=base64',
    'medium':"https://opentdb.com/api.php?amount=1&difficulty=medium&type=boolean&encode=base64",
    "hard": "https://opentdb.com/api.php?amount=1&difficulty=hard&type=boolean&encode=base64"
    }

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user=user,
        password=pword,
        database="trivia"
    )


@app.route("/")
def blank():
    return redirect(url_for('login'))



@app.route("/login", methods=["POST","GET"])
def login():
    if  session.get('id'):
      return redirect(url_for('home'))
    if request.method == "POST":
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id,username,password,role FROM users WHERE username=%s", (brukernavn,))
        bruker = cursor.fetchone()
        cursor.close()
        conn.close()
        if not bruker:
            return render_template("login.html", feil_melding="wrong username or password")
        if bruker and check_password_hash(bruker['password'], passord):
            session['username'] = bruker['username']
            session['id'] = bruker['id']
            session['role'] = bruker['role']
            flash("succesfully loged in as: "+bruker['username'],"succes")
            return redirect(url_for("home"))
        else:
            return render_template("login.html", feil_melding="wrong username or password")

    return render_template("login.html")

@app.route("/new_user", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        brukernavn = request.form['brukernavn']
        passord = generate_password_hash(request.form['passord'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                       (brukernavn, passord))
        conn.commit()
        cursor.close()
        conn.close()
        flash("user registered!", "success")
        return redirect(url_for("login"))

    return render_template("registrer.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("you have logged out", "info")
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if  not session.get('id'):
      return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.close()
    conn.close()
    return render_template('home.html')

@app.route("/call_q/<diff>")
def call_q(diff):
    client_ip = request.remote_addr
    if client_ip != "127.0.0.1":
        flash("you dont have acces to that route") 
        return redirect(url_for("home"))
    # this may break in the future
    url = diffurls[diff]
    try:
      
        response = requests.get(url)
        
     
        response.raise_for_status()
      
        data = response.json()
        
     
        # print("Success! Data retrieved:")
        # print(data)
        # print(f"Title: {data.get('title')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        flash(f"failed to get question error: {http_err}", "api contact failed")
        flash("try again later","advice")
        return redirect(url_for('home'))
    except Exception as err:
        print(f"An error occurred: {err}")
        flash(f"failed to get question unforseen error: {err}" , "unforseen error")
        return redirect(url_for('home'))
    for key in data['results'][0]:
        if key != "incorrect_answers":
            data['results'][0][key] = base64.b64decode(data['results'][0][key]).decode("utf-8")
        else:
            data['results'][0][key][0] = base64.b64decode(data['results'][0][key][0]).decode("utf-8")
    # print(data)

    # return redirect(url_for('home'))
    return data

@app.route("/anwser/<diffi>", methods=["GET", "POST"])
def anwser(diffi):
    url = 'http://127.0.0.1:5000' + url_for("call_q",diff = diffi)
    try:
      
        response = requests.get(url)
        
     
        response.raise_for_status()
      
        data = response.json()
        

    except requests.exceptions.HTTPError as http_err:
        flash(f"unkown error: {http_err}","error")
        return redirect(url_for('home'))
    except Exception as err:
        flash(f"unkown error: {err}","error")
        return redirect(url_for('home'))
    # print(type(data),data)
    return render_template("question.html", q = data)

if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0', port=5000)