import os
import requests
import tensorflow as tf
import numpy as np
import cv2
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename




app = Flask(__name__)

model = tf.keras.models.load_model("fashionMnist.h5") ## on appel le modell

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')

def predict(filename):
    image = tf.io.read_file(UPLOAD_FOLDER + "/" + filename)
    image = tf.io.decode_png(image, channels=1)
    image = tf.image.resize(image, [28, 28])

    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    prediction = model.predict(tf.reshape(image, [1, 28, 28]))

    return "Object Detected : {}".format(class_names[np.argmax(prediction[0])])







app.run(debug=True)
