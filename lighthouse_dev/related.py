import sys
from fogbugz import FogBugz
from fogbugz import FogBugzAPIError
import fbSettings
import argparse
import pprint
from BeautifulSoup import BeautifulSoup
from pymongo import Connection
from colorama import init, Fore


#consider a setting file
connection = Connection('localhost', 27017)
db = connection.lighthouse

def colorPrint(state,message):
    """ Prints red if state is 0, green if state is 1 """
    if state == 0:
        print(Fore.RED + message + Fore.RESET)
    if state == 1:
        print (Fore.GREEN + message + Fore.RESET)

def kickIt(new_ticket,editor,title):
    ticket_related = runEval(new_ticket)
    #if ticket_related: 
    updateRelated(new_ticket,ticket_related,editor,title)
    #else:
    #    colorPrint(0,"no ticket related")

def runEval(new_ticket):
    ticket_related = ticketToString(new_ticket) 
    #TODO 
    db_field = getRelatedProperty(ticket_related)
    if checkDupe(db_field,ticket_related) == False:
        addRelated(new_ticket,ticket_related)
        checkTicket(new_ticket,editor,title)
    return ticket_related

def checkTicket(new_ticket,editor,title):
    ticket = db['related_ticket'].find({"case_number":new_ticket,"related_to":{ '$exists': True}})
    if ticket.count() == 1:
       colorPrint(0,"This ticket was already processed. Let's check if its database value is equal to its fogbugz value --- not completed")
       #TODO
       runEval(new_ticket)
    else:
        colorPrint(1,"let this ticket go through the normal process, it had no related_to property") 
        kickIt(new_ticket,editor,title)

def getRelatedTicket(new_ticket):   
    response = fogbugz.search(q=new_ticket,cols='plugin_customfields')
    return response

def ticketToString(new_ticket):
    response = getRelatedTicket(new_ticket) 
    try:
        related_field = response.case.plugin_customfields_at_fogcreek_com_relatedxcaset117.string.encode('UTF-8')   
        return related_field
    except AttributeError:
        colorPrint(0,"This ticket has no related tickets")
        raise

#TODO
def getRelatedProperty(new_ticket):
    db_entry = db['related_ticket'].find({"case_number":new_ticket})
    print db_entry
    for ticket in db_entry:
        print ticket
        result = ticket["related_to"]
    return result

def checkDupe(db_field,ticket_related):
    if db_field == ticket_related:
        print  "halt, this has happened before"
        return True
    else:
        print "no, update with the new db field"
        return False

def updateRelated(new_ticket,ticket_related,editor,title):
    colorPrint(1, "updating " + ticket_related + " with " + new_ticket)
    response = fogbugz.edit(ixBug=ticket_related,sEvent=('case %s (%s) has been opened by %s' % (new_ticket, title, editor)))
    addRelated(new_ticket,ticket_related)

def addRelated(new_ticket,ticket_related):
    db['related_ticket'].update({"case_number":new_ticket},{'$set':{"related_to":ticket_related}}) 
    colorPrint(1,"Update the db")

if hasattr(fbSettings,'TOKEN'):
    fogbugz = FogBugz(fbSettings.URL, fbSettings.TOKEN)
else:
    fogbugz = FogBugz(fbSettings.URL)
    fogbugz.logon(fbSettings.LOGIN, fbSettings.PW)

if __name__ == '__main__':
   init()
