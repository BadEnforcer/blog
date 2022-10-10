from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


with app.app_context():
    db.create_all()


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = URLField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=db.session.query(BlogPost).all())


@app.route("/post/<int:index>")
def show_post(index):
    return render_template("post.html", post=db.session.query(BlogPost).filter_by(id=index).first())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route('/create-post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm()
    if request.method == 'GET':
        return render_template('make-post.html', form=form)

    if form.validate_on_submit():
        new_post = BlogPost(title=request.form.get('title'),
                            subtitle=request.form.get('subtitle'),
                            body=request.form.get('body'),
                            author=request.form.get('author'),
                            img_url=request.form.get('img_url'),
                            date=date.today().strftime("%B %d, %Y"))

        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for("get_all_posts"))


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # get post by ID
    post_to_update = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(title=post_to_update.title,
                               subtitle=post_to_update.subtitle,
                               body=post_to_update.body,
                               author=post_to_update.author,
                               img_url=post_to_update.img_url)

    if request.method == 'GET':
        return render_template('make-post.html', form=edit_form, page_type='edit', post=post_to_update)

    # on form validation
    if edit_form.validate_on_submit():
        with app.app_context():
            # Update post details
            post_to_update.title = edit_form.title.data
            post_to_update.subtitle = edit_form.subtitle.data
            post_to_update.body = edit_form.body.data
            post_to_update.author = edit_form.author.data
            post_to_update.img_url = edit_form.title.data
            # commit changes
            db.session.commit()
            return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(debug=True)
