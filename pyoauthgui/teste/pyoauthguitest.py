'''
Created on Nov 24, 2011

@author: hugosenari
'''

from pyoauthgui.pywebkitgtk import OauthGui
from pytripodyql import TriPod
if __name__ == '__main__':
    AK = "dj0yJmk9WjNaQkoxdDZyanJ2JmQ9WVdrOVYyTjNkMFJYTm1jbWNHbzlNVE13TWpBd05EVS0mcz1jb25zdW1lcnNlY3JldCZ4PWQ0"
    SK = "9d8c16493dfc5de7010f9cd173e91cb82d63f924"
    tri = TriPod(AK, SK)
    yuri = tri.yuri
    #yuri = 'http://localhost/'
    #yuri = 'https://localhost/oauth_callback'
    def callback (tk):
        print ('callbacked: ', tk, type(tk))
        tri.right_leg = tk
        print ('front ', tri.front_leg)
        print ('dash board: \n', tri.execute("select * from meme.user.dashboard").rows)
        print ("\n")
        print ('my posts: \n', tri.execute("select * from meme.posts(2) where owner_guid = @owner_guid", {'owner_guid':'me'}).rows)
        return tk
    oauthGui = OauthGui(yuri, callback)
    oauthGui.main()