from flask import Flask, render_template
import requests

app = Flask(__name__)
URL = 'https://api.npoint.io/eb6cd8a5d783f501ee7d'
response = requests.get(URL)
all_posts = response.json()


@app.route('/')
def home():
    return render_template('index.html', posts=all_posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/post/<int:post_id>')
def get_post(post_id):
    requested_post = None
    for post in all_posts:
        if post['id'] == post_id:
            requested_post = post
    return render_template('post.html', end_post=requested_post)


if __name__ == '__main__':
    app.run(debug=True)