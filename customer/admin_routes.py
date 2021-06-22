import os
import pathlib
from customer import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from flask_login import login_user, current_user
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from customer.forms import RegisterForm, LoginForm, RequestResetForm, ResetPasswordForm
from customer.models import User, Seller, Credit
from flask_breadcrumbs import register_breadcrumb




@app.route("/admin")
def admin_home_page():
    return render_template('admin_layout.html')

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/orders")
def admin_orders_page():
    return render_template('admin_orders.html')

@app.route("/order/details")
def order_details():
    return render_template('order_details.html')

@app.route("/coupon")
def admin_coupon_page():
    return render_template('admin_coupon.html')

@app.route("/admin_topup")
def admin_topup_page():
    return render_template('admin_topup.html')
