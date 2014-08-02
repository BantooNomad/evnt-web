#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app import r
from app import g
from app import logging
from app import salt
from app import RqlError

from flask import (render_template)
from flask import redirect, make_response
from flask import jsonify
from flask import abort, request

from json import dumps

import hashlib
from random import randint


@app.route('/events/<username>/', methods=['POST', 'GET'])
def tasks(username):
    # task = RegistrationForm(request.form)
    # get mobileNo
    # check if no exists
    return render_template('events.html', username=username)


@app.route('/calendar/<username>/', methods=['POST', 'GET'])
def getAllTasks(username):
    username = username
    return render_template('calendar.html', username=username)


@app.route('/api/getEvents/', methods=['POST', 'GET'])
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
        payload = "LOG_INFO=" + simplejson.dumps({ 'Request':'app.before' })
        requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

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


@app.route('/editCalendar/<username>/<calendar_id>/')
def taskInfo(username, calendar_id):
    try:
        user = r.table('Tasks').get(task_id).run(g.rdb_conn)

        task_title = str(user['task_title'])
        task_desc = str(user['task_desc'])
        task_urgency = str(user['task_urgency'])
        task_category = str(user['task_category'])
        due_date = str(user['due_date'])

    except RqlError:
        payload = "LOG_INFO=" + simplejson.dumps({ '/editTask/<username>/<task_id>/':'DB operation failed on /editTask/<task_id>/' })
        requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        logging.warning('DB operation failed on /editTask/<task_id>/')
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    return render_template(
        'editCalendar.html', task_category=task_category, task_urgency=task_urgency, locationData= "Nairobi", contactPersons="James",
        task_desc=task_desc, task_title=task_title, due_date=due_date, username=username, task_id=task_id)


@app.route('/api/editTask/<event_id>/', methods=['PUT', 'POST'])
def editTask(event_id):
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


@app.route('/api/deleteTask/', methods=['PUT', 'POST', 'DELETE'])
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

        payload = "LOG_INFO=" + simplejson.dumps({ '/editTask/<username>/<task_id>/':'DB operation failed on /editTask/<task_id>/' })
        requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)
        
        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Deleted"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp


@app.route('/api/event/', methods=['POST', 'GET'])
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

        payload = "LOG_INFO=" + simplejson.dumps({ '/api/addTask/':'DB operation failed on /addTask/' })
        requests.post("https://logs-01.loggly.com/inputs/e15fde1a-fd3e-4076-a3cf-68bd9c30baf3/tag/python/", payload)

        resp = make_response(jsonify({"Error": "503 DB error"}), 503)
        resp.headers['Content-Type'] = "application/json"
        resp.cache_control.no_cache = True
        return resp

    resp = make_response(jsonify({"OK": "Task Created"}), 200)
    resp.headers['Content-Type'] = "application/json"
    resp.cache_control.no_cache = True
    return resp
