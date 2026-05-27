import unittest
import os
import io
from datetime import date, timedelta
from app import create_app, db
from app.models import User, CafeteriaMenu, Announcement
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # In-memory database
    WTF_CSRF_ENABLED = False  # Disable CSRF for easier form testing in unit tests

class CRUDProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create dummy users
        self.user1 = User(username='testuser1', email='test1@example.com')
        self.user1.set_password('password')
        self.user2 = User(username='testuser2', email='test2@example.com')
        self.user2.set_password('password')
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/auth/login', data=dict(
            username_or_email=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_profile_access_required_login(self):
        # Accessing profile without login should redirect to login
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])

    def test_profile_update(self):
        # Login
        self.login('testuser1', 'password')
        
        # Test GET profile info
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser1', response.data)
        self.assertIn(b'test1@example.com', response.data)

        # Test POST profile update without avatar
        response = self.client.post('/profile', data=dict(
            username='updateduser',
            email='updated@example.com'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Profil bilgileriniz başarıyla güncellendi.'.encode('utf-8'), response.data)
        
        user = db.session.get(User, self.user1.id)
        self.assertEqual(user.username, 'updateduser')
        self.assertEqual(user.email, 'updated@example.com')

    def test_profile_avatar_upload_restrictions(self):
        self.login('testuser1', 'password')
        
        # Try uploading invalid file type
        response = self.client.post('/profile', data=dict(
            username='testuser1',
            email='test1@example.com',
            avatar=(io.BytesIO(b"dummy content"), 'test.txt')
        ), follow_redirects=True)
        # Should reject or show invalid file error
        self.assertIn('Sadece .jpg, .jpeg ve .png format'.encode('utf-8'), response.data)

        # Try uploading valid file type (.png)
        response = self.client.post('/profile', data=dict(
            username='testuser1',
            email='test1@example.com',
            avatar=(io.BytesIO(b"dummy image content"), 'avatar.png')
        ), follow_redirects=True)
        self.assertIn('Profil bilgileriniz başarıyla güncellendi.'.encode('utf-8'), response.data)
        user = db.session.get(User, self.user1.id)
        self.assertNotEqual(user.avatar_file, 'default.jpg')
        self.assertTrue(user.avatar_file.endswith('.png'))

    def test_menu_crud_and_permissions(self):
        self.login('testuser1', 'password')
        
        # Create menu
        response = self.client.post('/menu/add', data=dict(
            date='2026-05-27',
            menu_type='normal',
            soup='Mercimek Corbasi',
            main_dish='Kofte',
            side_dish='Pilav',
            calories=800
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Yemekhane menüsü başarıyla eklendi.'.encode('utf-8'), response.data)

        menu = db.session.scalar(db.select(CafeteriaMenu).where(CafeteriaMenu.soup == 'Mercimek Corbasi'))
        self.assertIsNotNone(menu)
        self.assertEqual(menu.user_id, self.user1.id)

        # Edit menu by owner
        response = self.client.post(f'/menu/{menu.id}/edit', data=dict(
            date='2026-05-27',
            menu_type='normal',
            soup='Domates Corbasi',
            main_dish='Kofte',
            side_dish='Pilav',
            calories=850
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Yemekhane menüsü başarıyla güncellendi.'.encode('utf-8'), response.data)
        
        # Verify changes
        db.session.refresh(menu)
        self.assertEqual(menu.soup, 'Domates Corbasi')

        # Logout user1 and login user2
        self.logout()
        self.login('testuser2', 'password')

        # Attempt to edit user1's menu by user2 -> should return 403
        response = self.client.get(f'/menu/{menu.id}/edit')
        self.assertEqual(response.status_code, 403)

        response = self.client.post(f'/menu/{menu.id}/edit', data=dict(
            date='2026-05-27',
            menu_type='normal',
            soup='Hack attempt',
            main_dish='Kofte',
            side_dish='Pilav',
            calories=850
        ))
        self.assertEqual(response.status_code, 403)

        # Attempt to delete user1's menu by user2 -> should return 403
        response = self.client.post(f'/menu/{menu.id}/delete')
        self.assertEqual(response.status_code, 403)

        # Logout user2 and login user1 (owner) to delete
        self.logout()
        self.login('testuser1', 'password')
        
        # Test delete using GET (Should not be allowed, since routes.py defines only POST)
        response = self.client.get(f'/menu/{menu.id}/delete')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

        # Test delete using POST
        response = self.client.post(f'/menu/{menu.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Yemekhane menüsü başarıyla silindi.'.encode('utf-8'), response.data)
        self.assertIsNone(db.session.get(CafeteriaMenu, menu.id))

    def test_announcement_crud_and_permissions(self):
        self.login('testuser1', 'password')
        
        # Create announcement
        response = self.client.post('/announcement/add', data=dict(
            title='Sinav Duyurusu',
            content='Sinavlar yaklasiyor.'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Duyuru başarıyla eklendi.'.encode('utf-8'), response.data)

        announcement = db.session.scalar(db.select(Announcement).where(Announcement.title == 'Sinav Duyurusu'))
        self.assertIsNotNone(announcement)
        self.assertEqual(announcement.user_id, self.user1.id)

        # Edit announcement by owner
        response = self.client.post(f'/announcement/{announcement.id}/edit', data=dict(
            title='Guncel Sinav Duyurusu',
            content='Sinavlar yaklasiyor.'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Duyuru başarıyla güncellendi.'.encode('utf-8'), response.data)
        
        db.session.refresh(announcement)
        self.assertEqual(announcement.title, 'Guncel Sinav Duyurusu')

        # Logout user1 and login user2
        self.logout()
        self.login('testuser2', 'password')

        # Attempt to edit user1's announcement by user2 -> should return 403
        response = self.client.get(f'/announcement/{announcement.id}/edit')
        self.assertEqual(response.status_code, 403)

        # Attempt to delete user1's announcement by user2 -> should return 403
        response = self.client.post(f'/announcement/{announcement.id}/delete')
        self.assertEqual(response.status_code, 403)

        # Logout user2 and login user1 (owner) to delete
        self.logout()
        self.login('testuser1', 'password')

        # Test delete using GET (Should fail/not allowed)
        response = self.client.get(f'/announcement/{announcement.id}/delete')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

        # Test delete using POST
        response = self.client.post(f'/announcement/{announcement.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Duyuru başarıyla silindi.'.encode('utf-8'), response.data)
        self.assertIsNone(db.session.get(Announcement, announcement.id))

    def test_pagination_and_ordering(self):
        # Create 7 cafeteria menus to test page sizing of 5
        menus = []
        for i in range(7):
            menu = CafeteriaMenu(
                date=date.today() - timedelta(days=i),
                menu_type='normal',
                soup=f'Soup {i}',
                main_dish=f'Dish {i}',
                side_dish=f'Side {i}',
                calories=700 + i,
                author=self.user1
            )
            menus.append(menu)
        db.session.add_all(menus)
        db.session.commit()

        # Request menus list page 1
        response = self.client.get('/menus')
        self.assertEqual(response.status_code, 200)
        # Should contain Soup 0 to Soup 4
        for i in range(5):
            self.assertIn(f'Soup {i}'.encode(), response.data)
        # Should NOT contain Soup 5 or Soup 6
        for i in range(5, 7):
            self.assertNotIn(f'Soup {i}'.encode(), response.data)

        # Request menus list page 2
        response = self.client.get('/menus?page=2')
        self.assertEqual(response.status_code, 200)
        # Should contain Soup 5 and Soup 6
        for i in range(5, 7):
            self.assertIn(f'Soup {i}'.encode(), response.data)
        # Should NOT contain Soup 0 to Soup 4
        for i in range(5):
            self.assertNotIn(f'Soup {i}'.encode(), response.data)

if __name__ == '__main__':
    unittest.main()
