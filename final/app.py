from flask import Flask, render_template, jsonify
import random
from grip_strength_tester import read_input

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("main.html", title="Main", name="Charles Nix")

@app.route('/update_progress')
def get_progress():
    progress = read_input()
    return jsonify({'progress': progress})
