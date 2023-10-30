from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length
from flask_bootstrap import Bootstrap5


# Define the LoginForm. The validators parameter accepts a List of validator Objects.
# DataRequired makes the two fields required fields, so the user must type something.
# Otherwise, an error will be generated.
# pip install email_validator to be able to use email validation.
class LoginForm(FlaskForm):
    # Validate if the Email is the right format.
    email = StringField(label="Email", validators=[Email()])
    # Validate if the Password is greater than or equals to 8.
    password = PasswordField(label="Password", validators=[Length(min=8)])
    button = SubmitField(label="Log In")


app = Flask(__name__)
# Set secret key for Flask app
app.secret_key = "this-is-our-secret"
# Initialize the Bootstrap5 class.
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # To validate the form and check if the form made a PUSH request, we use the validate_on_submit() function.
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    else:
        return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
