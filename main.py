#!/usr/bin/env python

import webapp2
import json
import urllib2

from google.appengine.ext import db
import logging

import jinja2
import os

import bitly
from local_settings import BitlyKey

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


def reddit_scrape(url):
    arr=[]
    jsondata = json.loads(urllib2.urlopen(url).read())
    shortapi = bitly.Api(login=BitlyKey['login'], apikey=BitlyKey['apikey'])
        
    for i in jsondata["data"]["children"]:
        f = i["data"]["url"]

        if f[-4:] in [".jpg",".png"]:
            arr.append( [ i["data"]["title"] , f ])
        if "http://imgur.com/" in f:
            f = "http://i."+f.split('/')[2]+"/"+f.split('/')[3]+".jpg"
            arr.append( [ i["data"]["title"] , f ])

    # appends fake url in the array
    for i in arr:
        i[0]=i[0].encode('ascii', 'ignore')
        i[1]=i[1].encode('ascii', 'ignore')
        f = shortapi.shorten( i[1]+';'+i[0] )
        f = f.split('/')[-1]
        i.append(f)

    return arr


class Matrix(db.Expando):
    data = db.TextProperty() #using text since string can only store 500 characters


# declaring array in global scope
arr=[]
try:
    q = db.GqlQuery("SELECT * FROM Matrix")
    for i in q:
        arr = json.loads(i.data)
        logging.info('database updated for the first time')
except:
    self.redirect('/db')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        try :   n = int(self.request.get('page'))
        except ValueError:  n=1

        try :   i = self.request.get('i')
        except ValueError:  i=""

        if i == "":
            template = jinja_environment.get_template('templates/index.html')
            self.response.out.write(template.render(arr=arr,n=n))
        else:
            bitly_url = "http://bit.ly/" + i

            fp = urllib2.urlopen(bitly_url)
            url=fp.geturl()

            title = url.split(';')[-1]
            title = urllib2.unquote(title)
            url = url.split(';')[0]

            template = jinja_environment.get_template('templates/image.html')
            self.response.out.write(template.render(url=url,title=title))


class Update_DB(webapp2.RequestHandler):
    def get(self):
        arr = reddit_scrape('http://www.reddit.com/user/TakSlak/m/sfwporn/.json?limit=200')
        
        try: 
            #flush the database
            q = db.GqlQuery("SELECT * FROM Matrix")
            for i in q:
                i.delete()
            logging.info('Database successfully flushed')
        except:
            logging.error('error flushing the database')    

        try:
            foo=Matrix()
            foo.data = json.dumps(arr)
            foo.put()
            logging.info('Database successfully updated')
        except HTTPError: 
            logging.error('error writing to database')
            self.redirect('/')

        self.response.out.write("Database updated and size : " + str(len(arr)))
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/db',Update_DB)
], debug=True)


'''
only store those links in db which ends with .jpg or .png [DONE]
(transform image links to imgur links) [DONE]

update database every 12 hours [DONE]

make separate page for image permalinks [DONE]

ad try catch in /db [DONE]

require login for /db

Add 404 page

'''

