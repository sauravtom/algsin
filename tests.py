#!/usr/bin/env python

import time

import urllib

import json

try:
    from google.appengine.api import urlfetch
    import webapp2
except:
    pass

from database import googl_shortner
from database import reddit_scraper

arr=[[u'Position: Unpaid [2013] Short (8:00)- Uncovering the Laws Regarding Unpaid Internships', u'https://vimeo.com/76955441'], [u'Free to Choose (1980), a 10 part series on economics and the morality of regulation and basic human freedom', u'http://www.youtube.com/watch?v=YRLAKD-Vuvk'], [u'Mondo Cane (1962) The original "shockumentary" consisting of a collection of mostly real archive footage displaying mankind at its most depraved and perverse. Just in time for Halloween.', u'http://www.youtube.com/watch?v=SodbsPbneMM&feature=c4-overview-vl&list=PL24D57B170B8E742B'], [u'Four Horsemen (2012) - 23 international thinkers, government advisors and Wall Street money-men break their silence and explain how to establish a moral and just society - [01:38]', u'http://www.youtube.com/watch?v=5fbvquHSPJU&list=UUs8SA3E0FAGsI6fdHZe88oQ'], [u'BBC: Extreme Pilgrim - Ascetic Christianity (58:59) [2008]', u'http://www.youtube.com/watch?v=9VjU_505i6E'], [u'The Boy With The Incredible Brain - My Shocking Story (2005)', u'http://www.youtube.com/watch?v=XXPTLNVAIfc'], [u'The Secret Life of Chaos - BBC [2010]', u'http://www.youtube.com/watch?v=PygpFRdvN3g&feature=youtu.be'], [u'[Request] Full version of TEACH (CBS, 2013)?', u'http://www.youtube.com/watch?v=Yh_1Xuvrvo4'], [u'The Woman Who Woke Up Chinese BBC (2013)', u'http://www.youtube.com/watch?v=mS28lxspE1w'], [u'bulletproof salesman (2008) Fidelis Cloer sells safety, more specifically he deals in heavy duty protection vehicles which will have a significant effect upon how you will be a leaving a fire fight. This documentary centres itself around the life in a day of an armoured vehicle salesman.', u'http://www.youtube.com/watch?v=QMgy4O669VE'], [u'"A Very British Witchcraft" (2013) - documentary on Gerald Gardner & Wicca', u'http://www.youtube.com/watch?v=dHAqBjOvYOQ'], [u"Race and Intelligence : Science's Last Taboo (2009) [44:52]", u'http://www.youtube.com/watch?v=Ao8W2tPujeE'], [u'SNAKE KILLERS OF KALAHARI (2001) aka The Crazy Nastyass Honey Badger', u'http://www.youtube.com/watch?v=LkZklaOvGS8\u200e'], [u'After Tiller Official Trailer 1 (2013) - Abortion Documentary', u'https://www.youtube.com/watch?v=xf3rETOO62s&feature=player_embedded#t=0'], [u'Drug Frenzy (2013)', u'http://www.youtube.com/watch?list=PL_IlIlrxhtPPAhi-eNZ0VaRzSY0c1-0n1&v=M7l1Tozxbg8'], [u'OOKP \u2013 The Day I Got My Sight Back [59m26s] [BBC] [2013]', u'https://www.youtube.com/watch?v=YlMRuDixr8M'], [u'Stephen Fry - The Machine That Made Us (2008)', u'http://www.youtube.com/watch?v=O6KmzuULPmQ'], [u'Jerry Seinfeld Biography [2003]', u'https://www.youtube.com/watch?v=ZKjEdAtNH6c'], [u'The Path Beyond Thought (2001)', u'http://www.youtube.com/watch?v=Tonvcf-3csQ'], [u'The Persecution of African Migrants in the Holy Land (2013)', u'http://www.youtube.com/watch?v=dPxv4Aff3IA'], [u'Crossing England in a Punt: River of Dreams (BBC, 2013)', u'http://www.youtube.com/watch?v=r4HCpTQNzEI'], [u'The Occult Experience (1985) - featuring Anton Lavey and H.R. Giger.', u'http://vimeo.com/21956578'], [u"The Gestapo - ''The Sword is Forged'' [2006]Part 1 of a three-part history of Nazi Germany's gestapo, or secret state police, recalls its origins; and profiles its leading figures, including its head, Heinrich M\xfcller. - [88:09]", u'http://www.youtube.com/watch?v=46wCNNdXbwo'], [u'The Pendle Witch Child (2012)', u'http://www.youtube.com/watch?v=Yv-JDUfADiw'], [u'A 17th Century History for Girls - Harlots, Housewives and Heroines [2013]', u'http://www.youtube.com/watch?v=uMLHBVrVE8E'], [u'The Silk Road. 12 episodes, each an hour long. [1980]', u'https://www.youtube.com/watch?v=b-AqeE2p_ww&list=PL43EA21B3FBAA90CF'], [u'The Shutka Book of Records - unique and a highly engaging insight into the biggest Roma settlement in Europe! (2005)', u'http://www.youtube.com/watch?v=RPJnukaw-3Q']]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write( googl_shortner('www.apple.com') )
        arr = 
        for i in arr:
            r=googl_shortner(i[1])
            self.response.out.write( '%s\n' %(r) )
        

app = webapp2.WSGIApplication([
    ('/tests', MainHandler)
], debug=True)

if __name__ =='__main__':
    googl_shortner('www.apple.com')
    start_time = time.clock()
    #print bitly3_shorten_oauth('http://sauravtom.github.io')
    for i in arr[5:]:
        print i[1] , googl_shortner(i[1])
    print time.clock() - start_time, "seconds"


