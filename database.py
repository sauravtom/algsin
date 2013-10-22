#!/usr/bin/env python

import webapp2
import json
import urllib2
import urllib

from google.appengine.ext import db
import logging

import jinja2
import os

#import bitly
#from local_settings import BitlyKey

import sys
from google.appengine.api import urlfetch

from datetime import datetime

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class Matrix(db.Expando):
    meme = db.TextProperty() #using text since string can only store 500 characters
    eye_candy = db.TextProperty()
    video = db.TextProperty()
    news = db.TextProperty()
    num = db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)

def super_array(arr):
    super_arr=[]
    for i in arr:
        for j in i:
            super_arr.append(j)
    return super_arr        

def googl_shortner(url):
    result = urlfetch.fetch(url='https://www.googleapis.com/urlshortener/v1/url',
        payload=json.dumps({"longUrl": url}),
        method=urlfetch.POST,
        headers={'Content-Type': 'application/json'})
    content = json.loads(result.content)
    '''
    try:
        logging.info( url,content['id'] )
    except:
        pass
    '''
    try:
        return content['id']
    except:
        return content['error']


def reddit_scrape(url,tag):
    arr=[]
    arr0=[] #filtered array
    
    try:    jsondata = json.loads(urlfetch.fetch(url).content)
    except: jsondata = json.loads(urllib2.urlopen(url).read())

    #make an array of title vs image links
    for i in jsondata["data"]["children"]:
        f = i["data"]["url"]
        #images
        if f[-4:] in [".jpg",".png",".gif"]:
            arr.append( [ i["data"]["title"] , f ])
            continue
        if "http://imgur.com/" in f:
            f = "http://i."+f.split('/')[2]+"/"+f.split('/')[3]+".jpg"
            arr.append( [ i["data"]["title"] , f ])
            continue
        #youtube videos
        if "youtube.com/watch" in f or "vimeo.com" in f:
            arr.append( [ i["data"]["title"] , f ])
            continue
        else:
            pass

    # appends fake url in the array
    for i in arr:
        try:
            i[0]=i[0].decode('unicode_escape').encode('ascii','ignore')
            f= googl_shortner(i[1]+'?title='+i[0])
        except:
            #logging.error(e)
            logging.error("Unable to shorten this url: " + i[1]+'?title='+i[0] + " value returned is "+f)
        else:
            i[0]=i[0].encode('ascii', 'ignore')
            i[1]=i[1].encode('ascii', 'ignore')
            f = f.split('/')[-1]
            i.append(f)
            i.append(tag)
            arr0.append(i)
            logging.info( i )
            f='Fuck OFf'

    x= len(arr) - len(arr0)
    #arr[0]=title; arr[1]=real image(content) url; arr[2]=bitly fake url; arr[3] = cat/tag(meme.advice_animal)
    return arr0

class Update_DB(webapp2.RequestHandler):
    def get(self,page_id):

        try:
            logging.info(page_id)
            if page_id == 'video':
                arr1=reddit_scrape('http://www.reddit.com/r/documentaries/.json?limit=50','video.documentaries')
                arr2=reddit_scrape('http://www.reddit.com/r/fullmoviesonvimeo+fullmoviesonyoutube/.json?limit=50','video.movies')
                arr3=reddit_scrape('http://www.reddit.com/r/fulltvshowsonyoutube/.json?limit=50','video.tvshows')
                arr4=reddit_scrape('http://www.reddit.com/r/standupspecials+standupvideos/.json?limit=50','video.standup')
                arr5=reddit_scrape('http://www.reddit.com/r/EarthPornVids+videoporn/.json?limit=50','video.bestof')
                arr6=reddit_scrape('http://www.reddit.com/r/VideoVault+BiographyFilms/.json?limit=50','video.old')

                super_arr = super_array( [arr1,arr2,arr3,arr4,arr5,arr6] )

            if page_id == 'meme':
                arr1=reddit_scrape('http://www.reddit.com/user/multi-mod/m/rage/.json?limit=50','meme.rage')
                arr2=reddit_scrape('http://www.reddit.com/r/AdviceAnimals/.json?limit=50','meme.advice_animals')
                arr3=reddit_scrape('http://www.reddit.com/r/ecards/.json?limit=50','meme.ecards')
                arr4=reddit_scrape('http://www.reddit.com/r/funny+memes/.json?limit=50','meme.other')
                arr5=reddit_scrape('http://www.reddit.com/user/helzibah/m/animalswith/.json?limit=50','meme.wtf')

                super_arr = super_array([arr1,arr2,arr3,arr4,arr5])

            if page_id == 'eyecandy':
                arr1=reddit_scrape('http://www.reddit.com/r/quotesporn/.json?limit=50','eyecandy.quotes')
                arr2=reddit_scrape('http://www.reddit.com/r/earthporn+ruralporn+skyporn/.json?limit=50','eyecandy.nature')
                arr3=reddit_scrape('http://www.reddit.com/r/cityporn+ArchitecturePorn/.json?limit=50','eyecandy.city')
                arr4=reddit_scrape('http://www.reddit.com/r/spaceporn+auroraporn/.json?limit=50','eyecandy.space')
                arr5=reddit_scrape('http://www.reddit.com/r/wallpapers/.json?limit=50','eyecandy.wallpapers')
                
                super_arr = super_array([arr1,arr2,arr3,arr4,arr5])
            
            
            logging.info("Array formation complete %s: %d " %( page_id, len(super_arr) ) )            
        
        except Exception as e:
            logging.error(e.args)
            #self.response.out.write(e)
            self.response.out.write("Eyuuu, Something went wrong, check the terminal for errors")
            
        else:
            #executed when the try clause does not raise an exception
            #flush the database
            arr=[]
            q = db.GqlQuery("SELECT * FROM Matrix")
            
            for foo in q:
                if page_id == 'video':  foo.video = json.dumps(super_arr)
                if page_id == 'meme':   foo.meme = json.dumps(super_arr)
                if page_id == 'eyecandy':   foo.eye_candy= json.dumps(super_arr)
            
            try:    foo.put()
            
            except UnboundLocalError:
                #Database is empty Create an instance of matrix
                foo = Matrix()
                foo.put()
                logging.info('Created first instance of Matrix')

            msg = '%s database updated with %d entries : %s' %(page_id,len(super_arr),str(datetime.now()))
            
            self.response.out.write(msg)

            
        if page_id in ['test','tests']:
            arr=reddit_scrape('http://www.reddit.com/user/helzibah/m/animalswith/.json?limit=50','meme.wtf')
            self.response.out.write(arr)

        
app = webapp2.WSGIApplication([
    ('/db', Update_DB),
    ('/db/(\S+)', Update_DB )
], debug=True)
