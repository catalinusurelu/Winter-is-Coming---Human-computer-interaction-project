#!flask/bin/python
from app import db
import os.path

from config import database_dir

if os.path.exists(database_dir):
	os.remove(database_dir)
