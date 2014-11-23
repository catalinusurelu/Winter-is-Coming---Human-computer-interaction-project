from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from app import app, db
from .models import User, Event

import random
from random import randint
import json

from sqlalchemy import desc


@app.route('/users', methods=['GET', 'POST'])
def users():
    if(request.method == "GET"):
        users = User.query.all()
        user_list = []
        for x in users:
            user_list.append(x.to_dict())
            
        return "GET Echo\n" + json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        app.logger.info("starting")
        jss = request.get_json()
        app.logger.info(str(jss))

        user = User(**jss)
        db.session.add(user)
        db.session.commit()

        return "POST Echo\n" + str(jss)

@app.route('/events', methods=['GET', 'POST'])
def events():
    if(request.method == "GET"):
        events = Event.query.all()
        event_list = []
        for x in events:
            event_list.append(x.to_dict())

        return "GET Echo\n" + json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        jss = request.get_json()
        jss['create_date'] = datetime.now()
        jss['event_status'] = 'started'

        event = Event(**jss)
        db.session.add(event)
        db.session.commit()

        return "POST Echo\n" + str(jss)

@app.route('/close_event/<int:event_id>', methods=['POST'])
def close_event(event_id):
        event = Event.query.get(event_id)
        event.event_status = 'closed'
        db.session.add(event)
        db.session.commit()

        return "POST Echo\n" + str(event.to_dict)

@app.route('/users/<int:user_id>/events', methods=['GET', 'POST', "DELETE"])
def user_events(user_id):
    user = User.query.get(user_id)

    if(user is None):
        return "No user", 404

    if(request.method == "GET"):
        event_list = []
        if(user.attending is not None):
            for x in user.attending:
                event_list.append(x.to_dict())
            
        return "GET Echo\n" + json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))
    elif(request.method == "POST"):
        jss = request.get_json()
        event = Event.query.get(jss['id'])

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



@app.route('/top_events')
def top_events():
   
    events = Event.query.filter(Event.event_status == "started").order_by(desc(Event.upvotes)).all()
    event_list = []

    if(events is not None):
        for x in events:
            event_list.append(x.to_dict())

    return "GET Echo\n" + json.dumps(event_list, sort_keys=True, indent=4, separators=(',', ': '))
    

@app.route('/top_users')
def top_users():
   
    users = User.query.order_by(desc(User.upvotes)).all()
    user_list = []
    if(users is not None):
        for x in users:
            user_list.append(x.to_dict())

    return "GET Echo\n" + json.dumps(user_list, sort_keys=True, indent=4, separators=(',', ': '))
