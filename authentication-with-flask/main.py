from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONFIGURE FLASK LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
# To generate your own strong secret key type the following in Windows Powershell
# $ python -c 'import secrets; print(secrets.token_hex())'
app.secret_key = "7ea16e427bee0c520c783b9d5515251c918575c7c780002c873836a338f2dccc"

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


# CREATE A USER_LOADER CALLBACK
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    """Return index page."""
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Register new user. 
    Return login page on GET request.
    Display flash message. Return login page if user already exists on POST request.
    Return secret page on user creation on POST request.
    """
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form.get("email"))).scalar()
        if user is None:
            with app.app_context():
                new_user = User(
                    email=request.form.get("email"),
                    password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256',
                                                    salt_length=8),
                    name=request.form.get("name"),
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('secret_page'))
        else:
            flash(message="You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Login user.
    Return login page on GET request.
    Return secret page if user exist on POST request.
    Display flash message. Return login page if user doesn't exist on POST request.
    Display flash message. Return login page if password doesn't match on POST request.
    """
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
        if user is not None:
            if check_password_hash(pwhash=user.password, password=request.form.get('password')):
                login_user(user)
                return redirect(url_for('secret_page'))
            else:
                flash(message="Password incorrect, please try again.")
                return redirect(url_for('login'))
        else:
            flash(message="That email does not exist, please try again.")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


@app.route('/secrets', methods=["GET", "POST"])
@login_required
def secret_page():
    """Return secret page if user is logged in."""
    return render_template('secrets.html')


@app.route('/logout')
@login_required
def logout():
    """Log user out. Return index page if user is logged in."""
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    """Download cheat sheet. Return cheat_sheet.pdf."""
    name = "files/cheat_sheet.pdf"
    return send_from_directory(app.static_folder, name)


if __name__ == "__main__":
    app.run(debug=True)
