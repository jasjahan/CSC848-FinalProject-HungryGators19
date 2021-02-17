from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
  return render_template("home.html")

@app.route("/Branden")
def Branden():
  return render_template("Branden.html")

@app.route("/Robert")
def Robert():
  return render_template("Robert.html")

@app.route("/Gurjot")
def Gurjot():
  return render_template("Gurjot.html")

@app.route("/Yongjian")
def Yongjian():
  return render_template("Yongjian.html")

@app.route("/Jasmine")
def Jasmine():
  return render_template("Jasmine.html")

@app.route("/TinThuZar")
def TinThuZar():
  return render_template("TinThuZar.html")

if __name__ == '__main__':
    app.run(debug=True)
