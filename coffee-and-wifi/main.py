from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

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
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


def get_cafe_data():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return list_of_rows


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = URLField(label='Cafe location on Google Maps (URL)', validators=[URL()])
    open_time = StringField(label='Opening Time e.g. 8:00 AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g. 5:30 PM', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi_rating = SelectField(label='Wi-Fi Strength Rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    socket_availability = SelectField(label='Power Socket Availability',
                                      choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField(label='Submit')


# All Flask routes below.
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    # Validate form data on clicking Submit button.
    if form.validate_on_submit():
        new_cafe = [form.cafe.data, form.location.data, form.open_time.data, form.close_time.data,
                    form.coffee_rating.data, form.wifi_rating.data, form.socket_availability.data]
        # Append new cafe details to cafe-data.csv
        with open(file='cafe-data.csv', encoding='utf-8', mode="a", newline='') as read_form:
            form_writer = csv.writer(read_form)
            form_writer.writerow(new_cafe)
            read_form.close()
        return redirect(url_for('cafes'))
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    all_cafes = get_cafe_data()
    return render_template('cafes.html', cafes=all_cafes)


if __name__ == '__main__':
    app.run(debug=True)
