from setuptools import setup

setup(name='tourism-agency',
      version='1.0.0',
      description='Tourism Agency for Fontenay',
      author='Bruno Fischetti <brunofischetti@gmail.com>',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['services', 'utils'],
      install_requires=[
          'alembic==1.0.7',
          'aniso8601==1.3.0',
          'arrow==0.10.0',
          'asn1crypto==0.22.0',
          'bcrypt==3.1.4',
          'beautifulsoup4==4.6.0',
          'bibtexparser==0.6.2',
          'certifi==2017.4.17',
          'cffi==1.10.0',
          'chardet==3.0.4',
          'click==6.7',
          'cryptography==3.2',
          'Flask==1.0.2',
          'Flask-Bcrypt==0.7.1',
          'Flask-Cors==3.0.7',
          'Flask-JWT-Extended==3.9.1',
          'Flask-Migrate==2.3.1',
          'Flask-MySQL==1.4.0',
          'Flask-RESTful==0.3.6',
          'Flask-Script==2.0.6',
          'Flask-SQLAlchemy==2.3.2',
          'idna==2.5',
          'itsdangerous==0.24',
          'Jinja2==2.10.1',
          'Mako==1.0.7',
          'MarkupSafe==1.0',
          'psycopg2==2.7.3.2',
          'pycparser==2.18',
          'PyJWT==1.4.2',
          'PyMySQL==0.9.2',
          'python-dateutil==2.6.0',
          'python-editor==1.0.4',
          'pytz==2017.3',
          'six==1.10.0',
          'SQLAlchemy==1.3.0',
          'urllib3==1.25.2',
          'uWSGI==2.0.15',
          'Werkzeug==0.14.1'
      ],
      entry_points='''
          [console_scripts]
          tourism_agency=app.py
      ''',
      packages=['models', 'resources'],
      # package_data = {
      #     'tap_salesforce/schemas': [
      #         # add schema.json filenames here
      #     ]
      # },
      include_package_data=True,
      )
