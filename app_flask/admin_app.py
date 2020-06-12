#!/usr/bin/env python3
"""
The flow to investor
"""
from flask import (
    Blueprint, render_template,
    session, redirect,
    url_for, request)
from datetime import datetime

admin = Blueprint("admin", __name__)

@admin.route("/", methods=['GET', 'POST'])
@admin.route("/login", methods=['GET', 'POST'])
def admin_login():
    """Logic for admin"""
    from models.admin import Admin

    if 'admin-session' in session:
        return redirect(url_for('home'))

    elif request.method == "POST":

        username = request.form['username']
        password = request.form["password"]

        md5PwdConfirm = md5(password.encode('utf-8')).hexdigest()
        userLog = Admin.query.filter_by(username=username).first()

        params = [username, password]

        for n in params:
            if len(n) is 0:
                return render_template("login_admin.html", error_fill=True)
        try:
            if userLog.pwd == md5PwdConfirm:
                session['admin-session'] = username
                return redirect(url_for("new_debts"))

            return render_template("login_admin.html", error_pwd=True)
        
        except:
            return render_template("login_admin.html", error_pwd=True)

    return render_template("login_admin.html")


@admin.route("/register", methods=['GET', 'POST'])
def admin_register():
    """
    Easy register of a new admin.
    Beta system
    """
    from models.admin import Admin

    if "admin-session" in session:
        redirect(url_for("new_debts"))

    if request.method == "POST":
        names = request.form["names"]
        last_names = request.form["lastNames"]
        username = request.form["email"]
        password = request.form["password"]

        params = [names, last_names, username, password]

        for n in params:
            if len(n) == 0:
                return render_template("register_admin.html", error_params=True)

        allAdmins = [admin.username for admin in Admin.query.all()]

        if username in allAdmins:
            return render_template("register_admin.html", error_exist=True)

        else:
            md5Pwd = md5(password.encode('utf-8')).hexdigest()
            try:
                newAdmin = Admin(names, last_names, username, md5Pwd)
            except:
                return render_template("register_admin.html", error_data=True)

            newAdmin.save()
            session['admin-session'] = username
            return redirect(url_for("new_debts"))

    return render_template("register_admin.html")


@admin.route("/new_debts", methods=['GET', 'POST'])
def new_debts():
    """All postulations debts"""
    from models.debt import Debt

    if "admin-username" in session:
        return "Prueba exitosa para admin"

    redirect(url_for("admin_login"))