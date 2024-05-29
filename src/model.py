#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/4/14 下午3:48
# @Author : Gao_Taiheng
# @File : model.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/crop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Crop(db.Model):
    __tablename__ = 'crop'

    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    user_class = db.Column(db.Enum('user', 'manage'), nullable=False)
    history = db.Column(db.String, nullable=True)


class PicHistory(db.Model):
    __tablename__ = 'pic_history'

    pic_name = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('crop.userid'))
    timestamp = db.Column(db.TIMESTAMP, nullable=True)
    res = db.Column(db.String(255), nullable=True)
    acc = db.Column(db.String(20), nullable=True)

    user = db.relationship('Crop', backref='pic_histories')


@app.route('/data', methods=['GET'])
def get_data():
    crops = Crop.query.all()
    result = [{'userid': crop.userid, 'username': crop.username, 'email': crop.email} for crop in crops]
    return jsonify(result)


@app.route('/data', methods=['POST'])
def insert_data():
    data = request.get_json()
    new_crop = Crop(username=data['username'], email=data['email'], phonenumber=data['phonenumber'],
                    password=data['password'], user_class=data['user_class'])
    db.session.add(new_crop)
    db.session.commit()
    return jsonify({'message': 'Data inserted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
