# tests/test_student.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase


class TestTeacherBlueprint(BaseTestCase):

    def test_teacher_login(self):
        # Ensure login behaves correctly.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Welcome, <em>teacher@teacher.com</em>!',
                response.data
            )
            self.assertIn(
                b'<li><a href="/teacher/2/classes/">View Classes</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "teacher@teacher.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertFalse(current_user.is_student())
            self.assertTrue(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_teacher_dashboard(self):
        # Ensure dashboard behaves correctly.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/teacher/2/classes/')
            self.assertIn(
                b'<h1>All Classes</h1>',
                response.data
            )
            self.assertIn(
                b'<p>You are not teaching any classes.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
