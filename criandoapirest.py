# -*- coding: utf-8 -*-
"""server.py

ATUALIZADO EM 12/04/2024 POR JOAO PAULO COELHO FURTADO

Original file is located at
    https://colab.research.google.com/drive/1__4k6tElSChgzSO0KQhPuE1wmQekYlIM
    
    Baseado em: https://nataniel-paiva.medium.com/cria%C3%A7%C3%A3o-de-uma-api-rest-com-python-76696d17bfb9
    
"""

#pip install flask flask-jsonpify flask-sqlalchemy flask-restful

from json import dumps

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import create_engine, text

db_connect = create_engine('sqlite:///exemplo.db')
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        #query = conn.execute("select * from user") 
        query = conn.execute(text("select * from user"))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        name = request.json['name']
        email = request.json['email']

        conn.execute(text("insert into user values(null, '{0}','{1}')".format(name, email)))
        
        conn.commit() # Salva as alterações no banco de dados

        query = conn.execute(text('select * from user order by id desc limit 1'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']

        conn.execute(text("update user set name ='" + str(name) +
                     "', email ='" + str(email) + "'  where id =%d " % int(id)))
        
        conn.commit() # Salva as alterações no banco de dados

        query = conn.execute(text("select * from user where id=%d " % int(id)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class UserById(Resource):
    def delete(self, id):
        conn = db_connect.connect()
        conn.execute(text("delete from user where id=%d " % int(id)))
        conn.commit() # Salva as alterações no banco de dados
        return {"status": "success"}

    def get(self, id):
        conn = db_connect.connect()
        #print(text("select * from user where id =%d " % int(id)))
        query = conn.execute(text("select * from user where id =%d " % int(id)))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

api.add_resource(Users, '/users') 
api.add_resource(UserById, '/users/<id>') 

if __name__ == '__main__':
    app.run()
    
    