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

#import sys
#from google.appengine.api import urlfetch

from database import Matrix

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])
    

class MainHandler(webapp2.RequestHandler):
    def get(self,page_url_=""):
        #self.response.out.write(page_url_)
        if page_url_ == "":
            self.redirect('/0.meme.ecards')
        try:
            meme_arr 
            video_arr
            eyecandy_arr
            #self.response.out.write("Database loaded from memory")
        except:
            q = db.GqlQuery("SELECT * FROM Matrix")
            for i in q:
                meme_arr = json.loads(i.meme)
                video_arr = json.loads(i.video)
                eyecandy_arr = json.loads(i.eye_candy)
                #self.response.out.write("Database Read")

        page_url=page_url_.split('.')

        #image(item) page
        if page_url_.find('.') == -1 and len(page_url_) in [6,7]:
            i=page_url[0]
            bitly_url = "http://goo.gl/" + i

            fp = urllib2.urlopen(bitly_url)
            url=fp.geturl()

            k = url.rfind("?title=")
            #title = url.split('/')[-1]  #does not work for videos
            #url = url.split(';')[0]
            #url = "/".join(url.split('/')[:-1])
            title = url[k+7:]
            title = urllib2.unquote(title)
            murl=url
            url = url[:k]
            type='pic'
            type2=""
            uid=""

            if 'youtube' in url:
                type = 'vid'
                type2 = 'yt'
                uid=url.split('v=')[-1]
                uid= uid.split('&')[0]
            if 'vimeo' in url:
                type = 'vid'
                type2 = 'vm'
                uid=url.split('/')[-1]

            template = jinja_environment.get_template('templates/image.html')
            self.response.out.write(template.render(url=url,title=title,type=type,type2=type2,uid=uid,murl=murl))
        
        #posts page
        if len(page_url) == 3:
            page_no = int(page_url[0]) + 1
            cat = page_url[1]   #meme,video,eyecandy
            sub_cat = page_url[2] #rage,documentaries
            arr = []
            arr0 = []
            if cat == 'meme':
                type='pic'
                arr0 = meme_arr
                for i in arr0:
                    if i[3].split('.')[1] == sub_cat:
                        arr.append(i)

            if cat == 'video':
                type='vid'
                arr0 = video_arr
                for i in arr0:
                    if i[3].split('.')[1] == sub_cat:
                        if 'vimeo.com' in i[1]:
                            i.append(i[1].split("/")[-1])
                            i.append('vm')
                        else:
                            f=i[1].split("v=")[-1] #R_odAWTEtMQ&hd=1
                            f=f.split('&')[0] #R_odAWTEtMQ
                            i.append(f)
                            i.append('yt')
                        arr.append(i)

            if cat == 'eyecandy':
                type='pic'
                arr0 = eyecandy_arr
                for i in arr0:
                    if i[3].split('.')[1] == sub_cat:
                        arr.append(i)

            nextpageurl = ".".join([str(page_no),cat,sub_cat])
            
            template = jinja_environment.get_template('templates/index.html')
            self.response.out.write(template.render(arr=arr,n=page_no,sub_cat=sub_cat,npu=nextpageurl,type=type)) 

        if page_url_ == 'scn':
            template = jinja_environment.get_template('templates/staff.html')
            self.response.out.write(template.render())

        if page_url_ == 'about':
            template = jinja_environment.get_template('templates/about.html')
            self.response.out.write(template.render())  



app = webapp2.WSGIApplication([
    ('/(\S+)', MainHandler),
    ('/',MainHandler)
], debug=True)


'''
TODO
only store those links in db which ends with .jpg or .png [DONE]
(transform image links to imgur links) [DONE]

update database every 12 hours [DONE]

make separate page for image permalinks [DONE]

ad try catch in /db [DONE]

improve layout [DONE]

Add eye candy page [DONE]

Edit image page

Add Video page [DONE]

make pretty urls http://stackoverflow.com/questions/5763425/how-to-configure-app-yaml-to-support-urls-like-user-user-id [DONE]

make test.py

for some urls the bitly fake url generator is not working, detect thes in the reddit scrape function and purge them from array [DONE]

home page redirect [DONE]

ADD navigation [DONE]

Filter nsfw posts by checking the over18 tag

Add together.js to the site

read main array from memory instead of loading it from db, in a session

require login for /db

Add 404 page

Add gif support

Implement lazy loading

Add news page

learn how to raise exceptions

learn python code profiling

meme.other and meme.wtf thingy

'''

