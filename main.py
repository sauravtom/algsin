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

    for i in arr:
        f = shortapi.shorten( i[1]+";"+i[0] )
        i.append(f)

    return arr


class Matrix(db.Expando):
    data = db.TextProperty() #using text since string can only store 500 characters


arr=[]
try:
    q = db.GqlQuery("SELECT * FROM Matrix")
    for i in q:
        arr = json.loads(i.data)
except:
    self.redirect('/db')


class MainHandler(webapp2.RequestHandler):
    def get(self):
        try :   n = int(self.request.get('page'))
        except ValueError:  n=1

        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render(arr=arr,n=n))

class Image_page(webapp2.RequestHandler):
    def get(self):
        fake_url = self.request.url
        bcode = fake_url.split('/')[-1]
        #bitly_url = self.request.get('u')
        bitly_url = "http://bit.ly/" + bcode 
        #except ValueError:  self.redirect('/')

        fp = urllib2.urlopen(bitly_url)
        url=fp.geturl()

        title = url.split(';')[-1]
        url = url.split(';')[0]

        template = jinja_environment.get_template('templates/image.html')
        self.response.out.write(template.render(url=url,title=title))

class Update_DB(webapp2.RequestHandler):
    def get(self):
        arr = reddit_scrape('http://www.reddit.com/user/TakSlak/m/sfwporn/.json?limit=200')
        
        try:
            foo=Matrix()
            foo.data = json.dumps(arr)
            foo.put()
            logging.info('Database successfully updated')
        except HTTPError: 
            self.redirect('/')


        self.response.out.write("Database updated and size : " + str(len(arr)))
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/db',Update_DB),
    ('/i',Image_page)
], debug=True)


'''
only store those links in db which ends with .jpg or .png [DONE]
(transform image links to imgur links) [DONE]

update database every 12 hours

make separate page for image permalinks

ad try catch in /db

'''

