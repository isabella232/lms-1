# manage.py


import os
import unittest
import coverage
import datetime

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=['*/__init__.py', '*/config/*']
)
COV.start()

from project.server import app, db
from project.server.models import Student, Teacher, Admin, Course


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    else:
        return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_users():
    """Creates sample users."""
    student = Student(
        email='student@student.com',
        password='student'
    )
    db.session.add(student)
    teacher = Teacher(
        email='teacher@teacher.com',
        password='teacher'
    )
    db.session.add(teacher)
    admin = Admin(
        email='ad@min.com',
        password='admin'
    )
    db.session.add(admin)
    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    teacher = Teacher.query.filter_by(email='teacher@teacher.com').first()
    first_course = Course(
        name='Philosophy 101',
        description='From Plato to Socrates...',
        subject='Liberal Arts',
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        teacher_id=teacher.id
    )
    db.session.add(first_course)
    second_course = Course(
        name='Music Appreciation',
        description='This course teaches you how to understand \
                     what you are hearing.',
        subject='Liberal Arts',
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        teacher_id=teacher.id
    )
    db.session.add(second_course)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
