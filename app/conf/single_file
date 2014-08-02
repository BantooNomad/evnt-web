#! /usr/bin/env python
# -*- coding: utf-8 -*-

# res/ rep cycle
from flask import (render_template, url_for)
from flask import redirect, make_response, Flask
from flask import Response, jsonify
from flask import abort, request
from flask import session, g
import pickle
from datetime import timedelta
from uuid import uuid4
from redis import Redis
from redis import StrictRedis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from json import dumps

import os
import logging
import hashlib
import uuid
from random import randint

salt = 'd40037e1ff7841838235533d910bbf24'

logging.basicConfig(filename='TaskWangu.log', level=logging.DEBUG)


import rethinkdb as r
from rethinkdb import *
import time
from datetime import datetime
from messageAPI import sendText

from redis import Redis
redis = Redis()

app = Flask('app')

import requests
from sendEMail import send_message


RDB_HOST = os.environ.get('RDB_HOST') or '188.226.195.158'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
LINK_DB = 'LinkUs'

ONLINE_LAST_MINUTES = 5

app.config[ONLINE_LAST_MINUTES] = 720


"""
def mark_online(user_id):
    now = int(time.time())
    expires = now + (60 * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    user_key = 'user-activity/%s' % user_id
    p = redis.pipeline()
    p.sadd(all_users_key, user_id)
    p.set(user_key, now)
    p.expireat(all_users_key, expires)
    p.expireat(user_key, expires)
    p.execute()


def get_user_last_activity(user_id):
    last_active = redis.get('user-activity/%s' % user_id)
    if last_active is None:
        return None
    return datetime.utcfromtimestamp(int(last_active))


def get_online_users():
    current = int(time.time()) // 60
    minutes = xrange(60)
    return redis.sunion(['online-users/%d' % (current - x)
                         for x in minutes])


class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = StrictRedis(host='188.226.195.158', port=6379)
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

app.session_interface = RedisSessionInterface()

"""


def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(LINK_DB).run(connection)
        r.db(LINK_DB).table_create('User').run(connection)
        logging.info('Database setup completed')
    except RqlRuntimeError:
        logging.info('App database already exists')
    finally:
        connection.close()


"""
# mark users online
@app.before_request
def mark_current_user_online():
    mark_online(request.remote_addr)
"""


@app.before_request
def before_request():
    try:
        logging.info('before_request')
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=LINK_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established")


@app.teardown_request
def teardown_request(exception):
    try:
        logging.info('teardown_request')
        g.rdb_conn.close()
    except AttributeError:
        pass


@app.route('/admin/', methods=['POST', 'GET'])
def adminSign():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        username = request.json.get('username')
        password = request.json.get('password')

        try:
            user = r.table('Admin').get(username).run(g.rdb_conn)
        except Exception, e:
            logging.warning('DB failed on /admin/ -> user not found')
            raise e

        if user is None:
            resp = make_response(jsonify({"Not Found": "User Not Found"}), 404)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(jsonify({"OK": "Signed In"}), 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminSignin.html')


@app.route('/api/signIn/', methods=['POST', 'PUT'])
def signIn():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    password = request.json.get('password')
    username = request.json.get('username')
    email = request.json.get('email')

    # join to another table
    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)
    except Exception, e:
        logging.warning('DB signIn failed on /api/signIn/ -> user not found')
        raise e

    if user is None:
        resp = make_response(jsonify({"Not Found": "User Not Found"}), 404)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    hashed_password = hashlib.sha512(str(password) + salt).hexdigest()

    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)

        if str(user['password']) != str(hashed_password):
            # add user to session then log in
            resp = make_response(
                jsonify({"Password": "Incorrect Password"}), 404)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp
    except RqlError:
        logging.warning('raise RqlError DB signIn failed on /api/signIn/')

    # manage sessions - add user to session
    # redis sessions -> flask
    # redis k/v store | dict
    resp = make_response(jsonify({"OK": "Signed In"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/profile/<username>/', methods=['POST', 'GET'])
def profile(username):

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        smsdata = request.json.get('smsdata')
        email = request.json.get('email')
        dob = request.json.get('dob')
        username = request.json.get('username')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "smscode": smsdata,
                                                        "state": state, "dob": dob, "mobileNo": mobileNo}).run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /profile/api/' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    try:
        user = r.table('UsersInfo').get(str(username)).run(g.rdb_conn)

        name = str(user['username'])
        state = str(user['state'])
        smscode = str(user['smscode'])
        password = str(user['password'])
        email = str(user['email'])
        mobileNo = str(user['mobileNo'])

    except RqlError:
        logging.warning('DB code verify failed on /profile/' + mobileNo)
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'profile2.html', name=name, email=email, smscode=smscode,
        state=state, username=username, mobileNo=mobileNo)


# credit API
@app.route('/api/credit/<username>/', methods=['POST', 'GET'])
def credit(username):

    if request.method == 'GET':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        username = request.json.get('username')

        try:
            user = r.table(
                'Payments').get(str(username)).pluck('credit_available').run(g.rdb_conn)

            credit = json.dumps(user)
            resp = make_response(jsonify(credit), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /api/credit' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        username = request.json.get('username')

        try:
            user = r.table(
                'Payments').get(str(username)).pluck('credit_available').run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /api/credit' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp


@app.route('/payments/<username>/', methods=['POST', 'GET'])
def payments(username):

    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        password = request.json.get('password')
        smsdata = request.json.get('smsdata')
        email = request.json.get('email')
        dob = request.json.get('dob')
        username = request.json.get('username')
        state = request.json.get('state')
        mobileNo = request.json.get('mobileNo')

        if mobileNo.startswith('0'):
            mobileNo = mobileNo[1:]

        if mobileNo.startswith('+254'):
            mobileNo = mobileNo[4:]

        try:
            user = r.table(
                'UsersInfo').get(str(username)).update({"email": email, "smscode": smsdata,
                                                        "state": state, "dob": dob, "mobileNo": mobileNo}).run(g.rdb_conn)

            resp = make_response(jsonify({"OK": "User Updated"}), 202)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        except RqlError:
            logging.warning(
                'DB code verify failed on /profile/api/' + username)
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

    try:
        user = r.table('Payments').get(str(username)).run(g.rdb_conn)
        username = str(user['username'])
        credit = str(user['credit_available'])

    except RqlError:
        logging.warning('DB code verify failed on /payments/' + mobileNo)
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'payments.html', username=username, credit=credit)


@app.route('/tasks/<username>/', methods=['POST', 'GET'])
def tasks(username):
    # task = RegistrationForm(request.form)
    # get mobileNo
    # check if no exists
    return render_template('createTask.html', username=username)


@app.route('/adminTasks/', methods=['POST', 'GET'])
def getAdminTasks():
    if request.method == 'POST':

        if not request.json:
            abort(400)

        if request.headers['Content-Type'] != 'application/json':
            abort(400)

        username = request.json.get('username')
        mobileNo = request.json.get('mobileNo')

        taskData = []
        try:
            tasks = r.table('Tasks').filter(
                {'task_urgency': 'started'}).limit(50).run(g.rdb_conn)
            for data in tasks:
                taskData.append(data)

        except RqlError:
            logging.warning('DB code verify failed on /api/adminTasks/')
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        taskData = dumps(taskData)

        resp = make_response(taskData, 200)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    try:
        task_size = r.table('Tasks').count().run(g.rdb_conn)

    except RqlError:
        logging.warning('DB code verify failed on /api/adminTasks/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template('adminViewTasks.html', task_size=task_size)


@app.route('/allTasks/<username>/', methods=['POST', 'GET'])
def getAllTasks(username):
    username = username
    return render_template('allTasks2.html', username=username)


@app.route('/api/getTasks/', methods=['POST', 'GET'])
def getTasks():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    username = request.json.get('username')

    taskData = []
    try:
        tasks = r.table('Tasks').filter({"username": username}).run(g.rdb_conn)
        for data in tasks:
            taskData.append(data)

    except RqlError:
        logging.warning('DB code verify failed on /api/getTasks/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    taskData = dumps(taskData)

    resp = make_response(taskData, 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/editTask/<username>/<task_id>/')
def taskInfo(username, task_id):
    try:
        user = r.table('Tasks').get(task_id).run(g.rdb_conn)

        task_title = str(user['task_title'])
        task_desc = str(user['task_desc'])
        task_urgency = str(user['task_urgency'])
        task_category = str(user['task_category'])
        due_date = str(user['due_date'])

    except RqlError:
        logging.warning('DB operation failed on /editTask/<task_id>/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'editTask2.html', task_category=task_category, task_urgency=task_urgency,
        task_desc=task_desc, task_title=task_title, due_date=due_date, username=username, task_id=task_id)


@app.route('/api/editTask/<task_id>/', methods=['PUT', 'POST'])
def editTask(task_id):
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    task_urgency = request.json.get('urgency')
    task_title = request.json.get('title')
    task_desc = request.json.get('description')
    task_category = request.json.get('category')
    due_date = request.json.get('due_date')
    task_id = request.json.get('task_id')

    # make request to get one task
    if request.method == 'GET':
        try:
            user_task = r.table('Tasks').get(task_id).run(g.rdb_conn)

        except RqlError:
            logging.warning('DB op failed on /api/editTask/')
            resp = make_response(jsonify({"Error": "503 DB error"}), 503)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp

        resp = make_response(jsonify({"Task fetched": user_task}), 202)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    try:
        r.table(
            'Tasks').get(task_id).update({'task_desc': task_desc, 'task_title': task_title,
                                          'task_category': task_category, 'task_urgency': task_urgency,
                                          'due_date': due_date}).run(g.rdb_conn)

    except RqlError:
        logging.warning('DB code verify failed on /api/editTask/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Updated"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/deleteTask/', methods=['PUT', 'POST'])
def deleteTask():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    task_id = request.json.get('task_id')

    try:
        # r.table('UsersInfo').get(mobileNo).update({"smscode": SMScode}).run(g.rdb_conn)
        r.table('Tasks').get(task_id).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/deleteTask/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Deleted"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/addTask/', methods=['POST', 'GET'])
def addTask():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    username = request.json.get('username')
    task_desc = request.json.get('description')
    task_title = request.json.get('title')
    # then update userInfo
    task_category = request.json.get('category')
    task_urgency = request.json.get('urgency')
    due_date = request.json.get('due_date')

    taskData = {"username": username, "task_title": task_title, "task_desc": task_desc,
                "task_category": task_category, "task_urgency": "started", "due_date": due_date}

    text_all = "LinkUs new task -> " + task_title + task_desc

    try:
        r.table('Tasks').insert(taskData).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/addTask/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # send email and SMS notification
    # sendText("+254710650613", str(text_all))
    # send_message("khalifleila@gmail.com", str(taskData))

    resp = make_response(jsonify({"OK": "Task Created"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/signUp/', methods=['POST'])
def getRandID():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    # use the mobile number as the id number its a unique entity
    # it works :D
    # use mobile number as username upon login -> send text with code
    username = request.json.get('username')
    email = request.json.get('email')
    # then update userInfo
    password = request.json.get('password')

    try:
        user = r.table('UsersInfo').get(username).run(g.rdb_conn)
        if user is not None:
            resp = make_response(jsonify({"Error": "User Exists"}), 400)
            resp.headers['Content-Type'] = "application/json"
            resp.cache_control.no_cache = True
            return resp
    except RqlError:
        logging.warning('DB code verify failed on /api/signUp/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    SMScode = randint(10000, 99999)
    # verify user send email with code
    # or SMS code
    # sendText(mobileNo, SMScode)
    hashed_password = hashlib.sha512(password + salt).hexdigest()

    try:
        # r.table('UsersInfo').get(mobileNo).update({"smscode": SMScode}).run(g.rdb_conn)
        r.table(
            'UsersInfo').insert({"state": "", "username": username, "dob": "", "email": email, "password": hashed_password,
                                 "smscode": SMScode, "mobileNo": ""}).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB code verify failed on /api/signUp/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    # add to sessions then login

    resp = make_response(jsonify({"OK": "Signed Up"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/newsLetter/', methods=['POST'])
def addNewsLetter():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    email = request.json.get('email')
    # mobile no is the id - primary key

    try:
        r.table('newsLetter').insert({
            'email': email,
        }).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB could not write on /api/newsLetter/')
        resp = make_response(jsonify({'Error': 'Save Failed'}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({'OK': 'Content Saved'}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/removeUser/', methods=['POST'])
def removeUser():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    password = request.json.get('password')
    username = request.json.get('username')

    # mobile no is the id - primary key
    try:
        r.table('UsersInfo').get(username).delete().run(g.rdb_conn)
    except RqlError:
        logging.warning('DB remove user failed on /api/removeUser')

    resp = make_response(jsonify({'OK': 'Content Removed'}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/UserInfo/', methods=['POST'])
def addUser():
    if not request.json:
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    # get JSON engine params
    fname = request.json.get('fname')
    lname = request.json.get('lname')
    username = request.json.get('username')
    mobileNo = request.json.get('mobileNo')  # this <- id
    state = request.json.get('state')
    location = request.json.get('location')
    email = request.json.get('email')

    # no id just work with mobileNo - easier
    # we'll send a text message enter code!

    if mobileNo.startswith('0'):
        mobileNo = mobileNo[1:]

    if mobileNo.startswith('+254'):
        mobileNo = mobileNo[4:]

    try:
        r.table('UsersInfo').insert({
            'fname': fname,
            'lname': lname,
            'mobileNo': mobileNo,
            'email': email,
            'state': state,
            'userVerified': 'False',
            'location': location
        }).run(g.rdb_conn)
    except RqlError:
        logging.warning('DB could not write on /api/adduser')

    resp = make_response(jsonify({"OK": "Content Saved"}), 202)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


# Basic Error handlers
@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify({"Error 404":
                                  "Not Found"}), 404)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify({"Error 400":
                                  "Bad request"}), 400)


@app.errorhandler(500)
def internal_error(e):
    return make_response(jsonify({"Error 500":
                                  "Internal Server Error"}), 500)


@app.errorhandler(408)
def timeout(e):
    return make_response(jsonify({"Error 408":
                                  "Request Timeout"}), 408)


@app.errorhandler(405)
def invalidMethod(e):
    return make_response(jsonify({"Error 405":
                                  "Invalid Request Method"}), 405)


@app.errorhandler(410)
def gone(e):
    return make_response(jsonify({"Error 410":
                                  "Resource is Gone"}), 410)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    # import newrelic.agent
    # newrelic.agent.initialize('conf/newrelic.ini')
    app.run('0.0.0.0', port=port, debug=True, threaded=True)
    # app.run(port=8000, debug=True, host='0.0.0.0')
    # this can be omitted if using gevent wrapped around gunicorn
