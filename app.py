from flask import Flask, render_template, url_for, jsonify
from Show_Area.client.camera import Camera
import os
import json

def get_images(tag):
    json_file = os.path.join("static","data",tag+".json")
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data["images"]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_image_paths')
def get_value():
    image_paths = get_images()
    return jsonify(image_paths)


if __name__ == "__main__":
    print("Hello")
    camera = Camera()
   
    camera.start_process()
    app.run(debug=False)
