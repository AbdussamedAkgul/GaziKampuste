from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Regexp, Optional
from flask_wtf.file import FileField, FileAllowed
from app.models import User
from app import db

class ProfileForm(FlaskForm):
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
    avatar = FileField('Profil Fotoğrafı (Avatar)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece .jpg, .jpeg ve .png formatındaki görselleri yükleyebilirsiniz!')
    ])
    submit = SubmitField('Profili Güncelle')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(db.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane seçin.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = db.session.scalar(db.select(User).where(User.email == email.data))
            if user is not None:
                raise ValidationError('Bu e-posta adresi zaten kayıtlı. Lütfen başka bir e-posta adresi girin.')


class CafeteriaMenuForm(FlaskForm):
    date = DateField('Tarih', format='%Y-%m-%d', validators=[
        DataRequired(message='Tarih seçilmesi zorunludur.')
    ])
    menu_type = SelectField('Menü Tipi', choices=[
        ('normal', 'Normal Menü'),
        ('vegetarian', 'Vejetaryen Menü')
    ], validators=[
        DataRequired(message='Menü tipi seçilmesi zorunludur.')
    ])
    soup = StringField('Çorba', validators=[
        DataRequired(message='Çorba alanı zorunludur.'),
        Length(max=100, message='Çorba adı en fazla 100 karakter olabilir.')
    ])
    main_dish = StringField('Ana Yemek', validators=[
        DataRequired(message='Ana yemek alanı zorunludur.'),
        Length(max=100, message='Ana yemek adı en fazla 100 karakter olabilir.')
    ])
    side_dish = StringField('Yardımcı Yemek', validators=[
        DataRequired(message='Yardımcı yemek alanı zorunludur.'),
        Length(max=100, message='Yardımcı yemek adı en fazla 100 karakter olabilir.')
    ])
    calories = IntegerField('Kalori (kcal)', validators=[
        Optional()
    ])
    submit = SubmitField('Kaydet')


class AnnouncementForm(FlaskForm):
    title = StringField('Başlık', validators=[
        DataRequired(message='Başlık alanı zorunludur.'),
        Length(max=100, message='Başlık en fazla 100 karakter olabilir.')
    ])
    content = TextAreaField('İçerik', validators=[
        DataRequired(message='Duyuru içeriği zorunludur.')
    ])
    submit = SubmitField('Kaydet')
