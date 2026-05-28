from flask import jsonify
from app import db
from app.api.v1 import api_v1
from app.models import CafeteriaMenu, Announcement, User

@api_v1.route('/menus', methods=['GET'])
def get_menus():
    menus = db.session.scalars(db.select(CafeteriaMenu).order_by(CafeteriaMenu.date.desc())).all()
    data = []
    for menu in menus:
        data.append({
            'id': menu.id,
            'date': menu.date.isoformat(),
            'menu_type': menu.menu_type,
            'soup': menu.soup,
            'main_dish': menu.main_dish,
            'side_dish': menu.side_dish,
            'calories': menu.calories,
            'author_username': menu.author.username
        })
    return jsonify(data)

@api_v1.route('/announcements', methods=['GET'])
def get_announcements():
    announcements = db.session.scalars(db.select(Announcement).order_by(Announcement.date.desc())).all()
    data = []
    for announcement in announcements:
        data.append({
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.content,
            'date': announcement.date.isoformat(),
            'author_username': announcement.author.username
        })
    return jsonify(data)
