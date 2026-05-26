from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth import auth
from app.auth.forms import RegisterForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User

def send_reset_email(user, token):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    print("\n" + "="*80)
    print(f"MOCK E-POSTA GONDERILDI ({user.email})")
    print(f"Merhaba {user.username},")
    print("GaziKampuste Yonetim Sistemi sifre sifirlama talebiniz alinmistir.")
    print("Sifrenizi sifirlamak icin lütfen asagidaki baglantiya tiklayin:")
    print(f"-> {reset_url}")
    print("Bu baglanti 10 dakika gecerlidir.")
    print("Eger bu talebi siz yapmadiysaniz bu e-postayi gormezden gelebilirsiniz.")
    print("="*80 + "\n")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt işleminiz başarıyla gerçekleşti! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(
                (User.username == form.username_or_email.data) | 
                (User.email == form.username_or_email.data)
            )
        )
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı/e-posta veya şifre.', 'danger')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        flash(f'Hoş geldiniz, {user.username}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
            next_page = url_for('main.index')
        return redirect(next_page)
        
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user:
            token = user.get_reset_password_token()
            send_reset_email(user, token)
        # Güvenlik nedeniyle kullanıcı olmasa bile aynı mesajı gösteriyoruz
        flash('Şifre sıfırlama yönergeleri e-posta adresinize gönderildi.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Geçersiz veya süresi dolmuş şifre sıfırlama bağlantısı.', 'danger')
        return redirect(url_for('main.index'))
        
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_password.html', form=form)
