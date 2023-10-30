from flask import Flask, render_template, request
import requests
import smtplib
import os

MY_EMAIL = "again.meowya@gmail.com"
MY_PASSWORD = os.environ['MY_PASSWORD']
POST_ENDPOINT = "https://api.npoint.io/eb6cd8a5d783f501ee7d"


def send_mail(message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="testing.meowya@gmail.com",
                            msg=f"Subject: Contact Form Message\n\n{message}")


def get_api_data():
    """Gets post data from npoint API. Returns API data as JSON."""
    response = requests.get(url=POST_ENDPOINT)
    response.raise_for_status()
    data = response.json()
    return data


app = Flask(__name__)


@app.route("/")
def home_page():
    """Returns homepage."""
    all_posts = get_api_data()
    return render_template("index.html", posts=all_posts)


@app.route("/about")
def about_page():
    """Returns About webpage."""
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    """Returns Contact webpage."""
    if request.method == "GET":
        message = "Contact Me"
        return render_template("contact.html", message=message)
    elif request.method == "POST":
        message = "Succesfully sent your message."
        actual_message = (f"Name: {request.form['name']}\nEmail: {request.form['email']}\n"
                          f"Phone Number: {request.form['phone']}\nMessage: {request.form['message']}")
        send_mail(actual_message)
        return render_template("contact.html", message=message)


@app.route("/post/<int:post_num>")
def get_post(post_num):
    """Returns Post webpage."""
    print(post_num)
    all_posts = get_api_data()
    for post in all_posts:
        if post['id'] == post_num:
            return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
