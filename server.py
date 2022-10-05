from flask import Flask, render_template
from requests import get

app = Flask(__name__)

datapoint = 'https://api.npoint.io/a851943134af3d5f028a'
data = get(datapoint).json()


@app.route('/')
def homepage():
    return render_template('pages/index-list.html', blog_posts_data=data)


@app.route('/view_post/<puid>')
def view_post(puid: int):
    for post in data:
        if post['puid'] == puid:
            return render_template('pages/post.html', post_data=post)



app.run(debug=True)
