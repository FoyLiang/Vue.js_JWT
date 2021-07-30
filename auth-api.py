import flask
import mysql.connector
from flask import request, jsonify
from flask_cors import CORS

import json
import ast

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def database_check(recive_data):
	msg = { "message": "success", "data": recive_data }
	mydb = mysql.connector.connect(
  	host="localhost",
  	user="root",
  	password="",
  	database="test"
	)
	
	mycursor = mydb.cursor()
	dict_data = ast.literal_eval(recive_data)
	sql = "INSERT INTO `user`(`first_name`, `last_name`, `password`, `email`) VALUES ('"+dict_data["first_name"]+"','"+dict_data["last_name"]+"','"+dict_data["password"]+"','"+dict_data["email"]+"')"
	mycursor.execute(sql)
	mydb.commit()

	print("SEND_DATA_SUCCESS")

	return msg
	
@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive (Foy_Test)</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/register', methods=['POST'])
def register():
	# print(request.json)
	recive_data = request.json
	recive_data = str(recive_data)

	dict_data = ast.literal_eval(recive_data)
	if dict_data["password"] != dict_data["password_confirm"]:
		return { "message": "Error", "data": "Password not match" }, 401
	else:
		return database_check(recive_data)

if __name__ == '__main__':
    app.run()
