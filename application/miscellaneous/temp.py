from flask import Flask,render_template
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", content="Testing")

@app.route("/aboutus.html")
def about():
    return render_template("aboutus.html", content="Testing")

@app.route("/regowner.html")
def regowner():
    return render_template("regowner.html", content="Testing")

@app.route("/regdriver.html")
def regdriver():
    return render_template("regdriver.html", content="Testing")

@app.route("/regsf.html")
def regsf():
    return render_template("regsf.html", content="Testing")

@app.route("/loginsf.html")
def logsf():
    return render_template("loginsf.html", content="Testing")

@app.route("/jas.html")
def jas():
    return render_template("jas.html", content="Testing")




if __name__ == "__main__":
    app.run(debug=True)

