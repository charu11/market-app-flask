from flask import url_for
from customer.models import User
from customer import app, mail
from flask_mail import Message


def send_reset_email():
    token = User.get_reset_token()
    msg = Message('Password reset password', sender='noreply@demo.com', recipients=[User.email])
    msg.body = f'''
    to reset the password visit this link:
    { url_for('reset_token', token=token, _external=True) }
    
    if you do not request this mail simply ignore this mail and do not make any changes
    '''

