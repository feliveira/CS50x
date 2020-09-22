import string
import os
from functools import wraps
from re import fullmatch
import requests
import urllib.parse
from validate_email import validate_email
from flask import redirect, request, session

def is_valid_email(email):
    return validate_email(
        email_address=email,
        check_regex=True,
        check_mx=True,
        from_address='my@from.addr.ess',
        helo_host='my.host.name',
        smtp_timeout=10,
        dns_timeout=10,
        use_blacklist=True
    )

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
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
    """
    A good password must have:
    
    - 8 or more characters
    - At least one uppercase character
    - At least one lowercase character
    - At least one digit
    """
    return fullmatch(r'[A-Za-z0-9]{8,}', key)
