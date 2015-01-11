from hashlib import md5
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(127), index=True)
    last_name = db.Column(db.String(127), index=True)
    email = db.Column(db.String(127), index=True, unique=True)
    upvotes = db.Column(db.Integer, index=True)
    password = db.Column(db.String(32))
    image_url = db.Column(db.String(1024))

    tokens = db.relationship('Token', backref='owner', lazy='dynamic')

    # Note to self: We also say that the backref is dynamic so we can query with the backref from the other side.
    attending = db.relationship('Event',
                               secondary='user_events_link',
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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), index=True)
    message = db.Column(db.String(4096), index=True)
    latitude = db.Column(db.Float, index=True)
    longitude = db.Column(db.Float, index=True)
    upvotes = db.Column(db.Integer, index=True, default = 0)
    event_type = db.Column(db.String(32))
    event_status = db.Column(db.String(32))
    image_url = db.Column(db.String(1024))

    create_date = db.Column(db.DateTime)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def to_dict(self):
        dictionary = {}
        dictionary['id'] = self.id
        dictionary['name'] = self.name
        dictionary['message'] = self.message
        dictionary['latitude'] = self.latitude
        dictionary['longitude'] = self.longitude
        dictionary['upvotes'] = self.upvotes
        dictionary['image_url'] = self.image_url
        dictionary['event_type'] = self.event_type
        dictionary['event_status'] = self.event_status
        dictionary['create_date'] = self.create_date
        dictionary['creator_id'] = self.creator_id

        return dictionary


class UserEventsLink(db.Model):
    __tablename__ = "user_events_link"
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
    vote = db.Column('upvoted', db.Integer, default = 0)
    user = db.relationship(User, backref=db.backref("user_assoc"))
    event = db.relationship(Event, backref=db.backref("event_assoc"))


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(32))


