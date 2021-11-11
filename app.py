import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request
# from tensorflow.keras.preprocessing.image import load_img
# from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__, template_folder='templates', static_folder='static')

class_names = ['Organic','Plastic','Recyclable']

# def get_model():
#     global model
#     model = load_model('saved_model/my_model')
#     print('Model loaded')

# def load_image(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_tensor = image.img_to_array(img)                    # (height, width, channels)
#     img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
#     img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
#     return img_tensor

# def prediction(img_path):
#     new_image = load_image(img_path)
#     pred = model.predict(new_image)
#     print(pred)
#     if len(pred[0]) > 1:
#         pred_class = class_names[tf.argmax(pred[0])]
#     else:
#         pred_class = class_names[int(tf.round(pred[0]))]
#     return pred_class


# get_model()

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/wastecheck", methods=['GET', 'POST'])
def wastecheck():
    return render_template('WasteCheck.html')

# @app.route("/predict", methods = ['GET','POST'])
# def predict():
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = file.filename
#         file_path = os.path.join(r'D:/PAL/CS/Github/webtech-hackreva/static/',filename)                       #slashes should be handeled properly
#         file.save(file_path)
#         product = prediction(file_path)
#         print(product)
#     return render_template('predict.html', product = product, user_image = file_path)            #file_path can or may used at the place of filename

if __name__ == "__main__":
    app.run(debug=True)