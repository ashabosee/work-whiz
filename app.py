from flask import *
import time


app = Flask(__name__)



@app.route("/")
def home():
    mHead = "The Easiest Way To Get Your Dream Job"
    return render_template("index.html", ab = mHead )

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)