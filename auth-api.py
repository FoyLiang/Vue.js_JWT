from re import split
import flask
import mysql.connector
from flask import request, jsonify
from flask_cors import CORS

import json
import ast
import jwt
import time

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def database_regis(recive_data):
	msg = { "message": "success", "data": recive_data }
	mydb = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	password="",
  	database="vue-db"
	)

	mycursor = mydb.cursor()
	dict_data = ast.literal_eval(recive_data)
	sql = "INSERT INTO `user`(`first_name`, `last_name`, `password`, `email`) VALUES ('"+dict_data["first_name"]+"','"+dict_data["last_name"]+"','"+dict_data["password"]+"','"+dict_data["email"]+"')"
	mycursor.execute(sql)
	mydb.commit()

	print("SEND_DATA_SUCCESS")

	return msg

def database_login(recive_data):
	recive_data = str(recive_data)
	mydb = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	password="",
  	database="vue-db"
	)

	mycursor = mydb.cursor()
	dict_data = ast.literal_eval(recive_data)
	sql = "SELECT * FROM `user` WHERE `email`=\""+dict_data["email"]+"\" and `password`=\""+dict_data["password"]+"\""
	mycursor.execute(sql)
	results = mycursor.fetchall()
	mydb.commit()

	if results == []:
		return { "message": "Error", "data": "Wrong email or password" }, 401
	else:
		tuple_data = results[0]
		nid, first, last, pasw, mail = tuple_data
		timeexp = int(time.time())+300
		str_payload = "{\"ID\": \""+str(nid)+"\",\"first_name\": \""+str(first)+"\",\"last_name\": \""+str(last)+"\",\"email\": \""+str(mail)+"\",\"exp\":\""+str(timeexp)+"\"}"
		json_payload = json.loads(str_payload)	
		encoded_jwt = jwt.encode(json_payload, "secret", algorithm="HS256")
		
		return { "message": "success", "token": encoded_jwt }


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive (Foy_Test)</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/login', methods=['POST'])
def login():
	# print(request.json)
	recive_data = request.json

	return database_login(recive_data)

@app.route('/register', methods=['POST'])
def register():
	# print(request.json)
	recive_data = request.json
	recive_data = str(recive_data)

	dict_data = ast.literal_eval(recive_data)
	if dict_data["password"] != dict_data["password_confirm"]:
		return { "message": "Error", "data": "Password not match" }, 401
	else:
		return database_regis(recive_data)

@app.route('/user', methods=['GET'])
def user():
	str_token = request.headers.get('Authorization')
	l_token = str_token.split(' ')
	token = l_token[1]
	if token == 'null':
		return { "message": "Error", "data": "No Data" }, 401
	else:
		de_jwt = jwt.decode(token, "secret", algorithms="HS256")
		str_data = str(de_jwt)
		data = str_data.replace("'", '"')
		jason_data = json.loads(data)	
		return jason_data

if __name__ == '__main__':
    app.run()
