'''
This module I made to be easy to auth user in oauth2
Require:
webkit, gtk, gobject
Created on Nov 24, 2011

@author: hugosenari


Part of this code I get from: 
http://ardoris.wordpress.com/2009/04/26/a-browser-in-14-lines-using-python-and-webkit/
'''

import gtk, re, webkit, urlparse

class OauthGuid(object):
    '''
    Easy python oauth2 authentication interface with webkit and gtk
    '''

    def __init__(self, uri, callback, oauthCallback=None, app=None, 
                 title='Authentication', 
                 label='If redirect doesn\'t work, type code on input then click in ok.', 
                 bt_label='ok'):
        '''
        params:
            uri: string url to open in browser for user get oauth verifier
            callback: callable function that receives as unique param oauth verifiers (str)
            oauthCallback: pattern of redirect url with oauth verifier
            app: gtk
            title: window title
            label: input label
            bt_label: ok button label
        '''
        #try to use user pattern
        if oauthCallback:
            self._oauth_callback = oauthCallback
        #try to use common pattern 
        elif re.match('oauth_callback=', uri):
            params = uri.split('oauth_callback=')
            self._oauth_callback = params[1].split('&')[0]
        #try to use default pattern
        else:
            sep = "&" if re.match('.+\?.+', uri) else "?"
            self._oauth_callback = 'https%3A%2F%2Flocalhost%2Foauth_callback'
            uri = "%s%soauth_callback=%s" % (uri, sep, self._oauth_callback) 
            
        self.uri = uri
        self.callback = callback
        self.window = None
        self.tx_label = label
        self.tx_title = title
        self.tx_bt_label = bt_label
        self._show()

    def _show(self):
        ##draw window
        self.window = gtk.Window()
        self.window.set_title(self.tx_title)
        vbox = gtk.VBox()
        self.window.maximize()
        entry = gtk.Entry()
        entry.set_text(self.uri)
        vbox.add(entry)
        ##draw broser
        browser = webkit.WebView()
        def callback (*args): self._callback(*args)
        browser.connect('resource-request-starting', callback)
        browser.open(self.uri)
        vbox.add(browser)
        ##draw form fields
        label = gtk.Label(self.tx_label)
        vbox.add(label)
        hbox = gtk.HBox()
        self.entry = gtk.Entry()
        #self.entry.set_text(self.uri)
        hbox.add(self.entry)
        btn = gtk.Button()
        btnlabel = gtk.Label(self.tx_bt_label)
        btn.add(btnlabel)
        def clicked(*args): 
            self._ok(*args)
        btn.connect('clicked', clicked)
        hbox.add(btn)
        vbox.add(hbox)
        self.window.add(vbox)
        ##show all to user
        self.window.show_all()
    
    def _callback(self, webView, webFrame, webResource, request, response, *args):
        if isinstance(request, webkit.NetworkRequest) \
                and re.match(self._oauth_callback, request.get_uri()):
            uri  = request.get_uri()
            callback = self.callback
            if callback and callable(callback):
                self._destroy()
                webView.stop_loading()
                return callback(uri)
            return uri
    
    def _ok(self, *args):
        code = self.entry.get_text()
        callback = self.callback 
        if callback and callable(callback):
            self._destroy()
            return callback(code)
        return code
    
    def _destroy(self):
        self.window.destroy()
    
    def main(self, *args, **kw):
        gtk.main(*args, **kw)

class OauthGui(OauthGuid):
    def __init__(self, uri, callback, oauthCallback=None, paramName='oauth_token'):
        '''
        params:
            uri: string url to open in browser for user get oauth verifier
            callback: callable function that receives as unique param oauth verifiers (str)
            oauthCallback: pattern of redirect url with oauth verifier
            paramName: param name in callback result
        '''
        def _callback(url):
            if paramName:
                for param in urlparse.urlparse(url).query.split('&'):
                    keyValue = param.split('=')
                    if len(keyValue) > 1 and keyValue[0] == paramName:
                        if callback and callable(callback):
                            return callback(keyValue[1])
            if callback and callable(callback):
                return callback(url)
            return url

        super(OauthGui, self).__init__(uri, _callback, oauthCallback=None)