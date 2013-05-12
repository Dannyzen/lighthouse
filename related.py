import sys
from fogbugz import FogBugz
from fogbugz import FogBugzAPIError
import fbSettings
import argparse
import pprint
from BeautifulSoup import BeautifulSoup
from pymongo import Connection

#consider a setting file
connection = Connection('localhost', 27017)
db = connection.lighthouse

def kickIt(new_ticket,editor,title):
    ticket_related = runEval(new_ticket,editor,title)
    if ticket_related: 
        updateRelated(new_ticket,ticket_related,editor,title)
    else:
       print "Ticket does not have a related case"

def runEval(new_ticket,editor,title):
    response = getRelatedTicket(new_ticket,editor,title) 
    try:
        ticket_related =  response.case.plugin_customfields_at_fogcreek_com_relatedxcaset117.string.encode('UTF-8')
        return ticket_related
    except AttributeError:
        raise
        return False

def checkTicket(new_ticket,editor,title):
    ticket = db['related_ticket'].find({"case_number":new_ticket,"related_to":{ '$exists': True}})
    if ticket.count() == 1:
        print "This ticket was already processed. Let's check if its database value is equal to its fogbugz value"
    else:
        print "let this ticket go through the normal process, it had no related_to property"
        runEval(new_ticket,editor,title)

def getRelatedTicket(new_ticket,editor,title):   
    #Todo - when this is run in isolation it returns a wild xml object. we can use the response.case.plugin... to flip this to a utf-8 string and then compare it to getRelatedProperty to build functionality for the case where a ticket related case is changed from '1' to '2'
    response = fogbugz.search(q=new_ticket,cols='plugin_customfields')
    return response
    
"""
def getRelatedProperty(new_ticket):
    #not yet completed 
    db_entry = db['related_ticket'].find({"case_number":new_ticket})
    for ticket in db_entry:
        return ticket["related_to"]
"""

def updateRelated(new_ticket,ticket_related,editor,title):
    print "-\n\-" + new_ticket
    response = fogbugz.edit(ixBug=ticket_related,sEvent=('case %s (%s) has been opened by %s' % (new_ticket, editor, title)))
    addRelated(new_ticket,ticket_related)

def addRelated(new_ticket,ticket_related):
    print new_ticket + ticket_related
    db['related_ticket'].update({"case_number":new_ticket},{'$set':{"related_to":ticket_related}}) 
    print "-\n\-Update the db"

if hasattr(fbSettings,'TOKEN'):
    fogbugz = FogBugz(fbSettings.URL, fbSettings.TOKEN)
else:
    fogbugz = FogBugz(fbSettings.URL)
    fogbugz.logon(fbSettings.LOGIN, fbSettings.PW)

if __name__ == '__main__':
    getTicketInfo()
