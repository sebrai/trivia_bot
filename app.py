from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os
import base64
from dotenv import load_dotenv


load_dotenv()

user = os.getenv("user")
pword = os.getenv("p_word")
app = Flask(__name__)
app.secret_key = os.getenv("skey")

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user=user,
        password=pword,
        database="trivia"
    )