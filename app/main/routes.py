from flask import render_template
from app.main import main

@main.route('/')
@main.route('/index')
def index():
    return "GaziKampuste Yönetim Sistemi - Ana Sayfa (Main Blueprint)"

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
