# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 10:35:19 2019

@author: JL
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        help="Every item needs a store id"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'Item not found'}, 404
        
# =============================================================================
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
# 
#         query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
#         cursor.execute(query, (name,))
# 
#         connection.commit()
#         connection.close()
# 
#         return {'message': 'Item deleted'}
# =============================================================================

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
# =============================================================================
#             try:
#                 updated_item.insert()
#             except:
#                 return {"message": "An error occurred inserting the item."}
# =============================================================================
        else:
            item.price = data['price']
# =============================================================================
#             try:
#                 updated_item.update()
#             except:
#                 raise
#                 return {"message": "An error occurred updating the item."}
# =============================================================================
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
# =============================================================================
#     def get(self):
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
# 
#         query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
#         result = cursor.execute(query)
#         items = []
#         for row in result:
#             items.append({'name': row[1], 'price': row[2]})
#         connection.close()
# 
#         return {'items': items}
# =============================================================================
