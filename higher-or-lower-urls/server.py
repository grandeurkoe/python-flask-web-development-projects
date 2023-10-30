from flask import Flask
from random import randint

CORRECT_NUMBER = randint(0, 9)

higher_lower_app = Flask(__name__)


@higher_lower_app.route("/")
def home():
    return (f"<h1>Guess a number between 0 and 9</h1>"
            f"<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>")


@higher_lower_app.route("/<int:guessed_number>")
def check_guess(guessed_number):
    # Check if guessed number is equal to the correct number.
    if guessed_number < CORRECT_NUMBER:
        return (f"<h1 style='color:red'>Too low, try again!</h1>"
                f"<img src='https://media0.giphy.com/media/TgmiJ4AZ3HSiIqpOj6/giphy.gif?cid"
                f"=ecf05e47vz4eyf5ddak37o6uooehicezvt54028mry7fi98l&ep=v1_gifs_search&rid=giphy.gif&ct=g'/>")
    elif guessed_number > CORRECT_NUMBER:
        return (f"<h1 style='color:purple'>Too high, try again!</h1>"
                f"<img src='https://media1.giphy.com/media/2cei8MJiL2OWga5XoC/giphy.gif?cid"
                f"=ecf05e475ax0e6qwkw9zvzy4hksetbpkpmalcit52vfshgbk&ep=v1_gifs_search&rid=giphy.gif&ct=g'/>")
    else:
        return (f"<h1 style='color:green'>You found me!</h1>"
                f"<img src='https://media0.giphy.com/media/naiba7cRbSjgrzJ9wa/giphy.gif?cid"
                f"=ecf05e47vu6w1yswj9wl1l8datfs8y0zh8yyr4wmsiteaouz&ep=v1_gifs_search&rid=giphy.gif&ct=g'/>")


if __name__ == "__main__":
    higher_lower_app.run(debug=True)
