from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    print("Creating-----------------------")
    print(data.to_dict())
    name = data.get('name')
    price = float(data.get('price'))  
    bakery_id = int(data.get('bakery_id'))

    bakery = Bakery.query.get(bakery_id)
    if bakery:
        new_baked_good = BakedGood(name=name, price=price, bakery=bakery)
        db.session.add(new_baked_good)
        db.session.commit()

        return make_response(new_baked_good.to_dict(), 201) 
    else:
        return make_response({'message': 'Bakery not found'}, 404)


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.form
    new_name = data.get('name')

    bakery = Bakery.query.get(id)
    if bakery:
        if new_name:
            bakery.name = new_name

        db.session.commit()
        return make_response(bakery.to_dict(), 200) 
    else:
        return make_response({'message': 'Bakery not found'}, 404)


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({'message': 'Baked good deleted successfully'}, 200)  # HTTP 200 OK
    else:
        return make_response({'message': 'Baked good not found'}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
