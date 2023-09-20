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
#API for movies## your api key
MOVIE_DB_API_KEY = "Your secret API"

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
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
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

    if form.validate_on_submit():
        title_movie = form.title.data
        # URL = f"https://api.themoviedb.org/3/search/movie?query={title_movie}&include_adult=false&language=en-US&page=1"
        # headers = {
        #     "accept": "application/json",
        #     "Authorization": "login in account to get it"
        # }
        #movies = requests.get(URL, headers=headers).json()["results"]
        MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
        movies = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": title_movie}).json()["results"]
        return render_template("select.html", movies=movies)

    return render_template('add.html', form=form)

@app.route('/find/<int:movie_id>')
def find(movie_id):
    MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
    URL = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(URL, params={"api_key": MOVIE_DB_API_KEY}).json()
    print(response)
    new_movie = Movie(title=response["title"],
                      img_url=f"{MOVIE_DB_IMAGE_URL}/{response['poster_path']}",
                      year=response['release_date'].split('-')[0],
                      description=response['overview'])
    db.session.add(new_movie)
    db.session.commit()
    movie = db.session.execute(db.select(Movie).where(Movie.title == response['title'])).scalar()
    return redirect(url_for('edit', movie_id=movie.id))


if __name__ == '__main__':
    app.run(debug=True)
