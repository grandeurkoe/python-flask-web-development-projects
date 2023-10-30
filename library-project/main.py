from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
# Create new_library.db
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new_library.db"

# Create the extension
db = SQLAlchemy()

# Initialize the app with the extension.
db.init_app(app)


def retrieve_from_library():
    """Retrieves all books in the library database. Returns all books as a list."""
    with app.app_context():
        all_books = []
        all_records = db.session.execute(db.select(Book).order_by(Book.id)).scalars()
        for each_record in all_records:
            record = {
                "id": each_record.id,
                "title": each_record.title,
                "author": each_record.author,
                "rating": each_record.rating,
            }
            all_books.append(record)
    return all_books


# Create Table.
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


@app.route('/', methods=["GET", "POST"])
def home():
    # Uncomment this when you run this app for the first time.
    # with app.app_context():
    #     db.create_all()
    if request.args.get('id') is not None:
        with app.app_context():
            current_book = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
            db.session.delete(current_book)
            db.session.commit()
        return redirect(url_for('home'))
    else:
        all_books = retrieve_from_library()
        return render_template('index.html', all_books=all_books, length=len(all_books))


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        with app.app_context():
            new_book = Book(title=request.form['book_name'],
                            author=request.form['book_author'],
                            rating=request.form['book_rating'])
            db.session.add(new_book)
            db.session.commit()

        # print(all_books)
        return redirect(url_for('home'))
    else:
        return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == "GET":
        with app.app_context():
            current_book = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
        return render_template('update.html', book=current_book)
    else:
        with app.app_context():
            current_book = db.session.execute(db.select(Book).where(Book.id == request.args.get('id'))).scalar()
            current_book.rating = request.form['updated_rating']
            db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
