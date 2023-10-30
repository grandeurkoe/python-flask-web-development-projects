from flask import Flask, render_template
import requests

POST_ENDPOINT = "https://api.npoint.io/eb6cd8a5d783f501ee7d"


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


@app.route("/contact")
def contact_page():
    """Returns Contact webpage."""
    return render_template("contact.html")


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
