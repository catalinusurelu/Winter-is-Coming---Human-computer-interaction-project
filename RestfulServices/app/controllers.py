from flask import render_template, flash, redirect, url_for, request, Response
from datetime import datetime
from app import app, db
from .models import User, Event, UserEventsLink

import random
from random import randint
import json

from sqlalchemy import desc

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from sqlalchemy import or_

from config import basedir

import os

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    app.logger.info(methods)
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            app.logger.info("Req method " + request.method)
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

            app.logger.info('OK')

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/users', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def users():
    if(request.method == "GET"):
        users = User.query.all()
        user_list = []
        for x in users:
            user_list.append(x.to_dict())
            
        return json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        app.logger.info("starting")
        jss = request.get_json()
        app.logger.info(str(jss))

        user = User(**jss)
        db.session.add(user)
        db.session.commit()

        # Get user with id.
        user = User.query.order_by(User.id.desc()).first()

        return json.dumps(user.to_dict())

@app.route('/users/<int:user_id>', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def user_id(user_id):
    user = User.query.get(user_id)
    if(request.method == "GET"):
        return json.dumps(user.to_dict(), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        app.logger.info("starting")
        jss = request.get_json()
        app.logger.info(str(jss))

        user = User(**jss)
        db.session.add(user)
        db.session.commit()

        # Get user with id.
        user = User.query.order_by(User.id.desc()).first()

        return json.dumps(user.to_dict())

@app.route('/events', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def events():
    if(request.method == "GET"):
        events = Event.query.all()
        event_list = []
        for x in events:
            event_list.append(x.to_dict())

        return json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        jss = request.get_json()
        jss['create_date'] = datetime.now()
        jss['event_status'] = 'started'

        event = Event(**jss)
        db.session.add(event)
        db.session.commit()

        return "POST Echo\n" + str(jss)

@app.route('/events/<int:event_id>', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def event_id(event_id):
    event = Event.query.get(event_id)
    if(request.method == "GET"):
        return json.dumps(event.to_dict(), sort_keys=True, indent=4, separators=(',', ': '))
    else:
        jss = request.get_json()
        jss['create_date'] = datetime.now()
        jss['event_status'] = 'started'

        event = Event(**jss)
        db.session.commit()

        return "POST Echo\n" + str(jss)

@app.route('/close_event/<int:event_id>', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], headers=['Content-Type'])
def close_event(event_id):
    event = Event.query.get(event_id)
    event.event_status = 'closed'
    db.session.add(event)
    db.session.commit()

    return "POST Echo\n" + str(event.to_dict)

@app.route('/users/<int:user_id>/events/<int:event_id>/upvote', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], headers=['Content-Type'])
def upvote_event(user_id, event_id):
    usersEventsLink = UserEventsLink.query.filter(UserEventsLink.vote <= 0,
                                                  UserEventsLink.user_id == user_id,
                                                  UserEventsLink.event_id == event_id).first()

    if usersEventsLink is None:
        usersEventsLink = UserEventsLink.query.filter(UserEventsLink.user_id == user_id,
                                                      UserEventsLink.event_id == event_id).first()
        if usersEventsLink is None:
            user = User.query.get(user_id)
            event = Event.query.get(event_id)

            usersEventsLink = UserEventsLink(user = user, event = event, vote = 1)

            db.session.add(usersEventsLink)

            event.upvotes = event.upvotes + 1

            db.session.commit()

            return str(event.upvotes)
        else:
            return ""

    if usersEventsLink is not None:
        usersEventsLink.vote = usersEventsLink.vote + 1
        usersEventsLink.event.upvotes = usersEventsLink.event.upvotes + 1
        db.session.add(usersEventsLink)
        db.session.commit()

        return str(usersEventsLink.event.upvotes)

    return ""

@app.route('/users/<int:user_id>/events/<int:event_id>/downvote', methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', methods=['POST', 'OPTIONS'], headers=['Content-Type'])
def downvote_event(user_id, event_id):
    usersEventsLink = UserEventsLink.query.filter(UserEventsLink.vote > 0,
                                                  UserEventsLink.user_id == user_id,
                                                  UserEventsLink.event_id == event_id).first()

    if usersEventsLink is None:
        usersEventsLink = UserEventsLink.query.filter(UserEventsLink.user_id == user_id,
                                                      UserEventsLink.event_id == event_id).first()
        if usersEventsLink is None:
            user = User.query.get(user_id)
            event = Event.query.get(event_id)

            if event.upvotes > 0:
                usersEventsLink = UserEventsLink(user = user, event = event, vote = -1)

                db.session.add(usersEventsLink)

                event.upvotes = event.upvotes - 1
                
                db.session.commit()

                return str(event.upvotes)
            else:
                return ""
        else:
            return ""


    if usersEventsLink is not None:
        usersEventsLink.vote = usersEventsLink.vote - 1
        usersEventsLink.event.upvotes = usersEventsLink.event.upvotes - 1
        db.session.add(usersEventsLink)
        db.session.commit()

        return str(usersEventsLink.event.upvotes)

    return ""


@app.route('/users/<int:user_id>/events', methods=['GET', 'POST', "DELETE", 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', "DELETE", 'OPTIONS'], headers=['Content-Type'])
def user_events(user_id):
    user = User.query.get(user_id)

    if(user is None):
        return "No user", 404

    # For multipart type we also create the event
    h = request.headers

    # conten type is of the form Invalid content type: multipart/form-data; boundary=----WebKitFormBoundaryaAQKqkPK9JMBmsuB
    if h['Content-Type'] is not None and "multipart/form-data" in h['Content-Type']:
        if request.method == 'POST':
            jss = {}
            jss['event_type'] = request.form['eventType']
            jss['latitude']= request.form['latitude']
            jss['longitude']= request.form['longitude']
            jss['name']= request.form['name']
            jss['message']= request.form['message']
            jss['create_date'] = datetime.now()
            jss['event_status'] = 'started'
            jss['creator_id'] = user_id

            event = Event(**jss)
            db.session.add(event)
            db.session.commit()

            # We need the event id so we can construct the image url.
            # We also need the event so we can link it to the creator.
            event = Event.query.order_by(Event.id.desc()).first()

            file = request.files['file']
            if file:
                filename = "Event_" + str(event.id) + os.path.splitext(file.filename)[1]
                event.image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # We store the image at the root of the site, so in a folder in ../RestfulServices
                if not os.path.exists(os.path.join(basedir,'..', app.config['UPLOAD_FOLDER'])):
                    os.makedirs(os.path.join(basedir,'..', app.config['UPLOAD_FOLDER']))


                file.save(os.path.join(basedir,'..', event.image_url))

            user.attending.append(event)
            db.session.add(user)
            db.session.commit()

             # Workaround to prevent 'redirection'. Can't prevent redirection from javascript.
            return redirect("http://" + app.config['HOST'] + "/index.html", code=302)

    if h['Content-Type'] is not None and h['Content-Type'] != "application/json":
            return "Invalid content type: " + h['Content-Type']

    if h['Content-Type'] is None:
        return "Content-type is mandatory"

    if(request.method == "GET"):
        event_list = []
        if(user.attending is not None):
            for x in user.attending:
                event_list.append(x.to_dict())
            
        return json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))
    elif(request.method == "POST"):
        jss = request.get_json()
        event = Event.query.get(jss['id'])
        event.creator_id = user_id

        user.attending.append(event)
        db.session.add(user)
        db.session.commit()

        return "POST Echo\n" + str(jss)
    else:
        jss = request.get_json()
        event = Event.query.get(jss['id'])

        user.attending.remove(event)
        db.session.add(user)
        db.session.commit()

        return "DELETE Echo\n" + str(jss)

@app.route('/events/<int:event_id>/users', methods=['GET', 'POST', "DELETE", 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'POST', "DELETE", 'OPTIONS'], headers=['Content-Type'])
def event_participants(event_id):
    event = Event.query.get(event_id)

    if(event is None):
        return "No event", 404

    if(request.method == "GET"):
        participant_list = []
        if(event.participants is not None):
            for x in event.participants:
                participant_list.append(x.to_dict())
            
        return json.dumps(participant_list, sort_keys=True, indent=4, separators=(',', ': '))
    elif(request.method == "POST"):
        jss = request.get_json()
        user = User.query.get(jss['id'])

        event.participants.append(user)
        db.session.add(event)
        db.session.commit()

        return "POST Echo\n" + str(jss)
    else:
        jss = request.get_json()
        user = User.query.get(jss['id'])

        event.participants.remove(user)
        db.session.add(event)
        db.session.commit()

        return "DELETE Echo\n" + str(jss)



@app.route('/top_events', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['Content-Type'])
def top_events():
    app.logger.info("Top events request")

    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    radius = request.args.get('radius')

    if(latitude is not None and longitude is not None and radius is not None):
            latitude = float(latitude)
            longitude = float(longitude)
            radius = float(radius)
            
            events = Event.query.filter(Event.event_status == "started", 
                or_(Event.latitude - latitude < radius, Event.latitude - latitude > -radius),
                or_(Event.longitude - longitude < radius, Event.longitude - longitude > -radius)).order_by(desc(Event.upvotes)).all()
    else:
        events = Event.query.filter(Event.event_status == "started").order_by(desc(Event.upvotes)).all()
    event_list = []

    if(events is not None):
        for x in events:
            event_list.append(x.to_dict())

    return json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))


@app.route('/top_users', methods=['GET', 'OPTIONS'])
@crossdomain(origin='*', methods=['GET', 'OPTIONS'], headers=['Content-Type'])
def top_users():
   
    users = User.query.order_by(desc(User.upvotes)).all()
    user_list = []
    if(users is not None):
        for x in users:
            user_list.append(x.to_dict())

    return json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': '))
