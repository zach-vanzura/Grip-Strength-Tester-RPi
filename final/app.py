from flask import Flask, render_template, jsonify
import random
from grip_strength_tester import read_input
import mysql.connector
import json
import datetime
import time
from flask import request

app = Flask(__name__)

credentials = json.load(open("credentials.json", "r"))

@app.route('/table', methods=['GET'])
def table():
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()

    cursor.execute("SELECT * FROM grip_log")
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return render_template("grip_table.html", data = data, name = 'Charles Nix')

@app.route("/", methods=["GET"])
def main():
    return render_template("main.html", title="Main", name="Charles Nix")

@app.route('/update_progress')
def get_progress():
    credentials = json.load(open("credentials.json", "r"))

    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )

    cursor = database.cursor()

    insert_sql = "INSERT INTO `grip_log` (`timestamp`, `name`, `progress`) VALUES (%s,%s,%s);"

    now = datetime.datetime.now()

    name = request.args.get('name', 'Default Name')
    
    progress = read_input()

    data = (now,name,progress)
    cursor.execute(insert_sql,data)

    database.commit()

    cursor.close()
    database.close()
    
    return jsonify({'progress': progress})
