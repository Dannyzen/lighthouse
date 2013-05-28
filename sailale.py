from sailthru import sailthru_client as sc
import fbSettings

api_secret = fbSettings.ST_SECRET
api_key = fbSettings.ST_KEY
sailthru_client = sc.SailthruClient(api_key, api_secret)


def purchaseCall(email):
    item=[{'id':'1','title':'SailAle Ticket', 'price':100, 'qty':1, 'url':'http://www.sailthru.com/sailale'}]
    data={"email": email,"items":item}
    response = sailthru_client.api_post("purchase",data)
    body = response.get_body()
    print body

def emailCall(email):
    data={'template':'SailAle Confirm',"vars":{"user":email},'email':'sailale@sailthru.com'}
    print data
    response = sailthru_client.api_post("send",data)
    body = response.get_body()
    print body

