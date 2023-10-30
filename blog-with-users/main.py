from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''


# admin_only decorator to only allow admin exclusive access to certain functionalities.
def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.get_id() == "1":
            pass
        else:
            abort(code=403)
        return function(*args, **kwargs)

    return decorated_function


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# CONNECT TO DB
db = SQLAlchemy()
db.init_app(app)

# INITIALIZE GRAVATAR
gravatar = Gravatar(app)


# CONFIGURE TABLES
# BlogPost table
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.relationship("User", back_populates="posts")
    img_url = db.Column(db.String(250), nullable=False)
    comments = db.relationship('Comment', back_populates="parent_post")


# User table for all registered users.
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    posts = db.relationship('BlogPost', back_populates="author")
    comments = db.relationship('Comment', back_populates="author")


# Comment table for all registered users.
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    parent_post = db.relationship('BlogPost', back_populates="comments")
    text = db.Column(db.Text)


with app.app_context():
    db.create_all()


# Create a user_loader callback.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=["GET", "POST"])
def register():
    """
    Register new user.
    Return register page on GET request.
    Return login page if user already exists on POST request.
    Return index page if user doesn't exist on POST request.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user is None:
            new_user = User(
                email=form.email.data,
                password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8),
                name=form.name.data,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('get_all_posts'))
        else:
            flash(message="You've already signed up with that email, login instead!")
            return redirect(url_for('login'))
    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Login existing user.
    Return login page on GET request.
    Return index page on POST request.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user is not None:
            if check_password_hash(pwhash=user.password, password=form.password.data):
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash(message="Password incorrect, please try again.")
                return redirect(url_for('login'))
        else:
            flash(message="That email does not exist, please try again.")
            return redirect(url_for('login'))
    else:
        return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Log out user.
    Return index page.
    """
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    """
    Gets all blog post.
    Return index page.
    """
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# Allow logged-in users to comment on posts.
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    """
    Show blog post by post ID.
    Return post page on GET request.
    Return login page if user isn't active on POST request.
    Return post page if user is active on POST request.
    """
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_active:
            flash(message="You need to login or register to comment.")
            return redirect(url_for('login'))
        else:
            post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
            with app.app_context():
                new_comment = Comment(
                    author_id=current_user.id,
                    post_id=post.author.id,
                    text=form.comment.data
                )
                db.session.add(new_comment)
                db.session.commit()
                return redirect(url_for('show_post', post_id=post_id))
    else:
        requested_post = db.get_or_404(BlogPost, post_id)
        return render_template("post.html", post=requested_post, form=form)


# Only allow admin user to create new posts.
@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    """
    Add new blog post.
    Return make-post page on GET request.
    Return index page on POST request.
    """
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# Only allow admin user to edit posts.
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    """
    Edit blog post by post ID.
    Return make-post page on GET request.
    Return post page on POST request.
    """
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# Only allow admin user to delete posts.
@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    """
    Delete blog post by post ID.
    Return index page.
    """
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    """Return about page."""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Return contact page."""
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
