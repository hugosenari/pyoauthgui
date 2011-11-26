'''
Created on Nov 24, 2011

@author: hugosenari
'''
from yql import ThreeLegged


class TriPod(ThreeLegged):
    '''
    Maybe you think this is a monster, to be honest this is.
    Look... anything that have user leg, yahoo leg and app leg is a monster.
    This three legs makes a 'Tripod', as in some well knowed movie. ;)
    I made it to be more easy to use, and also to have fun.
    '''
    def __init__(self, yahoo_app_key, secret_key,
                 yuri=None, left_leg=None, right_leg=None, front_leg=None):
        '''
        Build your tripod.
        To assembly new tripod you need this things:
        yahoo app key: string that you receved from yahoo when made app registration.
        secret key: another key, useful like 'Ping Machine'. 
        IMPORTANT:  This tripod isn't cool, don't fire lasers or any else... :(
                    Maybe in next versions.
        '''
        super(TriPod, self).__init__(yahoo_app_key, secret_key)
        self.uri_auth = yuri #uri for user authentication
        self.yahoo_leg = left_leg #yahoo leg
        self.user_leg = right_leg #user leg
        self.token_leg = front_leg #token leg

    def _lag(self):
        '''
        This function is not correctly named
        '''
        if not self.yahoo_leg or not self.uri_auth:
            self.yahoo_leg, self.uri_auth = super(TriPod, self).get_token_and_auth_url()

    @property
    def yuri(self):
        '''
        Yuri, is my japonese friend, he looks like string.
        He is important as yahoo oauth2 authentication url.
        '''
        self._lag()
        return self.uri_auth

    @property
    def left_leg(self):
        '''
        left leg, also called yahoo leg
        '''
        self._lag()
        return self.yahoo_leg

    @property
    def right_leg(self):
        '''
        right leg, well know as user leg
        '''
        return self.user_leg
    
    @right_leg.setter
    def right_leg(self, user_leg):
        self.user_leg = user_leg
        self.token_leg = super(TriPod, self).get_access_token(self.left_leg, user_leg)

    @property
    def front_leg(self):
        '''
        front leg, is access token received for request
        before use this, you need set right_leg 
        '''
        if self.check_token(self.token_leg):
            self.token_leg = super(TriPod, self).refresh_token(self.token_leg)
        return self.token_leg

    def execute(self, query, param = {}):
        return super(TriPod, self).execute(query, param, token=self.front_leg)

from pyoauthgui import OauthGui
import  gtk
if __name__ == '__main__':
    AK = "dj0yJmk9WjNaQkoxdDZyanJ2JmQ9WVdrOVYyTjNkMFJYTm1jbWNHbzlNVE13TWpBd05EVS0mcz1jb25zdW1lcnNlY3JldCZ4PWQ0"
    SK = "9d8c16493dfc5de7010f9cd173e91cb82d63f924"
    tri = TriPod(AK, SK)
    yuri = tri.yuri
    #yuri = 'http://localhost/'
    #yuri = 'https://localhost/oauth_callback'
    def callback (arg):
        print 'callbacked: ', arg
        return arg
    oauthGui = OauthGui(yuri, callback)
    gtk.main()