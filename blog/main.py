from flask import Flask, render_template
import requests


def get_blog_data():
    """Gets blog data from npoint API."""
    blog_response = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391")
    blog_response.raise_for_status()
    blog_posts = blog_response.json()
    return blog_posts


app = Flask(__name__)


@app.route('/blog')
def home():
    """Returns My blog page."""
    blog_posts = get_blog_data()
    return render_template("index.html", posts=blog_posts)


@app.route('/post/<post_id>')
def post(post_id):
    """Displays each post based on the post_id. Returns post page."""
    blog_posts = get_blog_data()
    return render_template("post.html", post=blog_posts[int(post_id) - 1])


if __name__ == "__main__":
    app.run(debug=True)
