import os
import pathlib
from customer import app, db, bcrypt, mail
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, current_user
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from customer.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from customer.models import User, Seller, Credit
from flask_breadcrumbs import register_breadcrumb
from customer.utils import send_reset_email

@app.route('/')
@app.route('/home')
def home_page():
    return redirect(url_for('login_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        print(username, email, password1, password2)

        user_mail = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username)
        print(user_mail and user_name)
        if password1 != password2:
            flash('passwords do not match. please enter valid password')
            return redirect(url_for('register_page'))

        if user_mail and user_name:
            flash('Email address already exists.')
            return redirect(url_for('register_page'))

        else:

            new_user = User(username=username, email=email, password_hash=password1)
            db.session.add(new_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()

            flash(f'Account created Successfully...!  now please login to continue', category='success')
            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Login success... You are Logged in as {attempted_user.username}', category='success')
            return redirect(url_for('topup_page'))
        else:
            flash('User name and password do not match. please check your customer name and password',
                  category='danger')

    return render_template('login.html', form=form, current_user=current_user)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password_page():
    if request.method == 'POST':
        user = current_user
        new_password = request.form.get('new_password')
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        print(hashed_password)
        user.password = hashed_password
        db.session.commit()
        flash('password has been updated successfully')
        return redirect(url_for('login_page'))
    return render_template('change_password.html')


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('topup_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login_page'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('topup_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login_page'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forget_password_page():
    return 'forget pasword'


@app.route('/topup', methods=['GET', 'POST'])
def topup_page():
    return render_template('topup.html')


@app.route('/account_manage', methods=['GET', 'POST'])
def account_manage_page():
    return render_template('account_manage.html', user=current_user)


@app.route('/credit_topup', methods=['GET', 'POST'])
def credit_top_up_page():
    credit = Credit.query.filter_by(id=current_user.id)

    print(current_user.id)
    return render_template('credit_topup.html', user=current_user,  credits=credit)


@app.route('/topup_record', methods=['GET', 'POST'])
def topup_record_page():

    return render_template('topup_records.html', current_user=current_user)


@app.route('/faq', methods=['GET', 'POST'])
def faq_page():
    return render_template('faq.html')


@app.route('/asin_report')
def asin_report_page():
    sellers = Seller.query.all()
    return render_template('asin_report.html', sellers=sellers)


@app.route('/ppc_report')
def ppc_report_page():
    return render_template('ppc_report.html')


@app.route('/video_upload')
def video_upload_page():
    return render_template('video_upload.html')


@app.route('/add_content')
def add_content_page():
    return render_template('add_A_content.html')


@app.route('/review_page')
def review_page():
    return render_template('review_page.html')


@app.route('/review_lookup')
def review_lookup_page():
    return render_template('review_lookup.html')
