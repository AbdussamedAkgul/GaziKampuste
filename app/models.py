from datetime import date
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='student', server_default='student', nullable=False)
    avatar_file: Mapped[str] = mapped_column(String(64), default='default.jpg', server_default='default.jpg', nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    # İlişkiler (One-to-Many)
    menus: Mapped[List["CafeteriaMenu"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    announcements: Mapped[List["Announcement"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    events: Mapped[List["Event"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def get_reset_password_token(self) -> str:
        from flask import current_app
        from itsdangerous import URLSafeTimedSerializer as Serializer
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_password_token(token: str, expires_in: int = 600) -> Optional['User']:
        from flask import current_app
        from itsdangerous import URLSafeTimedSerializer as Serializer
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_in)
        except Exception:
            return None
        return db.session.get(User, data['user_id'])



class CafeteriaMenu(db.Model):
    __tablename__ = 'cafeteria_menus'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    menu_type: Mapped[str] = mapped_column(String(20), default='normal', server_default='normal', nullable=False) # 'normal' veya 'vegetarian'
    soup: Mapped[str] = mapped_column(String(100), nullable=False)
    main_dish: Mapped[str] = mapped_column(String(100), nullable=False)
    side_dish: Mapped[str] = mapped_column(String(100), nullable=False)
    calories: Mapped[Optional[int]] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # İlişkiler (Many-to-One)
    author: Mapped["User"] = relationship(back_populates="menus")

    def __repr__(self) -> str:
        return f'<CafeteriaMenu {self.date} ({self.menu_type})>'


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # İlişkiler (Many-to-One)
    author: Mapped["User"] = relationship(back_populates="announcements")

    def __repr__(self) -> str:
        return f'<Announcement {self.title}>'


@login.user_loader
def load_user(user_id: str) -> Optional[User]:
    return db.session.get(User, int(user_id))

class Event(db.Model):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    event_type: Mapped[str] = mapped_column(String(20), nullable=False) # 'midterm', 'final', 'club', 'school'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # İlişkiler (Many-to-One)
    author: Mapped["User"] = relationship(back_populates="events")

    def __repr__(self) -> str:
        return f'<Event {self.title}>'
