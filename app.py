import os
import numpy as np
import pandas as pd
from PIL import Image
import json
from flask import Flask, render_template, request, url_for, redirect, flash, session
# from db import get_products, get_connection
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
import random
# from model import get_model,load_image, prediction
app = Flask(__name__, template_folder='templates', static_folder='static')

# get_model()

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer) #in cents
    accid = db.Column(db.String(50))
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))

class AddProduct(FlaskForm):
    name = StringField('Name')
    price = IntegerField('Price')
    accid = StringField('Account ID')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are accepted.')])


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/knowmore", methods=['GET', 'POST'])
def knowmore():
    return render_template('knowmore.html')

@app.route("/wastecheck", methods=['GET', 'POST'])
def wastecheck():
    return render_template('WasteCheck.html')

# @app.route("/predict", methods = ['GET','POST'])
# def predict():
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = file.filename
#         file_path = os.path.join(r'D:/PAL/CS/Github/webtech-hackreva/images/',filename)                       #slashes should be handeled properly
#         file.save(file_path)
#         product = prediction(file_path)
#         print(product)
#         if product == 'Organic':
#             return render_template('paper.html', product = 'organic', image = filename)
#         elif product == 'Plastic':
#             return render_template('plastic.html', product = 'plastic', image = filename)
#         elif product == 'Recyclable':
#             return render_template('recyclable.html', product = 'recyclable', image = filename)

# @app.route('/donate')
# def index():
#     products = get_products()
#     return render_template('donate.html', products=products)

@app.route('/try', methods=['GET'])
def index():
    products = Product.query.all()
    return render_template('try.html', products=products)

@app.route('/admin', methods=['GET'])
def admin():
    products = Product.query.all()
    return render_template('admin/index.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()
    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))

        new_product = Product(name=form.name.data, price=form.price.data, accid=form.accid.data, description=form.description.data, image=image_url)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)

if __name__ == "__main__":
    manager.run()