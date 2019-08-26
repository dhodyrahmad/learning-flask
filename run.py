# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 11:17:07 2019

@author: JL
"""

from app import app
from db import db

db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()
