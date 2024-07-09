from flask import *
import sqlite3
import time
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

app.secret_key = 'Qi7lbesp$=lqay=5t@r4'


@app.route("/")
def home():
    mHead = "Connecting You To Your future"
    return render_template("index.html", ab = mHead )

@app.route("/temp")
def temp():
    return render_template("all-job.html")

@app.route("/temp2")
def temp2():
    return render_template("job-single.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")  
    
@app.route("/index")
def index():
    return render_template("index.html")      



@app.route("/company-login", methods = ['GET','POST'])
@app.route("/company/login", methods = ['GET','POST'])
def company_login():
    if request.method == 'POST':
        login_email = request.form['log_email']
        login_pass  = request.form['log_password']
        if login_email is not None and login_pass is not None:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (login_email,))
            user = cursor.fetchone()
            conn.close()
        
            if user and check_password_hash(user[2], login_pass):
                session['email'] = login_email
                return redirect(url_for('company_dash'))
            else:
                return "Invalid credentials"
        
        ##############################################

        company_name = request.form['company-name']
        company_tagline = request.form['company-tagline']
        company_website = request.form['company-website']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re_password']
        
        if password == re_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO company (email, password, name, website, tagline) VALUES (?, ?, ?, ?, ?)", (email, hashed_password, company_name, company_website, company_tagline))
            conn.commit()
            conn.close()
            session['email'] = email
            return redirect(url_for('company_dash'))
        else:
            return "Passwords do not match"
    return render_template("employer_login.html")      



@app.route("/post_job")
def post_job():
    return render_template("post-job.html")  


@app.route("/job_post")
def job_post():
    return render_template("job_post.html")  

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS company (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT, name TEXT, tagline TEXT, website TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, region TEXT, type TEXT, desc TEXT, company_id TEXT, time TEXT)')

    print("Table created successfully")
    conn.close()

init_sqlite_db()



@app.route('/login', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = None
        password = None
        try:
            email = request.form['email']
            password = request.form['password']
        except Exception as e:
            print(e)
        
        if email is not None and password is not None:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()
        
            if user and check_password_hash(user[2], password):
                session['email'] = email
                return redirect(url_for('dash'))
            else:
                return "Invalid credentials"

        ##########################################

        s_email = request.form['sign_email']
        s_password = request.form['sign_password']
        re_password = request.form['sign_re_password']
        
        if s_password == re_password:
            hashed_password = generate_password_hash(s_password, method='pbkdf2:sha256')
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (s_email, hashed_password))
            conn.commit()
            conn.close()
            session['email'] = s_email
            return redirect(url_for('signup'))
        else:
            return "Passwords do not match"
    return render_template('login.html')


@app.route('/dashboard')
def dash():
    return render_template('all-job.html')

@app.route('/job-details')
def job_details():
    return render_template("job-single.html")



########################################################################

@app.route("/company/dashboard")
def company_dash():
    email = session['email']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE company_id = ?", (email,))
    jobs = cursor.fetchall()
    conn.close()
    print(jobs)
    return render_template("company-dash.html")  

@app.route('/company/posts')
def company_posts():
    return render_template('applicants.html')

@app.route("/company/posts/add",methods=['GET','POST'])
def company_add_post():

    if request.method == 'POST':
        region = request.form['region']
        type = request.form['job-type']
        desc = request.form['job-description']
        time1 = time.time()
        c_id = session['email']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (region,type,desc,company_id,time) VALUES (?, ?, ?, ?, ?)", (region, type, desc, c_id,time1))
        conn.commit()
        conn.close()


    return render_template("job_post.html")  

@app.route("/logout")
def logout():
    return "create logout logic you idiots!!"



if __name__ == '__main__':
    app.run(debug=True)