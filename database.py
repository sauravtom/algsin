#!/usr/bin/env python

import webapp2
import json
import urllib2
import urllib

from google.appengine.ext import db
import logging

import jinja2
import os

import bitly
from local_settings import BitlyKey

import sys
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

def reddit_scrape(url,tag):
    arr=[]
    arr0=[] #filtered array
    try:
        jsondata = json.loads(urlfetch.fetch(url).content)
    except:
        jsondata = json.loads(urllib2.urlopen(url).read())

    shortapi = bitly.Api(login=BitlyKey['login'], apikey=BitlyKey['apikey'])

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
            f = shortapi.shorten( i[1]+';'+i[0] )
        except:
            if len(f) == 0:
                continue
                logging.info("Unable to shorten this url: " + i[1])
            else:
                pass
        else:
            i[0]=i[0].encode('ascii', 'ignore')
            i[1]=i[1].encode('ascii', 'ignore')
            f = f.split('/')[-1]
            i.append(f)
            i.append(tag)
            logging.info("Shortened "+tag +" " +f+  " " + i[1] +" "+ i[0])
            arr0.append(i)
    #arr[0]=title; arr[1]=real image(content) url; arr[2]=bitly fake url; arr[3] = cat/tag(meme.advice_animal)
    return arr0

def super_array(arr):
    super_arr=[]
    for i in arr:
        for j in i:
            super_arr.append(j)
    return super_arr        

class Matrix(db.Expando):
    meme = db.TextProperty() #using text since string can only store 500 characters
    eye_candy = db.TextProperty()
    video = db.TextProperty()
    news = db.TextProperty()
    num = db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)

class Update_DB(webapp2.RequestHandler):
    def get(self):
        #self.response.out.write(page_id)

        try:
            arr1=reddit_scrape('http://www.reddit.com/r/documentaries/.json?limit=50','video.documentaries')
            arr2=reddit_scrape('http://www.reddit.com/r/fullmoviesonvimeo+fullmoviesonyoutube/.json?limit=50','video.movies')
            arr3=reddit_scrape('http://www.reddit.com/r/fulltvshowsonyoutube/.json?limit=50','video.tvshows')
            arr4=reddit_scrape('http://www.reddit.com/r/standupspecials+standupvideos/.json?limit=50','video.standup')
            arr5=reddit_scrape('http://www.reddit.com/r/EarthPornVids+videoporn/.json?limit=50','video.bestof')
            arr6=reddit_scrape('http://www.reddit.com/r/VideoVault+BiographyFilms/.json?limit=50','video.old')

            super_arr_video = super_array( [arr1,arr2,arr3,arr4,arr5,arr6] )

            arr1=reddit_scrape('http://www.reddit.com/user/multi-mod/m/rage/.json?limit=50','meme.rage')
            arr2=reddit_scrape('http://www.reddit.com/r/AdviceAnimals/.json?limit=50','meme.advice_animals')
            arr3=reddit_scrape('http://www.reddit.com/r/ecards/.json?limit=50','meme.ecards')
            arr4=reddit_scrape('http://www.reddit.com/r/funny+memes/.json?limit=50','meme.other')
            arr5=reddit_scrape('http://www.reddit.com/user/helzibah/m/animalswith/.json?limit=50','meme.wtf')

            super_arr_meme = super_array([arr1,arr2,arr3,arr4,arr5])

            arr1=reddit_scrape('http://www.reddit.com/r/quotesporn/.json?limit=50','eyecandy.quotes')
            arr2=reddit_scrape('http://www.reddit.com/r/earthporn+ruralporn+skyporn/.json?limit=50','eyecandy.nature')
            arr3=reddit_scrape('http://www.reddit.com/r/cityporn+ArchitecturePorn/.json?limit=50','eyecandy.city')
            arr4=reddit_scrape('http://www.reddit.com/r/spaceporn+auroraporn/.json?limit=50','eyecandy.space')
            arr5=reddit_scrape('http://www.reddit.com/r/wallpapers/.json?limit=50','eyecandy.wallpapers')
            
            super_arr_eyecandy = super_array([arr1,arr2,arr3,arr4,arr5])
            
           
        except:
            e = sys.exc_info()[0]
            print e
            logging.error(e)
            self.response.out.write("Something went wrong, debug debug debug")

        else:
            #executed when the try clause does not raise an exception
            #flush the database
            q = db.GqlQuery("SELECT * FROM Matrix")
            for i in q:
                i.delete()
            logging.info('Database successfully flushed')
            
            # add new stuff to db
            foo=Matrix()
            foo.meme = json.dumps(super_arr_meme)
            foo.video = json.dumps(super_arr_video)
            foo.eye_candy= json.dumps(super_arr_eyecandy)
            foo.num=1
            foo.put()
            
            self.response.out.write(
                "Database updated and size video: %d meme: %d  eyecandy :%d" %( len(super_arr_video) ,len(super_arr_meme) ,len(super_arr_eyecandy)) 
            )
        
        #self.response.out.write(arr)

app = webapp2.WSGIApplication([
    ('/db', Update_DB)
], debug=True)
