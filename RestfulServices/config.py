import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_dir
UPLOAD_FOLDER = 'event_images'
HOST = '128.199.38.110'
