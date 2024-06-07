from flask import Flask, render_template, request, redirect, url_for
import psycopg2


app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "Proje"
DB_USER = "postgres"
DB_PASS = "postgres"

def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def invalid_route(e):
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["login-username"]
        password = request.form["login-password"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            if password == user[2]:
                cur.close()
                conn.close()
                return redirect(url_for("index"))
            else:
                error = "Şifre yanlış!"
                return render_template("login.html", error=error)
        else:
            error = "Kullanıcı bulunamadı!"
            return render_template("login.html", error=error)
    else:
        pass

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        username = request.form["register-username"]
        password = request.form["register-password"]

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for("index"))
    else:
        pass

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

@app.route("/asd")
def asd():
    return render_template("asd.html")

if __name__ == "__main__":
    app.run(debug=True)
