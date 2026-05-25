from flask import render_template
from app.main import main

@main.route('/')
@main.route('/index')
def index():
    return "Gazi Mobil Yönetim Sistemi - Ana Sayfa (Main Blueprint)"
