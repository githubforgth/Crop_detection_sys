import os
import base64
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_mail import Mail
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin import Admin
from ultralytics import YOLO
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import Config
from src.config import crop_disease
from ML import detect_pic
from blueprint.admin import admin_bp, helper
from user_model import User

app = Flask(__name__)
app.config.from_object(Config)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = 'your_secret_key'

mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
admin = Admin(app, template_mode='bootstrap3', name='Admin')

app.register_blueprint(admin_bp)

model = YOLO('./run/train1/train3/weights/best.pt')
sql_connect = helper


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def image_to_binary(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = base64.b64encode(image_file.read())
    return binary_data


def generate_random_filename():
    return str(uuid.uuid4())


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'blm'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/login_info', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')
    res = sql_connect.sql_select('crop', None, {'phonenumber': phone})
    print(res, password, phone)
    if res and check_password_hash(res[0]['password'], password):
        user = User.get(res[0]['userid'])
        login_user(user)
        session['phone'] = phone
        session['user_id'] = res[0]['userid']
        session['username'] = res[0]['username']
        return jsonify({"success": True, "message": "登陆成功"})
    else:
        return jsonify({"success": False, "message": "账号密码错误，请重试"}), 401


@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user.username, is_admin=current_user.is_admin)


@app.route("/predict", methods=["POST"])
@login_required
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
@login_required
def iframe():
    file_path = session.get("file_path")
    if file_path:
        predict_res = detect_pic(file_path, model)
        sql_connect.sql_insert('pic_history', {
            'pic_name': file_path,
            'user_id': int(session['user_id']),
            'timestamp': datetime.now(),
            'res': crop_disease[predict_res['class_name']],
            'acc': predict_res["class_prob"]
        })
        return render_template("iframe.html", file_path=file_path, detect_res=predict_res,
                               res=crop_disease[predict_res['class_name']], is_admin=current_user.is_admin)
    else:
        return jsonify({"error": "File path not found"})


@app.route("/mine")
@login_required
def mine():
    res = sql_connect.sql_select('crop', None, {'userid': session['user_id']})
    return render_template("mine.html",
                           username=current_user.username,
                           email=res[0]['email'] if res[0]['email'] else "email",
                           phone=res[0]['phonenumber'],
                           is_admin=current_user.is_admin
                           )


@app.route("/Change_info", methods=["POST"])
@login_required
def change_info():
    res = sql_connect.sql_select('crop', None, {'userid': session['user_id']})
    email = request.values.get("email")
    phone = request.values.get("phone")
    user_name = request.values.get("username")
    password = request.values.get("password")
    vercode = request.values.get("vercode")
    if phone != res[0]['phonenumber']:
        flash('手机号已存在，请确认输入的手机号是否是正确的', 'error')
        return redirect(url_for('mine'))
    hashed_password = generate_password_hash(password)
    data_to_update = {'email': email, 'phonenumber': phone, 'password': hashed_password, 'username': user_name}
    sql_connect.sql_update('crop', data_to_update, where={"phonenumber": phone})
    return jsonify({'state': '修改成功'})


@app.route("/history")
@login_required
def history():
    if 'user_id' in session:
        history_list = sql_connect.sql_select('pic_history', '*', {'user_id': session['user_id']})
        print(history_list)
        return render_template('history.html', username=current_user.username, history_list=history_list, is_admin=current_user.is_admin)
    else:
        return redirect(url_for('login_page'))


@app.route('/advice', methods=['GET', "POST"])
@login_required
def advice_search():
    if request.method == 'POST':
        disease_name = request.form.get('disease_name')
        res = sql_connect.sql_select('advice', None, {'title': disease_name})
        if res:
            return render_template('advice.html', disease_name=disease_name, context=res[0]['content'])
        else:
            return jsonify({"error": "Disease not found"}), 404
    else:
        return render_template('advice.html', is_admin=current_user.is_admin)


@app.route('/advice/<disease_name>', methods=['GET'])
@login_required
def advice(disease_name):
    res = sql_connect.sql_select('advice', None, {'title': disease_name})
    if res:
        return render_template('advice.html', disease_name=disease_name, context=res[0]['content'], is_admin=current_user.is_admin)
    else:
        return jsonify({"error": "Disease not found"}), 404


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password and confirm_password and password == confirm_password:
            if not sql_connect.sql_select('crop', None, {'phonenumber': phone}):
                hashed_password = generate_password_hash(password)
                sql_connect.sql_insert('crop',
                                       {'username': username, 'phonenumber': username, 'password': hashed_password})
                res = sql_connect.sql_select('crop', None, {'phonenumber': username, 'password': hashed_password})
                if res:
                    user = User.get(res[0]['userid'])
                    login_user(user)
                    session['phone'] = phone
                    session['user_id'] = res[0]['userid']
                    session['username'] = res[0]['username']
                    return redirect(url_for('index'))
            else:
                flash("账户已存在", 'danger')
        else:
            flash("两次输入密码不相同", 'danger')
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/search-advice', methods=['GET'])
@login_required
def search_advice():
    if not current_user.is_admin:
        return redirect(url_for('login_page'))

    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 20

    advices, total = helper.search_advices(query, page, per_page)
    return render_template('advice/search_advice.html', advices=advices, query=query, page=page, total=total, per_page=per_page, is_admin=current_user.is_admin)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
