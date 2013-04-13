#Lighthouse.py | github.com/dannyzen/lighthouse
#Danny Rosen - @dannyzen. 4/2013

import json
import bottle
from helpers import *
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('localhost', 27017)
db = connection.lighthouse



@route('/ticket', method='POST')
def diplay_ticket():
    case_number = request.query.case_number
    editor = request.query.editor
    time = request.query.time
    project_name = request.query.project_name
    status = request.query.status
    title = request.query.title
    week = getWeek()
    month = getMonth()
    db_response=db['ticket'].save({"case_number":case_number,"editor":editor,"time":time,"project_name":project_name,"status":status,"title":title,"week":week})
run(host='0.0.0.0', port=1337)
