from validate_email import validate_email
import string
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def is_valid_email(email):
    is_valid = validate_email(email_address=email,check_regex=True, check_mx=False)
    return is_valid


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userid") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def convert(num, curr):
    return f'{curr} {num}'

def convert_currency(t):
    if t == "USD":
        return '$'
    if t == "IR":
        return '₹'
    if t == "BMK":
        return 'K'
    if t == 'BR':
        return 'R$'
    if t == "EUR":
        return '€'

def good_password(key):
    c1 = False
    c2 = False
    c3 = False
    c4 = False
    for i in key:
        if i.isdigit():
            c1 = True
            break

    for i in key:
        if i.isalpha():
            c2 = True
            break
    if len(key) >= 8:
        c3 = True
    for i in key:
        if i.isupper():
            c4 = True

    if c1 == True and c2 == True and c3 == True and c4 == True:
        return True
    else:
        return False
        

