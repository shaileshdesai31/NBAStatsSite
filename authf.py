from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from flask_login import login_user, logout_user, current_user, login_required
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    data = request.form
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Credentials', category='error')
        else:
            flash('Invalid Credentials', category='error')




    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=["GET"])
def sign_up():
    return render_template("sign_up.html", user=current_user)


"""email = request.form.get('email')
        password = request.form.get('password')

        conn = mysql.connector.connect(user='root', password='169lssms$Ybd484',
                                       host='127.0.0.1',
                                       database='nba')
        cur = conn.cursor(buffered=True)
        q = f"SELECT email, password FROM User u where u.email = '{email}'"
        cur.execute(q)
        result = cur.fetchall()
        print(result)
        if len(result) == 0:
            flash('Invalid Email-Password Combination', category='error')
        else:
            email_db = result[0][0]
            password_db = result[0][1]
            if check_password_hash(pwhash=password_db, password=password):
                flash('Login Successful', category='success')
                login_user()
            else:
                flash('Invalid Email-Password Combination', category='error')"""
