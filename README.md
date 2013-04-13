# Lighthouse

-
### What is it?


Lighthouse is a service built on [Python Bottle] (http://bottlepy.org/docs/dev/) that monitors Fogbugz for updates from the URL Trigger.

-
### Background


Fogbugz has a nifty [URL Trigger] (http://fogbugz.stackexchange.com/questions/6183/url-trigger-integrate-with-virtually-any-outside-system) which fires off a POST or GET to an external URL when an event occurs. (IE: When a case is opened and assigned to a specific person.) Lighthouse acts as the destination for the trigger, storing information into a mongodb document. 

-

### Installation

[Download and install MongoDB] (http://docs.mongodb.org/manual/installation)  
    
    git clone git@github.com:Dannyzen/lighthouse.git
#
    pip install bottle
#
    pip install pymongo
#
    cd lighthouse
    python lighthouse.py
<img src="https://github.com/dannyzen/lighthouse/raw/master/img/cmd.jpg" />

    Set your fogbugz url trigger to: 
        http://yourserver.com:1337/ticket?case_number={CaseNumber}&date={EventTime}&editor={PersonEditingName}&time={EventTime}&project_name={ProjectName}&status={StatusName}&title={Title}&week=getWeek()

<img src="https://github.com/dannyzen/lighthouse/raw/master/img/fb.jpg" />


### Document structure
-
        db.ticket.find().pretty()
        {
        "_id" : ObjectId("51699fe743d213423d1586fd"),
        "status" : "Active (1. Fix It)",
        "week" : 15,
        "project_name" : "QA",
        "title" : "testing",
        "case_number" : "5259",
        "editor" : "Danny Rosen",
        "time" : "2013-04-13 18:11:23Z"
        }
