from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from sql_connect import SQLConnector

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
helper = SQLConnector(database='crop', password='123456', host='localhost', user='root')

from werkzeug.security import generate_password_hash

if not helper.sql_select('crop', None, {'phonenumber': '18266820170'}):
    # 用户信息
    username = 'admin_user'
    email = 'admin@example.com'
    # userid = 1
    phonenumber = 18266820170
    password = 'password'
    user_class = 'manage'
    history = None

    # 生成密码哈希
    hashed_password = generate_password_hash(password)

    # 插入新用户
    helper.sql_insert('crop', {"username": username, "email": email, "user_class": user_class,
                               "phonenumber": phonenumber, "password": hashed_password})

    print("New user added successfully.")


@admin_bp.route('/manage-users', methods=['GET', 'POST'])
def manage_users():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')

        if user_id:
            helper.sql_update("crop", {"username": username,
                                       "phonenumber": phone,
                                       "password": password},
                              {'userid': user_id})
            flash('用户信息已更新', 'success')
        else:
            helper.sql_insert('crop', {"username": username,
                                       "phonenumber":phone,
                                       "password": password})
            flash('新用户已添加', 'success')

        return redirect(url_for('admin_bp.manage_users'))

    users = helper.get_all_users()
    return render_template('admin/user.html', users=users)


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('login'))

    helper.sql_delete('crop', {'userid': user_id})
    flash('用户已删除', 'success')
    return redirect(url_for('admin_bp.manage_users'))


@admin_bp.route('/advice/add', methods=['GET', 'POST'])
def add_advice():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('login'))

    if request.method == 'POST':
        disease_name = request.form.get('disease_name')
        advice_content = request.form.get('advice_content')

        if helper.add_advice(disease_name, advice_content):
            return redirect(url_for('admin_bp.add_advice'))

    return render_template('admin/add_advice.html')
