from hashlib import md5
from app import db


class UserEventsLink(db.Model):
	__tablename__ = "user_events_link"
	user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'))


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(127), index=True)
	last_name = db.Column(db.String(127), index=True)
	email = db.Column(db.String(127), index=True, unique=True)
	upvotes = db.Column(db.Integer, index=True)
	password = db.Column(db.String(32))
	image_url = db.Column(db.String(1024))

	tokens = db.relationship('Token', backref='owner', lazy='dynamic')

	attending = db.relationship('Event',
	                           secondary=user_events_link,
	                           backref=db.backref('participants', lazy='dynamic'),
	                           lazy='dynamic')

	def to_dict(self):
		dictionary = {}
		dictionary['id'] = self.id
		dictionary['first_name'] = self.first_name
		dictionary['last_name'] = self.last_name
		dictionary['email'] = self.email
		dictionary['upvotes'] = self.upvotes
		dictionary['image_url'] = self.image_url
		dictionary['password'] = self.password

		return dictionary


class Token(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	token = db.Column(db.String(32))


class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(127), index=True)
	latitude = db.Column(db.Float, index=True)
	longitude = db.Column(db.Float, index=True)
	upvotes = db.Column(db.Integer, index=True)
	event_type = db.Column(db.String(32))
	event_status = db.Column(db.String(32))
	image_url = db.Column(db.String(1024))

	create_date = db.Column(db.DateTime)

	creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


	def to_dict(self):
		dictionary = {}
		dictionary['id'] = self.id
		dictionary['name'] = self.name
		dictionary['latitude'] = self.latitude
		dictionary['longitude'] = self.longitude
		dictionary['upvotes'] = self.upvotes
		dictionary['image_url'] = self.image_url
		dictionary['event_type'] = self.event_type
		dictionary['event_status'] = self.event_status

		return dictionary
