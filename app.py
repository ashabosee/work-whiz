from flask import *
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.secret_key = 'your_secret_key'


@app.route("/")
def home():
    mHead = "Connecting You To Your future"
    return render_template("index.html", ab = mHead )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")  
    
@app.route("/index")
def index():
    return render_template("index.html")      

@app.route("/login")
def login():
    return render_template("login.html")  

@app.route("/employer_login")
def employer_login():
    return render_template("employer_login.html")      



@app.route("/post_job")
def post_job():
    return render_template("post-job.html")  

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")  

@app.route("/job_post")
def job_post():
    return render_template("job_post.html")  

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
    print("Table created successfully")
    conn.close()

init_sqlite_db()



@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re_password']
        
        if password == re_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        else:
            return "Passwords do not match"
    return render_template('login.html')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['email'] = email
            return redirect(url_for('job_post'))
        else:
            return "Invalid credentials"
    return render_template('login.html')


if __name__ == '__main__':
    app.run()