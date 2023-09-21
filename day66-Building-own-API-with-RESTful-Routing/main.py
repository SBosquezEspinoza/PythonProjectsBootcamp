from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route('/random', methods=["POST", "GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all() # to get a list instead of objects
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all', methods=["POST", "GET"])
def all_cafes():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()  # to get a list instead of objects
    cafes_dict = []
    for cafe in all_cafes:
        new_cafe = cafe.to_dict()
        cafes_dict.append(new_cafe)
    return jsonify(cafes=cafes_dict)


@app.route("/search", methods=["GET", "POST"])
def search_cafes():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

## HTTP POST - Create Record
@app.route('/add', methods=["GET","POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('has_toilet')),
        has_wifi=bool(request.form.get('has_wifi')),
        has_sockets=bool(request.form.get('has_sockets')),
        can_take_calls=bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price')
        )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"response": "Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>', methods=["PATCH"])
def update_price(cafe_id):
    #cafe_id = request.args.get('cafe_id')
    cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if cafe_to_update:
        cafe_to_update.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(response={"response": "Successfully updated the price cafe."}), 200
    else:
        return jsonify(response={"Not Found": "Not valid id."}), 404
## HTTP DELETE - Delete Record

@app.route('/report-closed/<cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    if cafe_to_delete:
        if request.args.get('api-key') == "TopSecretAPIKey":
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"response": "Successfully deleted cafe."}), 200
        else:
            return jsonify(response={"error": "Not allow."}), 403
    else:
        return jsonify(response={"Not Found": "Not valid id."}), 404

if __name__ == '__main__':
    app.run(debug=True)
