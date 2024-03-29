# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:49:01 2019

@author: JL
"""

from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404
    
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
    
        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except:
            return {'message': 'An error while creating the store.'},500
        
        return store.json(), 201
    
    def delete(self,name):
        store = StoreModel.find_by_name(name)
        
        if store:
            store.delete_from_db()
            
        return {'message': 'Store deleted.'}, 200
    
class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}