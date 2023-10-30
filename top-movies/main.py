import os
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

TMDB_AUTH_TOKEN = os.environ['TMDB_AUTH_TOKEN']
API_ENDPOINT = "https://api.themoviedb.org/3/search/movie"
IMAGE_URL = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
headers = {
    "accept": "application/json",
    "Authorization": TMDB_AUTH_TOKEN,
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# Configure the SQLite database, relative to app instance folder.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///top-movies.db"

# Create a db object using SQLAlchemy constructor.
db = SQLAlchemy()

# Initialize the app with the extension.
db.init_app(app)


# Define db.Model.
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String(500))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String(250))
    img_url = db.Column(db.String(500))


class UpdateMovieForm(FlaskForm):
    rating = FloatField(label="Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()], name="rating")
    review = StringField(label="Your Review", validators=[DataRequired()], name="review")
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()], name="title")
    submit_movie = SubmitField(label="Add Movie")


def receive_all_movies():
    """Retrieves all movies in the top-movies database. Returns all movies as a list."""
    with app.app_context():
        all_movies = []
        rank = 1
        all_records = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars()
        for each_record in all_records:
            each_record.ranking = rank
            db.session.commit()
            record = {
                "id": each_record.id,
                "title": each_record.title,
                "year": each_record.year,
                "description": each_record.description,
                "rating": each_record.rating,
                "ranking": each_record.ranking,
                "review": each_record.review,
                "img_url": each_record.img_url,
            }
            all_movies.append(record)
            rank += 1

        return all_movies


@app.route("/")
def home():
    # Uncomment this when you run this app for the first time.
    # with app.app_context():
    #     db.create_all()
    if request.args.get('id') is not None:
        with app.app_context():
            delete_movie = db.session.execute(db.select(Movie).where(Movie.id == request.args.get('id'))).scalar()
            db.session.delete(delete_movie)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        all_movies = receive_all_movies()
        return render_template("index.html", all_movies=all_movies, length=len(all_movies))


@app.route("/edit", methods=["GET", "POST"])
def edit_movie():
    form = UpdateMovieForm()
    if form.validate_on_submit():
        with app.app_context():
            update_movie = db.session.execute(db.select(Movie).where(Movie.id == request.args.get('id'))).scalar()
            update_movie.rating = request.form['rating']
            update_movie.review = request.form['review']
            db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template("edit.html", form=form)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        param = {
            "query": request.form['title']
        }
        tmdb_response = requests.get(url=API_ENDPOINT, headers=headers, params=param)
        tmdb_response.raise_for_status()
        tmdb_data = tmdb_response.json()
        return render_template("select.html", tmdb_data=tmdb_data['results'])
    else:
        if request.args.get("id") is not None:
            movie_response = requests.get(url=f"https://api.themoviedb.org/3/movie/{request.args.get('id')}",
                                          headers=headers)
            movie_response.raise_for_status()
            movie_data = movie_response.json()
            print(movie_data)
            with app.app_context():
                new_movie = Movie(title=movie_data["original_title"],
                                  year=int(movie_data["release_date"].split("-")[0]),
                                  description=movie_data["overview"],
                                  img_url=f"{IMAGE_URL}{movie_data['poster_path']}"
                                  )
                db.session.add(new_movie)
                db.session.commit()
                return redirect(url_for('edit_movie', id=new_movie.id))
        else:
            return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
