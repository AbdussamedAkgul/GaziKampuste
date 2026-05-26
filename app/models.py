from datetime import date
from typing import List, Optional
from sqlalchemy import String, Text, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

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

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


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
