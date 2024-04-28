from flask import Flask, render_template, jsonify
from ISStreamer.Streamer import Streamer
import random
from grip_strength_tester import read_input

streamer = Streamer(
    bucket_name="FT",
    bucket_key="UUNP4VCRQJV7",
    access_key="ist_e5y21RVgoiT_lMfkC1wgrb85Y_DtStmi"
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("main.html", title="Main", name="Charles Nix")

@app.route('/update_progress')
def get_progress():
    progress = read_input()
    streamer.log("FT", progress)
    streamer.flush()
    return jsonify({'progress': progress})
