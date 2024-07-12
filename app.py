from flask import *
import sqlite3
import time
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

app.secret_key = 'Qi7lbesp$=lqay=5t@r4'

conn = sqlite3.connect('database.db')


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

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        Fname = request.form['fname']
        Lname = request.form['lname']
        email = request.form['email']
        sub = request.form['subject']
        msg = request.form['message']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contact (Fname, Lname, email, sub, msg) VALUES (?, ?, ?, ?, ?)",
                       (Fname, Lname, email, sub, msg))
        conn.commit()
        conn.close()
        return redirect(url_for('contact'))

    return render_template("contact.html")


    
@app.route("/index")
def index():
    return render_template("index.html")      



@app.route("/company-login", methods = ['GET','POST'])
@app.route("/company/login", methods = ['GET','POST'])
def company_login():
    if request.method == 'POST':
        login_email = None
        login_pass = None
        try:
            login_email = request.form['log_email']
            login_pass  = request.form['log_password']
        except Exception as e:
            print(e)
        if login_email is not None and login_pass is not None:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM company WHERE email = ?", (login_email,))
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



@app.route("/post-job")
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
    conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, region TEXT, type TEXT, desc TEXT, VACANCY TEXT, exp TEXT, sal TEXT, edu TEXT, company_id TEXT, time TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS contact (id INTEGER PRIMARY KEY AUTOINCREMENT, Fname TEXT, Lname TEXT, email TEXT, sub TEXT, msg TEXT)')
    
    conn.close()

init_sqlite_db()



@app.route('/login', methods=['GET', 'POST'])
def signup():
    msg = None
    alert_msg = request.args.get("msg")
    if alert_msg:
        msg = alert_msg
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

        print(s_email)
        print(s_password)
        
        if s_password == re_password:
            hashed_password = generate_password_hash(s_password, method='pbkdf2:sha256')
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (s_email, hashed_password))
            conn.commit()
            conn.close()
            session['email'] = s_email
            return redirect(url_for('signup', msg="Signed in successfully!"))
        else:
            return "Passwords do not match"
    return render_template('login.html', msg=msg)


@app.route('/dashboard')
def dash():
    email = session['email']
    print(email)
    conn = sqlite3.connect('database.db')
    if conn:
        print("connected")
    cursor = conn.cursor()
    cr = cursor.execute("SELECT * FROM jobs")
    print(cr)
    jobs = cursor.fetchall()
    conn.close()
    print(jobs)
    job_count = len(jobs)
    return render_template('user-dash.html', count=job_count, jobs=jobs)

@app.route('/user/details')
def job_details():
    id = request.args.get('id')
    email = session['email']
    print(email)
    conn = sqlite3.connect('database.db')
    if conn:
        print("connected")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs where id="+id)
    jobs = cursor.fetchone()
    print(jobs[9])
    cursor.execute("SELECT * FROM company where email="+'"'+jobs[9]+'"')
    comp = cursor.fetchone()
    print(jobs)
    print(comp[3])
    conn.close()
    date_time = datetime.datetime.fromtimestamp(float(jobs[10]))
    formatted_date = date_time.strftime("%B %d, %Y")
    return render_template("job-single.html", company_name = comp[3], job = jobs, date = formatted_date)

@app.route('/user/apply')
def apply_job():
    id = request.args.get('id')
    email = session['email']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    tb_name="APPLIED_"+str(retrieve_current_user()[0])
    stat  = f"CREATE TABLE IF NOT EXISTS {tb_name}(id INTEGER,job_id text,time text)"
    cursor.execute(stat)
    conn.commit()

    stat = f"INSERT INTO {tb_name}(job_id,time) values (?,?)"
    cursor.execute(stat,(id,time.time()))
    conn.commit()
    conn.close()

    return redirect('/dashboard')

def retrieve_current_user():
    email = session['email']
    conn = sqlite3.connect('database.db')
    if conn:
        print("connected")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where email="+'"'+email+'"')
    user = cursor.fetchone()
    conn.close()
    return user




########################################################################

@app.route("/company/dashboard")
def company_dash():
    email = session['email']
    print(email)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE company_id = ?", (email,))
    jobs = cursor.fetchall()
    conn.close()
    print(jobs)
    job_count = len(jobs)
    return render_template("company-dash.html", jobs = jobs, count=job_count)  

@app.route('/company/posts')
def company_posts():
    return render_template('applicants.html')

@app.route("/company/posts/add",methods=['GET','POST'])
def company_add_post():

    if request.method == 'POST':
        category = request.form['category']
        region = request.form['region']
        type = request.form['job-type']
        desc = request.form['job-description']
        vacancy=request.form['vacancy']
        exp=request.form['experience']
        sal=request.form['salary']
        edu=request.form['education']
        time1 = time.time()
        c_id = session['email']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (category,region,type,desc,vacancy,exp,sal,edu,company_id,time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (category,region, type, desc, vacancy, exp, sal, edu, c_id, time1))
        conn.commit()
        conn.close()

    return render_template("company-posts.html")  

@app.route("/logout")
def logout():
    return "succussfully logout"



if __name__ == '__main__':
    app.run(debug=True)