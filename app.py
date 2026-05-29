from flask import Flask, render_template,url_for,request
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os
import pymysql.cursors
load_dotenv()


app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_DATABASE_HOST"] ="localhost"
app.config["MYSQL_DATABASE_DB"] = "dictionary"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("SQL_PASSWORD")

# Initialize MySQL
mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route("/", methods=["GET", "POST"])
def index():
    user_response = ""
    if request.method == "POST":
        user_input = request.form["word"]
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT meaning FROM word WHERE word = %s", (user_input))
        words = cursor.fetchall()
        user_response = words[0]["meaning"] if words else "Word not found in the dictionary."
    return render_template("index.html", user_response=user_response)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)