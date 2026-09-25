from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
import base64
from dotenv import load_dotenv


load_dotenv()

user = os.getenv("user")
pword = os.getenv("pword")
app = Flask(__name__)
app.secret_key = os.getenv("skey")

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


if __name__ == "__main__":

    app.run(debug=True,host='0.0.0.0', port=5000)