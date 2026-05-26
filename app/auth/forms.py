from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User
from app import db

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[
        DataRequired(message='Kullanıcı adı zorunludur.'),
        Length(min=3, max=64, message='Kullanıcı adı 3 ile 64 karakter arasında olmalıdır.'),
        Regexp('^[A-Za-z0-9_.]+$', message='Kullanıcı adı sadece harf, rakam, alt çizgi (_) ve nokta (.) içerebilir.')
    ])
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta adresi zorunludur.'),
        Email(message='Geçersiz e-posta adresi.'),
        Length(max=120, message='E-posta adresi en fazla 120 karakter olabilir.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur.'),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    password_confirm = PasswordField('Şifre Tekrar', validators=[
        DataRequired(message='Şifre tekrarı zorunludur.'),
        EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = db.session.scalar(db.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane seçin.')

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Bu e-posta adresi zaten kayıtlı. Lütfen başka bir e-posta adresi girin.')


class LoginForm(FlaskForm):
    username_or_email = StringField('Kullanıcı Adı veya E-posta', validators=[
        DataRequired(message='Kullanıcı adı veya e-posta adresi zorunludur.')
    ])
    password = PasswordField('Şifre', validators=[
        DataRequired(message='Şifre zorunludur.')
    ])
    remember_me = BooleanField('Beni Hatırla')
    submit = SubmitField('Giriş Yap')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('E-posta', validators=[
        DataRequired(message='E-posta adresi zorunludur.'),
        Email(message='Geçersiz e-posta adresi.')
    ])
    submit = SubmitField('Şifre Sıfırlama Bağlantısı Gönder')

    def validate_email(self, email):
        user = db.session.scalar(db.select(User).where(User.email == email.data))
        if user is None:
            raise ValidationError('Bu e-posta adresiyle kayıtlı bir kullanıcı bulunamadı.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Yeni Şifre', validators=[
        DataRequired(message='Yeni şifre zorunludur.'),
        Length(min=6, message='Şifre en az 6 karakter olmalıdır.')
    ])
    password_confirm = PasswordField('Yeni Şifre Tekrar', validators=[
        DataRequired(message='Şifre tekrarı zorunludur.'),
        EqualTo('password', message='Şifreler eşleşmiyor.')
    ])
    submit = SubmitField('Şifreyi Güncelle')
