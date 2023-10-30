from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''
today = date.today()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# CREATE POST FORM
class PostForm(FlaskForm):
    blog_post_title = StringField(label="Blog Post Title", validators=[DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[DataRequired()])
    your_name = StringField(label="Your Name", validators=[DataRequired()])
    blog_image_url = StringField(label="Blog Image URL", validators=[URL()])
    blog_content = CKEditorField(label="Blog Content")
    submit_post = SubmitField(label="Submit Post")


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    """Get all blog posts from database. Return index page."""
    all_posts = db.session.execute(db.select(BlogPost))
    posts = all_posts.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<post_id>')
def show_post(post_id):
    """Get blog post by ID. Return post page."""
    current_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
    requested_post = current_post.scalar()
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    """Create new blog post. Return make-post page on GET request. Return index page on POST request."""
    form = PostForm()
    if form.validate_on_submit():
        with app.app_context():
            new_post = BlogPost(
                title=form.blog_post_title.data,
                subtitle=form.subtitle.data,
                date=today.strftime("%B %m, %Y"),
                body=form.blog_content.data,
                author=form.your_name.data,
                img_url=form.blog_image_url.data,
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('get_all_posts'))
    else:
        return render_template("make-post.html", form=form, heading="New Post")


@app.route("/edit-post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """Edit existing blog post by ID. Return make-post page on GET request. Return post page on POST request."""
    form = PostForm()
    if form.validate_on_submit():
        with app.app_context():
            current_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
            requested_post = current_post.scalar()
            requested_post.title = form.blog_post_title.data
            requested_post.subtitle = form.subtitle.data
            requested_post.body = form.blog_content.data
            requested_post.author = form.your_name.data
            requested_post.img_url = form.blog_image_url.data
            db.session.commit()
            return redirect(url_for('show_post', post_id=post_id))
    else:
        current_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
        requested_post = current_post.scalar()
        form.blog_post_title.data = requested_post.title
        form.subtitle.data = requested_post.subtitle
        form.blog_content.data = requested_post.body
        form.your_name.data = requested_post.author
        form.blog_image_url.data = requested_post.img_url
        return render_template("make-post.html", form=form, heading="Edit Post")


@app.route("/delete/<post_id>")
def delete_post(post_id):
    with app.app_context():
        """Delete existing blog post by ID. Return index page."""
        current_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id))
        requested_post = current_post.scalar()
        db.session.delete(requested_post)
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
    app.run(debug=True, port=5003)
