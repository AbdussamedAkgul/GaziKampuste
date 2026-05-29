import os
import time
from datetime import date
from flask import render_template, redirect, url_for, flash, request, abort, current_app, session
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from app import db
from app.main import main
from app.main.forms import ProfileForm, CafeteriaMenuForm, AnnouncementForm, EventForm
from app.models import User, CafeteriaMenu, Announcement, Event
from app.decorators import admin_required

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@main.route('/')
@main.route('/index')
def index():
    today = date.today()
    normal_menu = db.session.scalar(
        db.select(CafeteriaMenu).where(
            CafeteriaMenu.date == today
        )
    )
    
    # Fallback to the latest menus if today's menu isn't entered yet
    if normal_menu is None:
        normal_menu = db.session.scalars(
            db.select(CafeteriaMenu).order_by(CafeteriaMenu.date.desc())
        ).first()
        
    # Get latest 3 announcements
    latest_announcements = db.session.scalars(
        db.select(Announcement).order_by(Announcement.date.desc(), Announcement.id.desc()).limit(3)
    ).all()
    
    return render_template('index.html', normal_menu=normal_menu, announcements=latest_announcements)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(file.filename)
            if allowed_file(filename):
                ext = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"user_{current_user.id}_{int(time.time())}.{ext}"
                
                upload_folder = os.path.join(current_app.root_path, 'static', 'avatars')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Delete old avatar file if not default.jpg
                if current_user.avatar_file and current_user.avatar_file != 'default.jpg':
                    old_path = os.path.join(upload_folder, current_user.avatar_file)
                    if os.path.exists(old_path):
                        try:
                            os.remove(old_path)
                        except Exception:
                            pass
                
                file.save(os.path.join(upload_folder, unique_filename))
                current_user.avatar_file = unique_filename
            else:
                flash('Yalnızca .png, .jpg, .jpeg uzantılı resimler yüklenebilir.', 'danger')
                return redirect(url_for('main.profile'))
                
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profil bilgileriniz başarıyla güncellendi.', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    return render_template('profile.html', form=form)

# Cafeteria Menu CRUD
@main.route('/menus')
def menus_list():
    page = request.args.get('page', 1, type=int)
    query = db.select(CafeteriaMenu).order_by(CafeteriaMenu.date.desc(), CafeteriaMenu.id.desc())
    pagination = db.paginate(query, page=page, per_page=5, error_out=False)
    menus = pagination.items
    delete_form = FlaskForm()
    return render_template('menus.html', menus=menus, pagination=pagination, delete_form=delete_form)

@main.route('/menu/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_menu():
    form = CafeteriaMenuForm()
    if form.validate_on_submit():
        menu = CafeteriaMenu(
            date=form.date.data,
            soup=form.soup.data,
            main_dish=form.main_dish.data,
            side_dish=form.side_dish.data,
            calories=form.calories.data,
            author=current_user
        )
        db.session.add(menu)
        db.session.commit()
        flash('Yemekhane menüsü başarıyla eklendi.', 'success')
        return redirect(url_for('main.menus_list'))
    return render_template('menu_form.html', form=form, title='Yeni Menü Ekle')

@main.route('/menu/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_menu(id):
    menu = db.get_or_404(CafeteriaMenu, id)
        
    form = CafeteriaMenuForm()
    if form.validate_on_submit():
        menu.date = form.date.data
        menu.soup = form.soup.data
        menu.main_dish = form.main_dish.data
        menu.side_dish = form.side_dish.data
        menu.calories = form.calories.data
        db.session.commit()
        flash('Yemekhane menüsü başarıyla güncellendi.', 'success')
        return redirect(url_for('main.menus_list'))
    elif request.method == 'GET':
        form.date.data = menu.date
        form.soup.data = menu.soup
        form.main_dish.data = menu.main_dish
        form.side_dish.data = menu.side_dish
        form.calories.data = menu.calories
        
    return render_template('menu_form.html', form=form, title='Menü Düzenle')

@main.route('/menu/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_menu(id):
    menu = db.get_or_404(CafeteriaMenu, id)
        
    form = FlaskForm()
    if form.validate_on_submit():
        db.session.delete(menu)
        db.session.commit()
        flash('Yemekhane menüsü başarıyla silindi.', 'success')
    else:
        flash('Güvenlik doğrulaması başarısız oldu.', 'danger')
    return redirect(url_for('main.menus_list'))

# Announcements CRUD
@main.route('/announcements')
def announcements_list():
    page = request.args.get('page', 1, type=int)
    query = db.select(Announcement).order_by(Announcement.date.desc(), Announcement.id.desc())
    pagination = db.paginate(query, page=page, per_page=5, error_out=False)
    announcements = pagination.items
    delete_form = FlaskForm()
    return render_template('announcements.html', announcements=announcements, pagination=pagination, delete_form=delete_form)

@main.route('/announcement/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            date=date.today(),
            author=current_user
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Duyuru başarıyla eklendi.', 'success')
        return redirect(url_for('main.announcements_list'))
    return render_template('announcement_form.html', form=form, title='Yeni Duyuru Ekle')

@main.route('/announcement/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_announcement(id):
    announcement = db.get_or_404(Announcement, id)
        
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash('Duyuru başarıyla güncellendi.', 'success')
        return redirect(url_for('main.announcements_list'))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
        
    return render_template('announcement_form.html', form=form, title='Duyuru Düzenle')

@main.route('/announcement/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_announcement(id):
    announcement = db.get_or_404(Announcement, id)
        
    form = FlaskForm()
    if form.validate_on_submit():
        db.session.delete(announcement)
        db.session.commit()
        flash('Duyuru başarıyla silindi.', 'success')
    else:
        flash('Güvenlik doğrulaması başarısız oldu.', 'danger')
    return redirect(url_for('main.announcements_list'))

@main.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('main.index'))
    
    q_lower = q.lower()
    
    # Duyurularda arama
    announcements = db.session.scalars(
        db.select(Announcement).where(
            or_(
                Announcement.title.ilike(f'%{q}%'),
                Announcement.content.ilike(f'%{q}%')
            )
        ).order_by(Announcement.date.desc())
    ).all()

    # Menülerde arama (çorba, ana yemek veya yan lezzet)
    menus = db.session.scalars(
        db.select(CafeteriaMenu).where(
            or_(
                CafeteriaMenu.soup.ilike(f'%{q}%'),
                CafeteriaMenu.main_dish.ilike(f'%{q}%'),
                CafeteriaMenu.side_dish.ilike(f'%{q}%')
            )
        ).order_by(CafeteriaMenu.date.desc())
    ).all()
    
    # Diğer (Statik) Sayfalarda Arama Algoritması
    static_pages = [
        {
            "title": "Akademik Takvim",
            "url": url_for("main.academic_calendar"),
            "description": "Dönem başı, dönem sonu ve kayıt haftalarını içeren takvim.",
            "keywords": ["akademik", "takvim", "güz", "bahar", "tatil", "ders", "kayıt"]
        },
        {
            "title": "Sınav Takvimi",
            "url": url_for("main.exam_schedule"),
            "description": "Vize ve final sınav saatlerini içeren haftalık sınav programı.",
            "keywords": ["sınav", "vize", "final", "program", "saat", "takvim"]
        },
        {
            "title": "Profil",
            "url": url_for("main.profile"),
            "description": "Kullanıcı hesap bilgileri, şifre ve avatar güncelleme ekranı.",
            "keywords": ["profil", "hesap", "ayarlar", "şifre", "avatar", "kullanıcı", "resim"]
        },
        {
            "title": "Ana Sayfa",
            "url": url_for("main.index"),
            "description": "Sitenin ana sayfası.",
            "keywords": ["ana sayfa", "giriş", "home"]
        }
    ]
    
    static_results = []
    for page in static_pages:
        # Eğer sorgu direkt sayfa adında geçiyorsa veya keywordlerde varsa
        if q_lower in page["title"].lower() or any(q_lower in kw for kw in page["keywords"]):
            static_results.append(page)

    return render_template('search_results.html', query=q, announcements=announcements, menus=menus, static_results=static_results)

@main.route('/set_language/<lang>')
def set_language(lang):
    if lang in current_app.config['LANGUAGES']:
        session['language'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main.route('/schedule')
def schedule():
    return render_template('schedule.html')

# Academic Calendar
@main.route('/academic-calendar')
def academic_calendar():
    return render_template('academic_calendar.html')

# Exam Schedule
@main.route('/exam-schedule')
def exam_schedule():
    return render_template('exam_schedule.html')

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
