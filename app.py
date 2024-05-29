import os
import base64
import uuid

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_admin import Admin
from ultralytics import YOLO
from flask_mail import Mail
from datetime import datetime

from config import Config
from ML import detect_pic
from sql_connect import SQLConnector

app = Flask(__name__)
mail = Mail(app)
app.config.from_object(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='admin', template_mode='bootstrap3')

model = YOLO('./run/train1/train3/weights/best.pt')
table_name = 'crop'
sql_connect = SQLConnector(database='crop', password='123456', host='localhost', user='root')


def image_to_binary(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = base64.b64encode(image_file.read())
    return binary_data


def generate_random_filename():
    random_filename = str(uuid.uuid4())
    return random_filename


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'.png', 'jpg', 'jpeg', 'blm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login_info', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')

    res = sql_connect.sql_select(table_name, None, {'phonenumber': phone, 'password': password})
    if res:
        session['phone'] = phone
        session['user_id'] = res[0][2]
        session['username'] = res[0][0]
        return redirect(url_for('index'))
    else:
        return jsonify({'message': '账号或密码输入错误'}), 401
        # return '<script> alert("账号或密码输入错误");window.open(127.0.0.1:5000/login);;</script>'


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html', username=session['username'])


@app.route("/predict", methods=["POST"])
def predict_picture():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "Please upload file"})

    if file and allowed_file(file.filename):
        filename = generate_random_filename() + "." + file.filename.split('.')[-1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        session["file_path"] = file_path
        try:
            return jsonify({"message": "Upload successful"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "Invalid file format"})


@app.route("/iframe", methods=["GET", "POST"])
def iframe():
    file_path = session.get("file_path")
    if file_path:
        predict_res = detect_pic(file_path, model)
        sql_connect.sql_insert('pic_history', {'pic_name': file_path, 'user_id': int(session['user_id']),
                                               'timestamp': datetime.now(), 'res': predict_res['class_name'],
                                               'acc': predict_res["class_prob"]})
        return render_template("iframe.html", file_path=file_path, detect_res=predict_res)
    else:
        return jsonify({"error": "File path not found"})


@app.route("/mine")
def mine():
    return render_template("mine.html", username=session.get('username'))


@app.route("/Change_info", methods=["POST"])
def change_info():
    email = request.values.get("email")
    phone = request.values.get("phone")
    password = request.values.get("password")
    vercode = request.values.get("vercode")

    data_to_update = {'email': email, 'phonenumber': phone, 'password': password}
    sql_connect.sql_update(table_name, data_to_update, where={"phonenumber": phone})
    return jsonify({'state': 'Alter success'})


@app.route("/user/admin")
def admin_page():
    return render_template("admin.html", username=session.get('username'))


@app.route("/suggest")
def suggest():
    pass
    return ""


@app.route("/history")
def history():
    if 'user_id' in session:
        history_list = sql_connect.sql_select('pic_history', '*', {'user_id': session['user_id']})
        return render_template('history.html', username=session['username'], history_list=history_list)
    else:
        return redirect(url_for('login_page'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            sql_connect.sql_insert('crop', {'phonenumber': username, 'password': password, "username": 'Web 用户'})
            res = sql_connect.sql_select(table_name, None, {'phonenumber': username, 'password': password})
            if res:
                session['phone'] = username
                session['user_id'] = res[0][2]
                session['username'] = res[0][0]
                return redirect(url_for('index'))
        return render_template('signup.html', error="Passwords do not match")
    return render_template('signup.html')


@app.route('/logout')
def logout():
    # 清除会话信息
    session.pop('username', None)
    session.pop('user_id', None)
    session.pop('phone', None)
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
