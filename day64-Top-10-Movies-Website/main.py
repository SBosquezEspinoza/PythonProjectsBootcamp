from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-10-movies-collection.db"
# initialize the app with the extension
db.init_app(app)


class AddMovie(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField("Add Movie")


class MovieForm(FlaskForm):
    new_rating = StringField('Your Rating out of 10 e.g. 7.5', validators=[DataRequired()])
    new_review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField("Done")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie))
    all_movies = result.scalars()
    return render_template('index.html', movies=all_movies)


@app.route('/edit?<int:movie_id>', methods=["POST", "GET"])
def edit(movie_id):
    movie_form = MovieForm()
    movie = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    ##option1
    if movie_form.validate_on_submit():
        movie.rating = float(movie_form.new_rating.data)
        movie.review = movie_form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    # if request.method == "POST":
    #     movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    #     movie_to_update.rating = float(request.form['rating'])
    #     movie_to_update.review = request.form['review']
    #     db.session.commit()
    #     return redirect(url_for('home'))

    # or book_to_update = db.get_or_404(Movie, book_id)
    return render_template('edit.html', movie=movie, form=movie_form)


@app.route('/delete/<int:movie_id>')
def delete(movie_id):
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == movie_id)).scalar()
    # or movie_to_delete = db.get_or_404(Movie, book_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["POST", "GET"])
def add():
    form = AddMovie()
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
