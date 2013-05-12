#Lighthouse.py | github.com/dannyzen/lighthouse
#Danny Rosen - @dannyzen. 4/2013

import json
import bottle
from helpers import *
from bottle import route, run, request, abort
from pymongo import Connection
from related import kickIt, checkTicket 

connection = Connection('localhost', 27017)
db = connection.lighthouse

@route('/assigned_to_qa', method='POST')
def add_ticket():
    case_number = request.query.case_number
    editor = request.query.editor
    time = request.query.time
    project_name = request.query.project_name
    status = request.query.status
    title = request.query.title
    week = getWeek()
    month = getMonth()
    db_response=db['ticket'].save({"case_number":case_number,"editor":editor,"time":time,"project_name":project_name,"status":status,"title":title,"week":getWeek(), "month":getMonth()})

@route('/related_ticket_open', method='POST')
def open_related():
    case_number = request.query.case_number
    editor = request.query.editor
    time = request.query.time
    project_name = request.query.project_name
    status = request.query.status
    title = request.query.title
    week = getWeek()
    db_response=db['related_ticket'].save({"case_number":case_number,"editor":editor,"time":time,"project_name":project_name,"status":status,"title":title,"week":getWeek(), "month":getMonth()})
    #Hacky.
    new_ticket = case_number 
    kickIt(new_ticket,editor,title)

@route('/related_ticket_edit', method='POST')
def edit_related():
    case_number = request.query.case_number
    editor = request.query.editor
    time = request.query.time
    project_name = request.query.project_name
    status = request.query.status
    title = request.query.title
    week = getWeek()
    checkTicket(case_number,editor,title)

run(host='0.0.0.0', port=1339)
