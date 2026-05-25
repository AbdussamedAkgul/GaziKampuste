from flask import render_template
from app.auth import auth

@auth.route('/login')
def login():
    return "Gazi Mobil Yönetim Sistemi - Giriş Sayfası (Auth Blueprint)"
