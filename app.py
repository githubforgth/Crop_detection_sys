from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from ultralytics import YOLO
from ML import detect_pic
import os
import sql_connect
import base64
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = 'gth'  # 设置一个安全密钥
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# UPLOAD CONFIG
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = YOLO('./ML/runs/classify/train21/weights/best.pt')
table_name = 'crop'


def image_to_binary(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = base64.b64encode(image_file.read())
    return binary_data


def generate_random_filename():
    # 使用uuid模块生成随机字符串作为文件名
    random_filename = str(uuid.uuid4())
    return random_filename


def allowed_file(filename):
    # RULE of file upload
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login_info', methods=['POST'])
def login():
    # 假设你从表单中获取了用户ID，用user_id代替
    phone = request.form.get('phone')
    password = request.form.get('password')
    # 存储用户ID在session中

    res = sql_connect.sql_select(table_name, None, {'phonenumber': phone, 'password': password})
    if res != ():
        # 其他逻辑，比如跳转到用户的个人页面
        session['phone'] = phone
        session['user_id'] = res[0][2]
        session['username'] = res[0][0]
        print(session)
        return redirect(url_for('index'))
    else:
        return '<script> alert("账号或密码输入错误");window.open(127.0.0.1:5000/login);;</script>'


@app.route('/')
def index():
    # THE ROOT OF WEBSITE
    try:
        return render_template('index.html', username=session['username'])
    except KeyError:
        return redirect(url_for('login_page'))


@app.route("/predict", methods=["POST", "GET"])
def predict_picture():
    # UPLOAD FILE (THE FUNCTION NAME HAVE SOME TROUBLE)
    if "file" not in request.files:
        return jsonify({"error": "No file provided"})

    file = request.files['file']
    if file.filename == "":
        return render_template("error.html", error="Please upload file")

    if file and allowed_file(file.filename):
        filename = generate_random_filename() + "." + file.filename.split('.')[-1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        session["file_path"] = file_path
        print(session.get('file_path'))
        try:
            return jsonify({
                "message": "Upload successful",
            })
        except Exception as e:
            return render_template("error.html", error=str(e))
    else:
        return render_template("error.html", error="Invalid file format")


# 使用iframe
@app.route("/iframe", methods=["GET", "POST"])
def iframe():
    # THE INDEX IFRAME, SHOW THE RESULT OF DETECT.
    file_path = session["file_path"]
    print(file_path)
    predict_res = detect_pic(file_path, model)
    sql_connect.sql_insert('pic_history', {'pic_name': file_path, 'user_id': int(session['user_id']), 'timestamp': datetime.now(), 'res': predict_res['class_name'], 'acc': predict_res["class_prob"]})
    print("Upload success!")
    return render_template("iframe.html", file_path=file_path, detect_res=predict_res)


@app.route("/mine")  # 我的
def mine():
    # SHOW MINE
    return render_template("mine.html", username=session['username'])


@app.route("/Change_info", methods=["POST"])
def Change_info():
    email = request.values["email"]
    phone = request.values["phone"]
    password = request.values["password"]
    vercode = request.values["vercode"]
    # ['username', 'email', 'userid', 'phonenumber', 'password', 'user_class', 'history']
    data_to_update = {'email': email, 'phonenumber': phone, 'password': password}

    sql_connect.sql_update(table_name, data_to_update, where={"phonenumber": phone})
    return jsonify({'state': 'Alter success'})


@app.route("/admin")
def admin():
    return render_template("admin.html", username=session['username'])


@app.route("/suggest")
def suggest():
    pass
    return ""


@app.route("/history")
def history():
    history_list = sql_connect.sql_select('pic_history', '*', {'user_id': session['user_id']})
    return render_template('history.html', username=session['username'], history_list = history_list)


@app.route('/signup')
def signup():
    username = request.args.get('username')
    password = request.args.get('password')
    confirm_password = request.args.get('confirm_password')
    if (password and confirm_password) and password == confirm_password:
        sql_connect.sql_insert('crop', {'phonenumber': username, 'password': password, "username": 'Web 用户'})
        res = sql_connect.sql_select(table_name, None, {'phonenumber': phone, 'password': password})
        if res != ():
            # 其他逻辑，比如跳转到用户的个人页面
            session['phone'] = username
            session['user_id'] = res[0][2]
            session['username'] = res[0][0]
        return redirect(url_for('index'))
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
