import sqlite3
from flask_restful import Resource, reqparse
from models.item_model import ItemModel
from flask_jwt import jwt_required


class Item(Resource):
    
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every Item needs to have a Store!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'There exists no item with such name'}, 404


    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name) is not None:
            return {"Error": "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        # item = {'name': name, 'price': data['price']}

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # if ItemModel.find_by_name(name) is None:
        #     return {'message': 'There exists no item with such name'}, 400
        
        # connection, cursor = ItemModel.open_connection()
        # cursor.execute('DELETE FROM items WHERE name = ?', (name, ))

        # connection.commit()
        # connection.close()

        # return {'message': 'Item Removed'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}


    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # return {"items": list(map(lamdba x: x.json(), ItemModel.query.all()))}