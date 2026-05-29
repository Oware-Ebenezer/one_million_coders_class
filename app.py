from flask import Flask, render_template,url_for,request
from flaskext.mysql import MySQL
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_DATABASE_HOST"] ="localhost"
app.config["MYSQL_DATABASE_DB"] = "dictionary"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("SQL_PASSWORD")

# Initialize MySQL
mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def index():
    user_response = ""
    if request.method == "POST":
        conn = mysql.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT meaning FROM word WHERE word = %s", (request.form["word"],))
        words = cursor.fetchall()
        user_response = words[0][0] if words else ""
    return render_template("index.html", user_response=user_response)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)