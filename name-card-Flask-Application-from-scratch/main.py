import requests
from flask import Flask, render_template

app = Flask(__name__)

##FOR RENDER HTML FILES WE NEED TO IMPORT render_template
# and create a folder called template, for images and more we need STATIC FOLDER
##  ALWAYS STATIC AND TEMPLATES FOLDERS

##To be able to see the style of our website we need to create a <link> and add the relationship as
# rel='stylesheet' and href= wherever is located, must be added in html files in head

#Si descargamos una pagina web de acceso gratuito y anadimos en inspect en google chrome "" document.body.contentEditable=true"
#podemos editarlo sin tener que volver al html
#no se guarda cuando se refresca, save the html and move to your templates

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
