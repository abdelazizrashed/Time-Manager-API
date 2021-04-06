from setuptools import setup

setup(
    name = 'app',
    version = '0.0',
    description = 'API for a time manager app which manages time by creating schedules and devide them into tasks.',
    author='Abdelaziz Rashed',
    author_email='abdelaziz.y.rashed@gmail.com',
    packages = [
        'app'
    ],
    include_package_data = True,
    install_requires=[
        'flask',
        'flask_restful',
        'flask_jwt',
        'flask_sqlalchemy'
    ]
)