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
                b'<li><a href="/teacher/classes">View Classes</a></li>',
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

    def test_teacher_classes(self):
        # Ensure a teacher can view all classes.
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
            response = self.client.get('/teacher/classes')
            self.assertIn(
                b'<h1>All Classes</h1>',
                response.data
            )
            self.assertIn(
                b'<p>You are not teaching any classes.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_validate_teacher_decorator(self):
        # Ensure a user has to be a teacher to view all classes.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            response = self.client.get(
                '/teacher/classes',
                follow_redirects=True
            )
            self.assertIn(
                b'You do not have the correct permissions to view that page.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_add_class_page(self):
        # Ensure a teacher can view add class page.
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
            response = self.client.get('/teacher/add_class')
            self.assertIn(
                b'<h1>Add Class</h1>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_add_class(self):
        # Ensure a teacher can add a new class.
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
            response = self.client.post(
                '/teacher/add_class',
                data=dict(
                    name='Music Appreciation',
                    description='This class teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'<h1>All Classes</h1>',
                response.data
            )
            self.assertIn(
                b'Music Appreciation',
                response.data
            )
            self.assertNotIn(
                b'<p>You are not teaching any classes.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_view_classes(self):
        # Ensure a teacher can only view classes that they create.
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
            self.client.post(
                '/teacher/add_class',
                data=dict(
                    name='Music Appreciation',
                    description='This class teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.client.get('/logout')
            self.client.post(
                '/login',
                data=dict(
                    email='michael@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/teacher/classes')
            self.assertIn(
                b'<h1>All Classes</h1>',
                response.data
            )
            self.assertNotIn(
                b'Music Appreciation',
                response.data
            )
            self.assertIn(
                b'<p>You are not teaching any classes.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_view_class(self):
        # Ensure a teacher can view an individual class.
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
            self.client.post(
                '/teacher/add_class',
                data=dict(
                    name='Music Appreciation',
                    description='This class teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            response = self.client.get('/teacher/class/1')
            self.assertIn(
                b'<h1>Music Appreciation</h1>',
                response.data
            )
            self.assertIn(
                b'This class teaches you how to understand',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_edit_class(self):
        # Ensure a teacher can edit an individual class.
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
            self.client.post(
                '/teacher/add_class',
                data=dict(
                    name='Music Appreciation',
                    description='This class teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            response = self.client.post(
                '/teacher/update_class/1',
                data=dict(
                    name='Art Appreciation',
                    description='From here to there.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'<h1>Art Appreciation</h1>',
                response.data
            )
            self.assertIn(
                b'From here to there.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_edit_class_page(self):
        # Ensure a teacher can view edit class page.
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
            self.client.post(
                '/teacher/add_class',
                data=dict(
                    name='Music Appreciation',
                    description='This class teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            response = self.client.get('/teacher/update_class/1')
            self.assertIn(
                b'<h1>Update Class</h1>',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="name" \
name="name" required type="text" value="Music Appreciation">',
                response.data
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
