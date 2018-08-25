#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 shady <shady@MrRobot.local>
#

"""
Flask app for Cloud Native Project
"""
from flask import Flask, request
from flask import jsonify, make_response, abort
import json
import sqlite3

app = Flask(__name__)

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    api_list = []

    cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        a_dict = {}
        a_dict['version'] = row[0]
        a_dict['buildtime'] = row[1]
        a_dict['methods'] = row[2]
        a_dict['links'] = row[3]
        api_list.append(a_dict)

    conn.close()
    return jsonify({'api_version': api_list}), 200

@app.route("/api/v1/users", methods=['GET'])
def get_users():
    return list_users()

def list_users():
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute('SELECT username, full_name, email, password, id from users')
    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['name'] = row[1]
        a_dict['email'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]

        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list': api_list})

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

def list_user(user_id):
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    data = cursor.fetchall()
    conn.close()
    if(len(data) != 0):
        user = {}
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id'] = data[0][4]
        return jsonify(user)
    else:
        abort(404)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Resource not found!'}), 404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json \
        or not 'username' in request.json \
        or not 'email' in request.json \
        or not 'password' in request.json:
        abort(400)
    user = {
        'username': request.json['username'],
        'email': request.json['email'],
        'name': request.json['name'],  
        'password': request.json['password'],
    }
    print(user)
    return jsonify({'status': add_user(user)})

def add_user(new_user):
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    api_list = []
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users where username=? or email=?', \
        (new_user['username'], new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute('INSERT INTO users (username, email, password, full_name) \
            values(?,?,?,?)', (new_user['username'], new_user['email'], new_user['email'], new_user['name']))
        conn.commit()
        conn.close()
        return True

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json \
        or not 'username' in request.json:
        abort(400)
    user = request.json['username']
    return jsonify({'status': del_user(user)}), 200

def del_user(username):
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where username=?", (username,))
    data = cursor.fetchall()
    if len(data) == 0:
        abort(404)
    else:
        cursor.execute('delete from users where username==?',(username,))
        conn.commit()
        return True
@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': upd_user(user)}), 200

def upd_user(user):
    conn = sqlite3.connect('./database.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users where id=?', (user['id'],))
    data = cursor.fetchall()
    print(data)
    if len(data) == 0:
        abort(404)
    else:
        key_list = user.keys()
        for i in key_list:
            if i != 'id':
                cursor.execute("""UPDATE users set {0}=? where id=?""".format(i), (user[i], user['id']))
                conn.commit()
        return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
