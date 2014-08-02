#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
from app import r
from app import g
from app import logging
from app import salt

from flask import (render_template)
from flask import redirect, make_response
from flask import Response, jsonify
from flask import abort, request
from flask import session

import os
import logging
from random import randint


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
