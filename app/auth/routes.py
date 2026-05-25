from flask import render_template
from app.auth import auth

@auth.route('/login')
def login():
    return "GaziKampüste Yönetim Sistemi - Giriş Sayfası (Auth Blueprint)"
