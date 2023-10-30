from flask import Flask, render_template

name_card_app = Flask(__name__)


@name_card_app.route("/")
def name_card():
    return render_template("index.html")


if __name__ == "__main__":
    name_card_app.run(debug=True)
