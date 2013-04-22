import sys
from fogbugz import FogBugz
from fogbugz import FogBugzAPIError
import fbSettings
import argparse
import pprint
from BeautifulSoup import BeautifulSoup

def getTicketInfo(new_ticket,editor,title):
    response = fogbugz.search(q=new_ticket,cols='plugin_customfields')
    evalField(new_ticket,response,title,editor)

def evalField(new_ticket,response,editor,title):
    try:
        ticket_related =  response.case.plugin_customfields_at_fogcreek_com_relatedxcaset117.string.encode('UTF-8')
        updateRelated(new_ticket,ticket_related,editor,title)
    except AttributeError:
        print "Ticket does not have a related case"
        raise
        sys.exit()
    print "debug " + ticket_related

def updateRelated(new_ticket,ticket_related,editor,title):
    response = fogbugz.edit(ixBug=ticket_related,sEvent=('case %s (%s) has been opened by %s' % ticket_related, title, editor))

if hasattr(fbSettings,'TOKEN'):
    fogbugz = FogBugz(fbSettings.URL, fbSettings.TOKEN)
else:
    fogbugz = FogBugz(fbSettings.URL)
    fogbugz.logon(fbSettings.LOGIN, fbSettings.PW)

if __name__ == '__main__':
    getTicketInfo()
