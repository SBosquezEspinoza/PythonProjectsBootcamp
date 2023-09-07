import requests
from flask import Flask, render_template
import datetime
app = Flask(__name__)

##FOR RENDER HTML FILES WE NEED TO IMPORT render_template
# and create a folder called templates, for images and more we need STATIC FOLDER
##  ALWAYS STATIC AND TEMPLATES FOLDERS

##To be able to see the style of our website we need to create a <link> and add the relationship as
# rel='stylesheet' and href= wherever is located, must be added in html files in head

#Si descargamos una pagina web de acceso gratuito y anadimos en inspect en google chrome "" document.body.contentEditable=true"
#podemos editarlo sin tener que volver al html
#no se guarda cuando se refresca, save the html and move to your templates

##for APIS

## URL building with flask in html files we can reference another html file to redirect them
## <a href= " {{url_for('name of the function to reference', send variables same way name=3 that will be send it as <num> en route(/..) }} > link </a>

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/guess/<name>')
def guess(name):
    gender_url = f'https://api.genderize.io?name={name}'
    gender_response = requests.get(gender_url)
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    age_url = f'https://api.agify.io?name={name}'
    age_response = requests.get(age_url)
    age_data = age_response.json()
    age = age_data["age"]
    return render_template('guess.html', name=name, gender=gender, age=age)


@app.route('/blog')
def blog():
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template('blog.html', all_posts=all_posts)


if __name__ == '__main__':
    app.run(debug=True)
