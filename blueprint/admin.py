from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user
from operation.SQL_operation import MySQLHelper
from sql_connect import SQLConnector

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
helper = SQLConnector(database='crop', password='123456', host='localhost', user='root')


@admin_bp.route('/admin/manage-users')
def view_users():
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for('login'))

    users = helper.get_all_users()
    return render_template('admin/view_users.html', users=users)


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
