from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Convert Cafe object to dictionary. Returns dictionary."""
        dictionary = {}
        # Loop through each column in the data record.
        for column in self.__table__.columns:
            # Create a new dictionary entry:
            # Key - Name of the column
            # Value - Value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Return homepage."""
    return render_template("index.html")


@app.route("/random")
def random_cafe():
    """Get random cafe data from the database. Return random cafe data as JSON"""
    # Pick cafe at random.
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafe_picked = choice(all_cafes)
    # Convert the cafe_picked data record to a dictionary of key-value pairs.
    return jsonify(cafe=cafe_picked.to_dict())


# HTTP GET - Read Record
@app.route("/all")
def all_cafe():
    """Get all cafe data from database. Return all cafe data as JSON."""
    result = db.session.execute(db.select(Cafe))
    cafe_list = result.scalars().all()
    for cafe_index in range(len(cafe_list)):
        cafe_list[cafe_index] = cafe_list[cafe_index].to_dict()
    return jsonify(cafes=cafe_list)


@app.route("/search")
def search_cafe():
    """Get cafe data by location. Return result as JSON."""
    query_location = request.args.get('loc')
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    cafe_list = result.scalars().all()
    if len(cafe_list) != 0:
        for cafe_index in range(len(cafe_list)):
            cafe_list[cafe_index] = cafe_list[cafe_index].to_dict()
        return jsonify(cafes=cafe_list)
    else:
        not_found = {"Not Found": "Sorry, we don't have a cafe at that location."}
        return jsonify(error=not_found)


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_cafe():
    """Add cafe data. Return result as JSON."""
    with app.app_context():
        new_cafe = Cafe(name=request.form['name'],
                        map_url=request.form['map_url'],
                        img_url=request.form['img_url'],
                        location=request.form['location'],
                        seats=request.form['seats'],
                        # Convert STRING TO INT type and then finally convert to BOOL.
                        has_toilet=bool(int(request.form['has_toilet'])),
                        has_wifi=bool(int(request.form['has_wifi'])),
                        has_sockets=bool(int(request.form['has_sockets'])),
                        can_take_calls=bool(int(request.form['can_take_calls'])),
                        coffee_price=request.form['coffee_price'],
                        )
        db.session.add(new_cafe)
        db.session.commit()
        success = {"success": "Successfully added the new cafe"}
        return jsonify(response=success)


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_cafe_price(cafe_id):
    """Update cafe data by ID. Return result as JSON."""
    with app.app_context():
        update_cafe = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if update_cafe:
            update_cafe.coffee_price = request.args.get('new_price')
            db.session.commit()
            return jsonify(success="Successfully updated the price.")
        else:
            not_found = {"Not Found": "Sorry, we don't have a cafe with that ID in the database."}
            return jsonify(error=not_found)


# HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    """Delete cafe data by ID. Return result as JSON."""
    with app.app_context():
        cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
        if request.args.get('api_key') == "TopSecretAPIKey":
            if cafe_to_delete:
                db.session.delete(cafe_to_delete)
                db.session.commit()
                return jsonify(success="Successfully deleted the cafe.")
            else:
                not_found = {"Not Found": "Sorry, we don't have a cafe with that ID in the database."}
                return jsonify(error=not_found)
        else:
            return jsonify(error="Sorry, that's not allowed. Make sure you have the correct_api_key.")


if __name__ == '__main__':
    app.run(debug=True)
