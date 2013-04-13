import json
import bottle
from helpers import *
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('localhost', 27017)
db = connection.lighthouse
 
@route('/documents/:input', method='POST')

def post_document(input):
    print input
    db['documents'].save({"test":input})


@route('/ticket', method='POST')
def diplay_ticket():
    #/ticket?case_number=case_number
    case_number = request.query.case_number
    editor = request.query.editor
    time = request.query.time
    project_name = request.query.project_name
    status = request.query.status
    title = request.query.title
    week = getWeek()
    month = getMonth()

    print case_number 
    db_response=db['ticket'].save({"case_number":case_number,"editor":editor,"time":time,"project_name":project_name,"status":status,"title":title,"week":week})
    #print db_response
run(host='0.0.0.0', port=1337)
