#!flask/bin/python
from app import app
from config import HOST

app.run(host=HOST, debug=True)
