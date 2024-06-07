from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from psycopg2 import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

DB_HOST = "localhost"
DB_NAME = "Proje"
DB_USER = "postgres"
DB_PASS = "postgres"


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")
@app.route("/fileupload", methods=['GET',"POST"])
def fileupload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data 
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) 
        return "Başarıyla Yüklendi"
    return render_template("fileupload.html",form=form)
def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    return conn
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/submit_form", methods=["POST"])
def submit_form():
    if request.method == "POST":
        name = request.form["isim"]
        phone = request.form["tel"]
        email = request.form["mail"]
        subject = request.form["konu"]
        message = request.form["mesaj"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO customers (name, phone, email, subject, message) VALUES (%s, %s, %s, %s, %s)",
            (name, phone, email, subject, message),
        )

        conn.commit()
        cur.close()
        conn.close()

        return render_template("index.html")
@app.route('/login_register', methods=['POST'])
def login_register():
    if request.method == 'POST':
        connection = connect_db()
        cursor = connection.cursor()
        
        username = request.form['username']
        password = request.form['password']
        submit_button = request.form['submit_button']

        if submit_button == 'register':
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                session['username'] = username
                return redirect(url_for('index'))
            except Error as e:
                print("Error while registering:", e)
                connection.rollback()
        elif submit_button == 'login':
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return "Invalid username or password"

        cursor.close()
        connection.close()
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
@app.route("/asd")
def asd():
    return render_template("asd.html")
@app.route("/login")
def login():
    return render_template("login.html")
if __name__ == "__main__":
    app.run(debug=True)