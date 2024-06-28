from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from sql_connect import SQLConnector
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
helper = SQLConnector(database='crop', password='123456', host='localhost', user='root')

# Add a default admin user if not exists
default_admin_phone = '18266820170'
if not helper.sql_select('crop', None, {'phonenumber': default_admin_phone}):
    username = 'admin_user'
    email = 'admin@example.com'
    phonenumber = default_admin_phone
    password = 'password'
    user_class = 'manage'

    hashed_password = generate_password_hash(password)

    helper.sql_insert('crop', {
        "username": username,
        "email": email,
        "user_class": user_class,
        "phonenumber": phonenumber,
        "password": hashed_password
    })
    print("New admin user added successfully.")


@admin_bp.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if not current_user.is_admin:
        return redirect(url_for('login_page'))

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')

        user_data = {
            "username": username,
            "phonenumber": phone,
            "password": generate_password_hash(password) if password else None
        }

        if user_id:
            helper.sql_update("crop", {k: v for k, v in user_data.items() if v is not None}, {'userid': user_id})
            flash('用户信息已更新', 'success')
        else:
            helper.sql_insert('crop', {k: v for k, v in user_data.items() if v is not None})
            flash('新用户已添加', 'success')

        return redirect(url_for('admin_bp.manage_users'))

    users = helper.get_all_users()
    return render_template('admin/user.html', users=users)


@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('login'))

    helper.sql_delete('crop', {'userid': user_id})
    flash('用户已删除', 'success')
    return redirect(url_for('admin_bp.manage_users'))


@admin_bp.route('/advice/add', methods=['GET', 'POST'])
@login_required
def add_advices():
    if not current_user.is_admin:
        return redirect(url_for('login'))

    if request.method == 'POST':
        disease_name = request.form.get('disease_name')
        advice_content = request.form.get('advice_content')

        if helper.add_advice(disease_name, advice_content):
            flash('建议已添加', 'success')
            return redirect(url_for('admin_bp.add_advices'))

    return render_template('admin/add_advice.html')
