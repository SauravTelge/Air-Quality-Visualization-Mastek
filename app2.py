from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/map")
def home():
    return render_template("name.html" )

if __name__ == '__main__':
    app.run(debug=True)