from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
import pymysql
from dotenv import load_dotenv

app = Flask(__name__)
mysql = MySQL(app)

load_dotenv(".env", verbose=True)
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = request.form['email']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('''
                       CREATE TABLE IF NOT EXISTS request (id INTEGER, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(100))
                        ''')
        cur.execute('SELECT email, COUNT(*) FROM request WHERE email = %s', (email))
        data = cur.fetchone()
        if data['email'] is None:
            cur.execute("INSERT INTO request (first_name, last_name, email) VALUES (%s,%s,%s)",
                        (first_name, last_name, email))
            conn.commit()
            conn.close()
            return render_template('thanks.html')
        else:
            return render_template('index.html', message=" You have already submitted the form")


if __name__ == "__main__":
    app.run(port=4999)
